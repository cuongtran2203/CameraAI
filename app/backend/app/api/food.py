"""
Food & QC Routes
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy import func

from app.db.database import get_db
from app.models.models import (
    FoodItem, FoodMasterImage, FoodQCResult, Branch, User
)
from app.schemas.schemas import (
    FoodItemCreate, FoodItemResponse,
    FoodMasterImageCreate, FoodMasterImageResponse,
    FoodQCResultResponse
)
from app.api.auth import get_current_user

router = APIRouter(prefix="/food", tags=["Food & QC"])


# ========================
# Food Item Routes
# ========================

@router.get("/items", response_model=List[FoodItemResponse])
async def get_food_items(
    branch_id: Optional[UUID] = None,
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of food items
    """
    query = select(FoodItem)

    if branch_id:
        query = query.where(FoodItem.branch_id == branch_id)
    if category:
        query = query.where(FoodItem.category == category)
    if is_active is not None:
        query = query.where(FoodItem.is_active == is_active)
    if search:
        query = query.where(FoodItem.name.ilike(f"%{search}%"))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    # Skip for now

    # Pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(FoodItem.name)

    result = await db.execute(query)
    items = result.scalars().all()

    return [FoodItemResponse.model_validate(i) for i in items]


@router.get("/items/{item_id}", response_model=FoodItemResponse)
async def get_food_item(
    item_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get food item by ID
    """
    result = await db.execute(select(FoodItem).where(FoodItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found"
        )

    return FoodItemResponse.model_validate(item)


@router.post("/items", response_model=FoodItemResponse)
async def create_food_item(
    item_data: FoodItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new food item
    """
    # Check unique code within branch
    if item_data.code:
        result = await db.execute(
            select(FoodItem).where(
                and_(
                    FoodItem.branch_id == item_data.branch_id,
                    FoodItem.code == item_data.code
                )
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Food code already exists in this branch"
            )

    item = FoodItem(**item_data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)

    return FoodItemResponse.model_validate(item)


@router.put("/items/{item_id}", response_model=FoodItemResponse)
async def update_food_item(
    item_id: UUID,
    item_data: FoodItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update food item
    """
    result = await db.execute(select(FoodItem).where(FoodItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found"
        )

    for field, value in item_data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    item.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(item)

    return FoodItemResponse.model_validate(item)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_item(
    item_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete food item (soft delete)
    """
    result = await db.execute(select(FoodItem).where(FoodItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found"
        )

    item.is_active = False
    await db.commit()

    return None


# ========================
# Master Image Routes
# ========================

@router.get("/items/{item_id}/master-images", response_model=List[FoodMasterImageResponse])
async def get_master_images(
    item_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get master images for a food item
    """
    result = await db.execute(
        select(FoodMasterImage)
        .where(and_(FoodMasterImage.food_item_id == item_id, FoodMasterImage.is_active == True))
        .order_by(FoodMasterImage.created_at.desc())
    )
    images = result.scalars().all()

    return [FoodMasterImageResponse.model_validate(i) for i in images]


@router.post("/items/{item_id}/master-images", response_model=FoodMasterImageResponse)
async def add_master_image(
    item_id: UUID,
    image_data: FoodMasterImageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add master image for a food item
    """
    # Verify food item exists
    result = await db.execute(select(FoodItem).where(FoodItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found"
        )

    master_image = FoodMasterImage(
        food_item_id=item_id,
        image_url=image_data.image_url,
        embedding_data=image_data.embedding,
        captured_by=current_user.id if hasattr(current_user, 'id') else None,
        notes=image_data.notes
    )
    db.add(master_image)
    await db.commit()
    await db.refresh(master_image)

    return FoodMasterImageResponse.model_validate(master_image)


@router.delete("/master-images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_master_image(
    image_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete master image
    """
    result = await db.execute(select(FoodMasterImage).where(FoodMasterImage.id == image_id))
    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master image not found"
        )

    image.is_active = False
    await db.commit()

    return None


# ========================
# QC Results Routes
# ========================

@router.get("/qc-results", response_model=List[FoodQCResultResponse])
async def get_qc_results(
    branch_id: Optional[UUID] = None,
    food_item_id: Optional[UUID] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status_filter: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get food QC results
    """
    # Always join FoodItem to avoid errors
    query = select(FoodQCResult).join(FoodItem, FoodQCResult.food_item_id == FoodItem.id, isouter=True)

    if branch_id:
        query = query.where(FoodItem.branch_id == branch_id)
    if food_item_id:
        query = query.where(FoodQCResult.food_item_id == food_item_id)
    if start_date:
        query = query.where(FoodQCResult.checked_at >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.where(FoodQCResult.checked_at <= datetime.combine(end_date, datetime.max.time()))
    if status_filter:
        query = query.where(FoodQCResult.result_status == status_filter)

    # Pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(FoodQCResult.checked_at.desc())

    try:
        result = await db.execute(query)
        results = result.scalars().all()
        return [FoodQCResultResponse.model_validate(r) for r in results]
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/qc-summary")
async def get_qc_summary(
    branch_id: UUID,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get QC summary statistics
    """
    today = start_date or datetime.utcnow().date()
    end = end_date or today

    # Get summary
    result = await db.execute(
        select(
            func.count(FoodQCResult.id).label('total'),
            func.sum(func.cast(FoodQCResult.result_status == 'pass', int)).label('pass'),
            func.sum(func.cast(FoodQCResult.result_status == 'fail', int)).label('fail'),
            func.sum(func.cast(FoodQCResult.result_status == 'warning', int)).label('warning')
        )
        .join(FoodItem)
        .where(and_(
            FoodItem.branch_id == branch_id,
            FoodQCResult.checked_at >= datetime.combine(today, datetime.min.time()),
            FoodQCResult.checked_at <= datetime.combine(end, datetime.max.time())
        ))
    )
    row = result.one()

    total = row.total or 0
    pass_count = getattr(row, 'pass', 0) or 0

    return {
        "start_date": today.isoformat(),
        "end_date": end.isoformat(),
        "total_checks": total,
        "pass_count": pass_count,
        "fail_count": getattr(row, 'fail', 0) or 0,
        "warning_count": getattr(row, 'warning', 0) or 0,
        "pass_rate": round(pass_count / total, 2) if total > 0 else 0
    }
