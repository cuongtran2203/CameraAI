"""
Camera Routes
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db.database import get_db
from app.models.models import Camera, CameraAIConfig, Branch, User
from app.schemas.schemas import (
    CameraCreate, CameraUpdate, CameraResponse,
    CameraAIConfigCreate, CameraAIConfigResponse
)
from app.api.auth import get_current_user
from app.services.kafka_service import send_camera_command, send_ai_config

router = APIRouter(prefix="/cameras", tags=["Cameras"])


# ========================
# Camera Routes
# ========================

@router.get("", response_model=List[CameraResponse])
async def get_cameras(
    branch_id: Optional[UUID] = None,
    is_active: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of cameras
    """
    query = select(Camera)

    # Filter by branch if provided
    if branch_id:
        query = query.where(Camera.branch_id == branch_id)

    # Filter by active status
    if is_active is not None:
        query = query.where(Camera.is_active == is_active)

    # Get total count
    from sqlalchemy import func
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # Pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(Camera.created_at.desc())

    result = await db.execute(query)
    cameras = result.scalars().all()

    return [CameraResponse.model_validate(c) for c in cameras]


@router.get("/{camera_id}", response_model=CameraResponse)
async def get_camera(
    camera_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get camera by ID
    """
    result = await db.execute(select(Camera).where(Camera.id == camera_id))
    camera = result.scalar_one_or_none()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    return CameraResponse.model_validate(camera)


@router.post("", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
async def create_camera(
    camera_data: CameraCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new camera
    """
    # Verify branch exists
    result = await db.execute(select(Branch).where(Branch.id == camera_data.branch_id))
    branch = result.scalar_one_or_none()

    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found"
        )

    # Check camera code unique within branch
    result = await db.execute(
        select(Camera).where(
            and_(
                Camera.branch_id == camera_data.branch_id,
                Camera.code == camera_data.code
            )
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Camera code already exists in this branch"
        )

    # Create camera
    camera = Camera(
        branch_id=camera_data.branch_id,
        name=camera_data.name,
        code=camera_data.code,
        rtsp_url=camera_data.rtsp_url,
        location=camera_data.location,
        stream_type=camera_data.stream_type,
        resolution=camera_data.resolution,
        fps=camera_data.fps,
        ai_enabled=camera_data.ai_enabled.model_dump() if camera_data.ai_enabled else None
    )

    db.add(camera)
    await db.commit()
    await db.refresh(camera)

    return CameraResponse.model_validate(camera)


@router.put("/{camera_id}", response_model=CameraResponse)
async def update_camera(
    camera_id: UUID,
    camera_data: CameraUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update camera
    """
    result = await db.execute(select(Camera).where(Camera.id == camera_id))
    camera = result.scalar_one_or_none()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    # Update fields
    if camera_data.name is not None:
        camera.name = camera_data.name
    if camera_data.rtsp_url is not None:
        camera.rtsp_url = camera_data.rtsp_url
    if camera_data.location is not None:
        camera.location = camera_data.location
    if camera_data.ai_enabled is not None:
        camera.ai_enabled = camera_data.ai_enabled.model_dump()
    if camera_data.is_active is not None:
        camera.is_active = camera_data.is_active

    camera.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(camera)

    return CameraResponse.model_validate(camera)


@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(
    camera_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete camera (soft delete)
    """
    result = await db.execute(select(Camera).where(Camera.id == camera_id))
    camera = result.scalar_one_or_none()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    camera.is_active = False
    await db.commit()

    return None


# ========================
# Camera Control Routes
# ========================

@router.post("/{camera_id}/start")
async def start_stream(
    camera_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Start camera stream (send command to AI)
    """
    result = await db.execute(select(Camera).where(Camera.id == camera_id))
    camera = result.scalar_one_or_none()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    if not camera.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Camera is inactive"
        )

    # Send command to Kafka
    success = await send_camera_command(
        camera_id=str(camera_id),
        command="START_STREAM",
        options={
            "rtsp_url": camera.rtsp_url,
            "ai_enabled": camera.ai_enabled,
            "resolution": camera.resolution,
            "fps": camera.fps
        }
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start stream"
        )

    return {"message": "Stream started", "camera_id": str(camera_id)}


@router.post("/{camera_id}/stop")
async def stop_stream(
    camera_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Stop camera stream
    """
    success = await send_camera_command(
        camera_id=str(camera_id),
        command="STOP_STREAM"
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to stop stream"
        )

    return {"message": "Stream stopped", "camera_id": str(camera_id)}


@router.post("/{camera_id}/restart")
async def restart_stream(
    camera_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Restart camera stream
    """
    success = await send_camera_command(
        camera_id=str(camera_id),
        command="RESTART"
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to restart stream"
        )

    return {"message": "Stream restarted", "camera_id": str(camera_id)}


# ========================
# Camera AI Config Routes
# ========================

@router.get("/{camera_id}/ai-config", response_model=CameraAIConfigResponse)
async def get_ai_config(
    camera_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get camera AI configuration
    """
    result = await db.execute(select(CameraAIConfig).where(CameraAIConfig.camera_id == camera_id))
    config = result.scalar_one_or_none()

    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI config not found"
        )

    return CameraAIConfigResponse.model_validate(config)


@router.post("/{camera_id}/ai-config", response_model=CameraAIConfigResponse)
async def create_ai_config(
    camera_id: UUID,
    config_data: CameraAIConfigCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create/update camera AI configuration
    """
    # Verify camera exists
    result = await db.execute(select(Camera).where(Camera.id == camera_id))
    camera = result.scalar_one_or_none()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    # Check if config exists
    result = await db.execute(select(CameraAIConfig).where(CameraAIConfig.camera_id == camera_id))
    existing_config = result.scalar_one_or_none()

    if existing_config:
        # Update existing config
        for field, value in config_data.model_dump().items():
            if value is not None:
                setattr(existing_config, field, value)
        config = existing_config
    else:
        # Create new config
        config = CameraAIConfig(
            camera_id=camera_id,
            **config_data.model_dump()
        )
        db.add(config)

    await db.commit()
    await db.refresh(config)

    # Send config to AI via Kafka
    await send_ai_config(str(camera_id), config_data.model_dump())

    return CameraAIConfigResponse.model_validate(config)
