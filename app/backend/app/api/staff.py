"""
Staff Routes
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy import func

from app.db.database import get_db
from app.models.models import Staff, StaffFace, Shift, ShiftSchedule, User
from app.schemas.schemas import (
    StaffCreate, StaffUpdate, StaffResponse,
    StaffFaceCreate, StaffFaceResponse,
    ShiftCreate, ShiftResponse, ShiftScheduleCreate, ShiftScheduleResponse,
    StaffActionCreate, StaffActionResponse, DailyPerformanceResponse
)
from app.api.auth import get_current_user

router = APIRouter(prefix="/staff", tags=["Staff"])


# ========================
# Staff Routes
# ========================

@router.get("", response_model=List[StaffResponse])
async def get_staff(
    branch_id: Optional[UUID] = None,
    department: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of staff members
    """
    query = select(Staff)

    # Filters
    if branch_id:
        query = query.where(Staff.branch_id == branch_id)
    if department:
        query = query.where(Staff.department == department)
    if is_active is not None:
        query = query.where(Staff.is_active == is_active)
    if search:
        query = query.where(
            (Staff.full_name.ilike(f"%{search}%")) |
            (Staff.employee_code.ilike(f"%{search}%"))
        )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # Pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(Staff.full_name)

    result = await db.execute(query)
    staff = result.scalars().all()

    return [StaffResponse.model_validate(s) for s in staff]


@router.get("/{staff_id}", response_model=StaffResponse)
async def get_staff(
    staff_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get staff by ID
    """
    result = await db.execute(select(Staff).where(Staff.id == staff_id))
    staff = result.scalar_one_or_none()

    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found"
        )

    return StaffResponse.model_validate(staff)


@router.post("", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
async def create_staff(
    staff_data: StaffCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new staff member
    """
    # Check unique employee code within branch
    result = await db.execute(
        select(Staff).where(
            and_(
                Staff.branch_id == staff_data.branch_id,
                Staff.employee_code == staff_data.employee_code
            )
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee code already exists in this branch"
        )

    staff = Staff(**staff_data.model_dump())
    db.add(staff)
    await db.commit()
    await db.refresh(staff)

    return StaffResponse.model_validate(staff)


@router.put("/{staff_id}", response_model=StaffResponse)
async def update_staff(
    staff_id: UUID,
    staff_data: StaffUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update staff member
    """
    result = await db.execute(select(Staff).where(Staff.id == staff_id))
    staff = result.scalar_one_or_none()

    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found"
        )

    # Update fields
    for field, value in staff_data.model_dump(exclude_unset=True).items():
        setattr(staff, field, value)

    staff.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(staff)

    return StaffResponse.model_validate(staff)


@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(
    staff_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete staff (soft delete)
    """
    result = await db.execute(select(Staff).where(Staff.id == staff_id))
    staff = result.scalar_one_or_none()

    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found"
        )

    staff.is_active = False
    await db.commit()

    return None


# ========================
# Staff Face Routes
# ========================

@router.get("/{staff_id}/faces", response_model=List[StaffFaceResponse])
async def get_staff_faces(
    staff_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all faces of a staff member
    """
    result = await db.execute(
        select(StaffFace).where(StaffFace.staff_id == staff_id)
    )
    faces = result.scalars().all()

    return [StaffFaceResponse.model_validate(f) for f in faces]


@router.post("/{staff_id}/faces", response_model=StaffFaceResponse)
async def add_staff_face(
    staff_id: UUID,
    face_data: StaffFaceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add face for staff member
    """
    # Verify staff exists
    result = await db.execute(select(Staff).where(Staff.id == staff_id))
    staff = result.scalar_one_or_none()

    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found"
        )

    # If setting as primary, unset other primary
    if face_data.is_primary:
        result = await db.execute(
            select(StaffFace).where(
                and_(StaffFace.staff_id == staff_id, StaffFace.is_primary == True)
            )
        )
        for face in result.scalars().all():
            face.is_primary = False

    face = StaffFace(
        staff_id=staff_id,
        embedding_data=face_data.embedding,
        image_url=face_data.image_url,
        quality_score=face_data.quality_score,
        is_primary=face_data.is_primary
    )
    db.add(face)
    await db.commit()
    await db.refresh(face)

    return StaffFaceResponse.model_validate(face)


@router.delete("/{staff_id}/faces/{face_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff_face(
    staff_id: UUID,
    face_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete staff face
    """
    result = await db.execute(
        select(StaffFace).where(
            and_(StaffFace.id == face_id, StaffFace.staff_id == staff_id)
        )
    )
    face = result.scalar_one_or_none()

    if not face:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Face not found"
        )

    await db.delete(face)
    await db.commit()

    return None


# ========================
# Shift Routes
# ========================

@router.get("/shifts", response_model=List[ShiftResponse])
async def get_shifts(
    branch_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of shifts
    """
    query = select(Shift)
    if branch_id:
        query = query.where(Shift.branch_id == branch_id)

    result = await db.execute(query.order_by(Shift.start_time))
    shifts = result.scalars().all()

    return [ShiftResponse.model_validate(s) for s in shifts]


@router.post("/shifts", response_model=ShiftResponse)
async def create_shift(
    shift_data: ShiftCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new shift
    """
    shift = Shift(**shift_data.model_dump())
    db.add(shift)
    await db.commit()
    await db.refresh(shift)

    return ShiftResponse.model_validate(shift)


# ========================
# Staff Performance Routes
# ========================

@router.get("/performance", response_model=List[DailyPerformanceResponse])
async def get_staff_performance(
    branch_id: Optional[UUID] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get staff performance data
    """
    from app.models.models import DailyStaffPerformance

    query = select(DailyStaffPerformance)

    if branch_id:
        query = query.join(Staff).where(Staff.branch_id == branch_id)
    if start_date:
        query = query.where(DailyStaffPerformance.work_date >= start_date)
    if end_date:
        query = query.where(DailyStaffPerformance.work_date <= end_date)

    result = await db.execute(query.order_by(DailyStaffPerformance.work_date.desc()))
    performances = result.scalars().all()

    return [DailyPerformanceResponse.model_validate(p) for p in performances]


@router.get("/performance/{staff_id}", response_model=List[DailyPerformanceResponse])
async def get_staff_performance_by_id(
    staff_id: UUID,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get performance for specific staff
    """
    from app.models.models import DailyStaffPerformance

    query = select(DailyStaffPerformance).where(DailyStaffPerformance.staff_id == staff_id)

    if start_date:
        query = query.where(DailyStaffPerformance.work_date >= start_date)
    if end_date:
        query = query.where(DailyStaffPerformance.work_date <= end_date)

    result = await db.execute(query.order_by(DailyStaffPerformance.work_date.desc()))
    performances = result.scalars().all()

    return [DailyPerformanceResponse.model_validate(p) for p in performances]
