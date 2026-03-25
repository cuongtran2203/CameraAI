"""
Dashboard Routes - Real-time stats and reporting
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.models.models import (
    Branch, Camera, Staff, StaffAction, StaffFace,
    AttendanceRecord, DailyAttendance,
    FoodQCResult, FoodItem,
    CustomerEvent, DailyCustomerStats,
    DailyReport, User
)
from app.schemas.schemas import (
    DashboardStatsResponse, StaffSummary, ActionSummary,
    FoodQCSummary, CustomerSummary,
    DailyReportResponse
)
from app.api.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# ========================
# Dashboard Stats
# ========================

@router.get("/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(
    branch_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get real-time dashboard statistics for a branch
    """
    today = datetime.utcnow().date()

    # Verify branch exists
    result = await db.execute(select(Branch).where(Branch.id == branch_id))
    branch = result.scalar_one_or_none()
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found"
        )

    # === Staff Stats ===
    # Get all active staff
    staff_result = await db.execute(
        select(func.count(Staff.id))
        .where(and_(Staff.branch_id == branch_id, Staff.is_active == True))
    )
    total_staff = staff_result.scalar() or 0

    # Get today's attendance
    attendance_result = await db.execute(
        select(func.count(DailyAttendance.id))
        .join(Staff)
        .where(and_(
            Staff.branch_id == branch_id,
            DailyAttendance.work_date == today,
            DailyAttendance.status.in_(['present', 'late'])
        ))
    )
    present_staff = attendance_result.scalar() or 0

    attendance_rate = present_staff / total_staff if total_staff > 0 else 0

    staff_summary = {
        "total_online": present_staff,
        "total_scheduled": total_staff,
        "attendance_rate": round(attendance_rate, 2)
    }

    # === Action Stats ===
    # Get today's actions
    action_result = await db.execute(
        select(
            StaffAction.action_type,
            func.count(StaffAction.id).label('count')
        )
        .join(Staff)
        .where(and_(
            Staff.branch_id == branch_id,
            StaffAction.started_at >= datetime.combine(today, datetime.min.time())
        ))
        .group_by(StaffAction.action_type)
    )
    action_counts = {row.action_type: row.count for row in action_result}

    productive_count = sum([
        action_counts.get('cooking', 0),
        action_counts.get('washing', 0),
        action_counts.get('cleaning', 0),
        action_counts.get('serving', 0)
    ])
    idle_count = action_counts.get('idle', 0)

    top_actions = [
        {"action": action, "count": count}
        for action, count in sorted(action_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    action_summary = {
        "productive_count": productive_count,
        "idle_count": idle_count,
        "top_actions": top_actions
    }

    # === Food QC Stats ===
    # Get today's QC results
    qc_result = await db.execute(
        select(
            func.count(FoodQCResult.id).label('total'),
            func.sum(func.cast(FoodQCResult.result_status == 'pass', Integer)).label('pass'),
            func.sum(func.cast(FoodQCResult.result_status == 'fail', Integer)).label('fail'),
            func.sum(func.cast(FoodQCResult.result_status == 'warning', Integer)).label('warning')
        )
        .where(and_(
            FoodQCResult.food_item_id.in_(
                select(FoodItem.id).where(FoodItem.branch_id == branch_id)
            ),
            FoodQCResult.checked_at >= datetime.combine(today, datetime.min.time())
        ))
    )
    qc_row = qc_result.one()
    total_qc = qc_row.total or 0
    pass_qc = getattr(qc_row, 'pass', 0) or 0
    fail_qc = getattr(qc_row, 'fail', 0) or 0
    warning_qc = getattr(qc_row, 'warning', 0) or 0

    pass_rate = pass_qc / total_qc if total_qc > 0 else 0

    food_qc_summary = {
        "total_checked": total_qc,
        "pass_count": pass_qc,
        "fail_count": fail_qc,
        "warning_count": warning_qc,
        "pass_rate": round(pass_rate, 2)
    }

    # === Customer Stats ===
    # Get today's customer events
    customer_result = await db.execute(
        select(
            func.count(CustomerEvent.id).label('total'),
            func.sum(func.cast(CustomerEvent.event_type == 'entry', Integer)).label('entry'),
            func.sum(func.cast(CustomerEvent.event_type == 'exit', Integer)).label('exit')
        )
        .where(and_(
            CustomerEvent.branch_id == branch_id,
            CustomerEvent.detected_at >= datetime.combine(today, datetime.min.time()),
            CustomerEvent.is_staff == False
        ))
    )
    customer_row = customer_result.one()
    entry_today = customer_row.entry or 0

    # Get current in-store (entry - exit that haven't exited)
    # Simplified: just use entry - exit for now
    current_in_store = entry_today - (customer_row.exit or 0)

    # Get average dwell time
    dwell_result = await db.execute(
        select(func.avg(CustomerEvent.dwell_time_seconds))
        .where(and_(
            CustomerEvent.branch_id == branch_id,
            CustomerEvent.detected_at >= datetime.combine(today, datetime.min.time()),
            CustomerEvent.dwell_time_seconds.isnot(None)
        ))
    )
    avg_dwell = dwell_result.scalar()
    avg_dwell_minutes = int(avg_dwell / 60) if avg_dwell else 0

    customer_summary = {
        "current_in_store": max(0, current_in_store),
        "entry_today": entry_today,
        "avg_dwell_time_minutes": avg_dwell_minutes,
        "peak_hour": None  # TODO: Calculate from hourly stats
    }

    return DashboardStatsResponse(
        timestamp=datetime.utcnow(),
        staff=staff_summary,
        actions=action_summary,
        food_qc=food_qc_summary,
        customers=customer_summary
    )


# ========================
# Daily Reports
# ========================

@router.get("/reports", response_model=List[DailyReportResponse])
async def get_daily_reports(
    branch_id: Optional[UUID] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(30, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get daily reports
    """
    query = select(DailyReport)

    if branch_id:
        query = query.where(DailyReport.branch_id == branch_id)
    if start_date:
        query = query.where(DailyReport.report_date >= start_date)
    if end_date:
        query = query.where(DailyReport.report_date <= end_date)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    # Skip for now

    # Pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(DailyReport.report_date.desc())

    result = await db.execute(query)
    reports = result.scalars().all()

    return [DailyReportResponse.model_validate(r) for r in reports]


@router.get("/reports/{report_date}", response_model=DailyReportResponse)
async def get_daily_report(
    branch_id: UUID,
    report_date: date,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific daily report
    """
    result = await db.execute(
        select(DailyReport).where(
            and_(
                DailyReport.branch_id == branch_id,
                DailyReport.report_date == report_date
            )
        )
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    return DailyReportResponse.model_validate(report)


# ========================
# Real-time Stream Data
# ========================

@router.get("/realtime/{camera_id}")
async def get_realtime_camera_data(
    camera_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get real-time data for a specific camera
    Used for WebSocket connection establishment
    """
    result = await db.execute(select(Camera).where(Camera.id == camera_id))
    camera = result.scalar_one_or_none()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    # Get current active actions for this camera
    recent_actions = await db.execute(
        select(StaffAction)
        .options(selectinload(StaffAction.staff))
        .where(and_(
            StaffAction.camera_id == camera_id,
            StaffAction.ended_at.is_(None)
        ))
        .order_by(StaffAction.started_at.desc())
        .limit(10)
    )

    return {
        "camera_id": str(camera_id),
        "camera_name": camera.name,
        "location": camera.location,
        "ai_enabled": camera.ai_enabled,
        "active_actions": [
            {
                "staff_id": str(a.staff_id),
                "staff_name": a.staff.full_name if a.staff else None,
                "action_type": a.action_type,
                "started_at": a.started_at.isoformat()
            }
            for a in recent_actions.scalars().all()
        ]
    }


# ========================
# AI Streaming Data Simulation (15-minute intervals)
# ========================

import random
from datetime import datetime, time

@router.get("/ai-stream/timestamps")
async def get_ai_stream_timestamps(
    branch_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of 15-minute timestamp intervals for today
    Used to fetch AI data for each interval
    """
    # Verify branch exists
    result = await db.execute(select(Branch).where(Branch.id == branch_id))
    branch = result.scalar_one_or_none()
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found"
        )

    # Generate timestamps from 6:00 AM to 10:00 PM (last 15-minute interval)
    timestamps = []
    current_time = time(6, 0)
    end_time = time(22, 0)

    while current_time <= end_time:
        # Create datetime for today at this time
        now = datetime.utcnow()
        dt = datetime.combine(now.date(), current_time)
        timestamps.append(dt.isoformat())
        # Add 15 minutes
        current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=15)).time()

    return {
        "branch_id": str(branch_id),
        "timestamps": timestamps
    }


@router.get("/ai-stream/data")
async def get_ai_stream_data(
    branch_id: UUID,
    timestamp: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get simulated AI data for a specific 15-minute interval
    Returns dict with customer, staff, food QC, and safety data
    """
    # Verify branch exists
    result = await db.execute(select(Branch).where(Branch.id == branch_id))
    branch = result.scalar_one_or_none()
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found"
        )

    try:
        ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid timestamp format"
        )

    # Simulate AI data based on time of day
    hour = ts.hour

    # Adjust activity based on time (lunch/dinner rush)
    if 11 <= hour <= 13:
        activity_multiplier = 1.5  # Lunch rush
    elif 18 <= hour <= 20:
        activity_multiplier = 1.8  # Dinner rush
    else:
        activity_multiplier = 0.7  # Off-peak

    # Generate simulated data
    customer_entry = int(random.randint(3, 10) * activity_multiplier)
    customer_exit = int(random.randint(2, 8) * activity_multiplier)

    # Staff activities
    staff_activities = [
        {"staff_id": f"staff-{i}", "staff_name": f"Staff {i}", "action": random.choice(["cooking", "washing", "cleaning", "serving", "preparing"]), "duration_min": random.randint(5, 15)}
        for i in range(1, random.randint(4, 8))
    ]

    # Food QC results
    food_items_checked = random.randint(5, 15)
    qc_pass = int(food_items_checked * random.uniform(0.75, 0.95))
    qc_fail = food_items_checked - qc_pass
    qc_warnings = random.randint(0, 2)

    # Safety alerts (random chance)
    safety_alerts = []
    if random.random() < 0.15:  # 15% chance
        safety_alerts.append({
            "type": random.choice(["no_helmet", "no_gloves", "foreign_object", "temperature_alert"]),
            "severity": random.choice(["warning", "critical"]),
            "location": random.choice(["kitchen_1", "kitchen_2", "grill_area"]),
            "description": random.choice([
                "Staff detected without safety helmet",
                "Temperature exceeds safe threshold",
                "Foreign object detected in food",
                "Staff not wearing gloves"
            ])
        })

    # Equipment status
    equipment_status = [
        {"equipment_id": f"eq-{i}", "name": random.choice(["Oven", "Refrigerator", "Freezer", "Dishwasher", "Fryer"]), "status": random.choice(["normal", "normal", "normal", "warning"]), "temperature": random.randint(20, 180) if "Oven" in random.choice(["Oven", "Fryer"]) else random.randint(2, 8)}
        for i in range(1, 6)
    ]

    # Return complete AI data dict
    return {
        "timestamp": ts.isoformat(),
        "branch_id": str(branch_id),
        "customers": {
            "entry_count": customer_entry,
            "exit_count": customer_exit,
            "current_in_store": customer_entry - customer_exit,
            "avg_dwell_time_min": random.randint(15, 45),
            "peak_detection": random.choice([True, False]) if activity_multiplier > 1 else False
        },
        "staff": {
            "active_count": len(staff_activities),
            "activities": staff_activities,
            "productivity_score": random.randint(70, 95)
        },
        "food_qc": {
            "items_checked": food_items_checked,
            "passed": qc_pass,
            "failed": qc_fail,
            "warnings": qc_warnings,
            "pass_rate": round(qc_pass / food_items_checked * 100, 1) if food_items_checked > 0 else 0
        },
        "safety": {
            "alerts": safety_alerts,
            "total_alerts": len(safety_alerts),
            "critical_alerts": sum(1 for a in safety_alerts if a["severity"] == "critical")
        },
        "equipment": {
            "items": equipment_status,
            "warnings": sum(1 for e in equipment_status if e["status"] == "warning")
        },
        "summary": {
            "overall_score": random.randint(75, 95),
            "status": random.choice(["normal", "normal", "normal", "attention"]) if len(safety_alerts) == 0 else "attention",
            "notes": "All systems operational" if len(safety_alerts) == 0 else f"{len(safety_alerts)} safety alert(s) require attention"
        }
    }


@router.get("/ai-stream/today")
async def get_ai_stream_today(
    branch_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all AI stream data for today (all 15-minute intervals)
    Returns a dict with timestamps as keys
    """
    # Verify branch exists
    result = await db.execute(select(Branch).where(Branch.id == branch_id))
    branch = result.scalar_one_or_none()
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found"
        )

    # Generate all timestamps for today
    timestamps = []
    current_time = time(6, 0)
    end_time = time(22, 0)

    now = datetime.utcnow()
    while current_time <= end_time:
        dt = datetime.combine(now.date(), current_time)
        timestamps.append(dt)
        current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=15)).time()

    # Generate data for each timestamp
    all_data = {}
    for ts in timestamps:
        hour = ts.hour
        if 11 <= hour <= 13:
            activity_multiplier = 1.5
        elif 18 <= hour <= 20:
            activity_multiplier = 1.8
        else:
            activity_multiplier = 0.7

        customer_entry = int(random.randint(3, 10) * activity_multiplier)
        customer_exit = int(random.randint(2, 8) * activity_multiplier)

        staff_activities = [
            {"staff_id": f"staff-{i}", "staff_name": f"Staff {i}", "action": random.choice(["cooking", "washing", "cleaning", "serving", "preparing"]), "duration_min": random.randint(5, 15)}
            for i in range(1, random.randint(4, 8))
        ]

        food_items_checked = random.randint(5, 15)
        qc_pass = int(food_items_checked * random.uniform(0.75, 0.95))
        qc_fail = food_items_checked - qc_pass
        qc_warnings = random.randint(0, 2)

        safety_alerts = []
        if random.random() < 0.15:
            safety_alerts.append({
                "type": random.choice(["no_helmet", "no_gloves", "foreign_object", "temperature_alert"]),
                "severity": random.choice(["warning", "critical"]),
                "location": random.choice(["kitchen_1", "kitchen_2", "grill_area"]),
                "description": random.choice([
                    "Staff detected without safety helmet",
                    "Temperature exceeds safe threshold",
                    "Foreign object detected in food",
                    "Staff not wearing gloves"
                ])
            })

        equipment_status = [
            {"equipment_id": f"eq-{i}", "name": random.choice(["Oven", "Refrigerator", "Freezer", "Dishwasher", "Fryer"]), "status": random.choice(["normal", "normal", "normal", "warning"]), "temperature": random.randint(20, 180) if "Oven" in random.choice(["Oven", "Fryer"]) else random.randint(2, 8)}
            for i in range(1, 6)
        ]

        ts_key = ts.isoformat()
        all_data[ts_key] = {
            "timestamp": ts_key,
            "customers": {
                "entry_count": customer_entry,
                "exit_count": customer_exit,
                "current_in_store": customer_entry - customer_exit,
                "avg_dwell_time_min": random.randint(15, 45),
                "peak_detection": random.choice([True, False]) if activity_multiplier > 1 else False
            },
            "staff": {
                "active_count": len(staff_activities),
                "activities": staff_activities,
                "productivity_score": random.randint(70, 95)
            },
            "food_qc": {
                "items_checked": food_items_checked,
                "passed": qc_pass,
                "failed": qc_fail,
                "warnings": qc_warnings,
                "pass_rate": round(qc_pass / food_items_checked * 100, 1) if food_items_checked > 0 else 0
            },
            "safety": {
                "alerts": safety_alerts,
                "total_alerts": len(safety_alerts),
                "critical_alerts": sum(1 for a in safety_alerts if a["severity"] == "critical")
            },
            "equipment": {
                "items": equipment_status,
                "warnings": sum(1 for e in equipment_status if e["status"] == "warning")
            },
            "summary": {
                "overall_score": random.randint(75, 95),
                "status": random.choice(["normal", "normal", "normal", "attention"]) if len(safety_alerts) == 0 else "attention",
                "notes": "All systems operational" if len(safety_alerts) == 0 else f"{len(safety_alerts)} safety alert(s) require attention"
            }
        }

    return {
        "branch_id": str(branch_id),
        "date": now.date().isoformat(),
        "intervals": timestamps,
        "data": all_data
    }


@router.get("/kitchen/har/current")
async def get_kitchen_har_current(
    branch_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current kitchen HAR (Human Activity Recognition) data
    Used for initial load when entering Kitchen Analytics page
    """
    import random
    from datetime import datetime

    # Verify branch exists
    result = await db.execute(select(Branch).where(Branch.id == branch_id))
    branch = result.scalar_one_or_none()
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found"
        )

    # Get current staff activities
    staff_activities = [
        {"staff_id": "staff_001", "action": "cooking", "zone": "grill"},
        {"staff_id": "staff_002", "action": "preparing", "zone": "prep"},
        {"staff_id": "staff_003", "action": "washing", "zone": "sink"},
        {"staff_id": "staff_004", "action": "cooking", "zone": "fryer"},
        {"staff_id": "staff_005", "action": "plating", "zone": "counter"},
    ]

    staff_names = ["Marco V.", "Sarah L.", "John D.", "Emily K.", "David L."]
    har_data = []

    for i, activity in enumerate(staff_activities):
        work_time = random.randint(30, 120)
        active_pct = random.randint(70, 98)
        har_data.append({
            "staff_id": activity["staff_id"],
            "staff_name": staff_names[i] if i < len(staff_names) else f"Staff {i+1}",
            "current_action": activity["action"],
            "work_time_min": work_time,
            "active_time_min": int(work_time * active_pct / 100),
            "active_percentage": active_pct,
            "zone": activity["zone"],
            "timestamp": datetime.utcnow().isoformat()
        })

    return {
        "branch_id": str(branch_id),
        "timestamp": datetime.utcnow().isoformat(),
        "staff_count": len(har_data),
        "staff": har_data,
        "summary": {
            "total_work_time": sum(s["work_time_min"] for s in har_data),
            "average_active_percentage": sum(s["active_percentage"] for s in har_data) // len(har_data),
            "total_active_time": sum(s["active_time_min"] for s in har_data)
        }
    }


# Helper for SQLAlchemy cast
from sqlalchemy import Integer
