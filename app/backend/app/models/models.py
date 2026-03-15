"""
Database Models - SQLAlchemy ORM (MySQL)
Camera Analyst System
"""
import uuid
import json
from datetime import datetime, date, time
from typing import Optional, List
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float,
    Date, DateTime, Time, ForeignKey, UniqueConstraint,
    Index, CheckConstraint, Enum, JSON, Numeric
)
from sqlalchemy.orm import relationship, backref
from app.db.database import Base


def generate_uuid():
    return str(uuid.uuid4())


def default_uuid():
    return str(uuid.uuid4())


# =====================================================
# 1. TENANT MANAGEMENT
# =====================================================

class Company(Base):
    """Công ty / Chuỗi nhà hàng"""
    __tablename__ = "companies"

    id = Column(String(36), primary_key=True, default=default_uuid)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    address = Column(Text)
    phone = Column(String(20))
    logo_url = Column(String(500))
    settings = Column(JSON, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    branches = relationship("Branch", back_populates="company", cascade="all, delete-orphan")


class Branch(Base):
    """Chi nhánh / Nhà hàng"""
    __tablename__ = "branches"

    id = Column(String(36), primary_key=True, default=default_uuid)
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    address = Column(Text)
    timezone = Column(String(50), default="Asia/Ho_Chi_Minh")
    settings = Column(JSON, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="branches")
    users = relationship("User", back_populates="branch", cascade="all, delete-orphan")
    staff = relationship("Staff", back_populates="branch", cascade="all, delete-orphan")
    cameras = relationship("Camera", back_populates="branch", cascade="all, delete-orphan")
    shifts = relationship("Shift", back_populates="branch", cascade="all, delete-orphan")
    food_items = relationship("FoodItem", back_populates="branch", cascade="all, delete-orphan")
    daily_reports = relationship("DailyReport", back_populates="branch", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('company_id', 'code', name='uq_branch_company_code'),
    )


class User(Base):
    """Người dùng hệ thống"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=default_uuid)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    avatar_url = Column(String(500))
    role = Column(String(50), nullable=False)  # admin, manager, staff
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    branch = relationship("Branch", back_populates="users")
    permissions = relationship("Permission", back_populates="user", cascade="all, delete-orphan")


class Permission(Base):
    """Phân quyền chi tiết (RBAC)"""
    __tablename__ = "permissions"

    id = Column(String(36), primary_key=True, default=default_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resource = Column(String(100), nullable=False)  # cameras, reports, staff, etc.
    actions = Column(JSON, default=list)  # ['read', 'write', 'delete']
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="permissions")

    __table_args__ = (
        UniqueConstraint('user_id', 'resource', name='uq_permission_user_resource'),
    )


# =====================================================
# 2. STAFF MANAGEMENT
# =====================================================

class Staff(Base):
    """Nhân viên"""
    __tablename__ = "staff"

    id = Column(String(36), primary_key=True, default=default_uuid)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    employee_code = Column(String(50), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    department = Column(String(100))  # kitchen, service, receptionist
    position = Column(String(100))  # head_chef, sous_chef, waiter
    hire_date = Column(Date)
    salary_per_hour = Column(Numeric(10, 2))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    branch = relationship("Branch", back_populates="staff")
    faces = relationship("StaffFace", back_populates="staff", cascade="all, delete-orphan")
    attendance_records = relationship("AttendanceRecord", back_populates="staff", cascade="all, delete-orphan")
    daily_attendance = relationship("DailyAttendance", back_populates="staff", cascade="all, delete-orphan")
    actions = relationship("StaffAction", back_populates="staff", cascade="all, delete-orphan")
    daily_performance = relationship("DailyStaffPerformance", back_populates="staff", cascade="all, delete-orphan")
    food_qc_results = relationship("FoodQCResult", back_populates="staff", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('branch_id', 'employee_code', name='uq_staff_branch_code'),
    )


class StaffFace(Base):
    """Khuôn mặt nhân viên (Face Embeddings)"""
    __tablename__ = "staff_faces"

    id = Column(String(36), primary_key=True, default=default_uuid)
    staff_id = Column(String(36), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    embedding_data = Column(JSON, default=list)  # Store as JSON
    image_url = Column(String(500))
    quality_score = Column(Numeric(5, 4))
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    staff = relationship("Staff", back_populates="faces")


class Shift(Base):
    """Ca làm việc"""
    __tablename__ = "shifts"

    id = Column(String(36), primary_key=True, default=default_uuid)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_night_shift = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    branch = relationship("Branch", back_populates="shifts")
    schedules = relationship("ShiftSchedule", back_populates="shift", cascade="all, delete-orphan")
    daily_attendance = relationship("DailyAttendance", back_populates="shift")

    __table_args__ = (
        UniqueConstraint('branch_id', 'name', name='uq_shift_branch_name'),
    )


class ShiftSchedule(Base):
    """Lịch làm việc của nhân viên"""
    __tablename__ = "shift_schedules"

    id = Column(String(36), primary_key=True, default=default_uuid)
    staff_id = Column(String(36), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    shift_id = Column(String(36), ForeignKey("shifts.id", ondelete="CASCADE"), nullable=False)
    work_date = Column(Date, nullable=False)
    status = Column(String(20), default="scheduled")  # scheduled, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    staff = relationship("Staff")
    shift = relationship("Shift", back_populates="schedules")

    __table_args__ = (
        UniqueConstraint('staff_id', 'shift_id', 'work_date', name='uq_shift_schedule_staff_shift_date'),
    )


# =====================================================
# 3. CAMERA & CONFIGURATION
# =====================================================

class Camera(Base):
    """Camera"""
    __tablename__ = "cameras"

    id = Column(String(36), primary_key=True, default=default_uuid)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    rtsp_url = Column(Text, nullable=False)
    # AI processed stream URL (HLS from DeepStream)
    ai_hls_url = Column(Text, nullable=True)
    location = Column(String(255))  # kitchen_entrance, counter, dining_area
    stream_type = Column(String(20), default="rtsp")  # rtsp, http, webrtc
    resolution = Column(String(20), default="1080p")
    fps = Column(Integer, default=30)
    ai_enabled = Column(JSON, default={
        "face_recognition": True,
        "har": True,
        "food_qc": True,
        "customer_flow": True
    })
    is_active = Column(Boolean, default=True)
    last_online = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    branch = relationship("Branch", back_populates="cameras")
    ai_config = relationship("CameraAIConfig", back_populates="camera", uselist=False, cascade="all, delete-orphan")
    attendance_records = relationship("AttendanceRecord", back_populates="camera")
    staff_actions = relationship("StaffAction", back_populates="camera")
    food_qc_results = relationship("FoodQCResult", back_populates="camera")
    customer_events = relationship("CustomerEvent", back_populates="camera")
    hourly_customer_stats = relationship("HourlyCustomerStats", back_populates="camera")

    __table_args__ = (
        UniqueConstraint('branch_id', 'code', name='uq_camera_branch_code'),
    )


class CameraAIConfig(Base):
    """AI Configuration cho từng camera"""
    __tablename__ = "camera_ai_configs"

    id = Column(String(36), primary_key=True, default=default_uuid)
    camera_id = Column(String(36), ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False)

    # Face Recognition settings
    face_recognition_enabled = Column(Boolean, default=True)
    face_similarity_threshold = Column(Numeric(4, 3), default=0.85)
    liveness_detection_enabled = Column(Boolean, default=True)

    # HAR settings
    har_enabled = Column(Boolean, default=True)
    idle_threshold_minutes = Column(Integer, default=5)
    actions_to_detect = Column(JSON, default=['cooking', 'washing', 'cleaning', 'idle', 'phone_usage'])

    # Food QC settings
    food_qc_enabled = Column(Boolean, default=False)
    food_similarity_threshold = Column(Numeric(4, 3), default=0.90)
    trigger_method = Column(String(20), default="motion")  # motion, manual, schedule

    # Customer Flow settings
    customer_flow_enabled = Column(Boolean, default=True)
    staff_exclusion_enabled = Column(Boolean, default=True)
    min_dwell_time_seconds = Column(Integer, default=10)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    camera = relationship("Camera", back_populates="ai_config")


# =====================================================
# 4. ATTENDANCE (Chấm công)
# =====================================================

class AttendanceRecord(Base):
    """Lịch sử chấm công"""
    __tablename__ = "attendance_records"

    id = Column(String(36), primary_key=True, default=default_uuid)
    staff_id = Column(String(36), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    camera_id = Column(String(36), ForeignKey("cameras.id", ondelete="SET NULL"))
    event_type = Column(String(20), nullable=False)  # check_in, check_out
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    embedding_id = Column(String(36), ForeignKey("staff_faces.id", ondelete="SET NULL"))
    confidence_score = Column(Numeric(5, 4))
    image_url = Column(String(500))
    is_auto_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    staff = relationship("Staff", back_populates="attendance_records")
    camera = relationship("Camera", back_populates="attendance_records")
    embedding = relationship("StaffFace")


class DailyAttendance(Base):
    """Tổng hợp chấm công theo ngày"""
    __tablename__ = "daily_attendance"

    id = Column(String(36), primary_key=True, default=default_uuid)
    staff_id = Column(String(36), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    work_date = Column(Date, nullable=False)
    shift_id = Column(String(36), ForeignKey("shifts.id", ondelete="SET NULL"))

    check_in_time = Column(Time)
    check_out_time = Column(Time)
    check_in_confidence = Column(Numeric(5, 4))
    check_out_confidence = Column(Numeric(5, 4))

    total_hours = Column(Numeric(6, 2))
    status = Column(String(20), default="present")  # present, late, absent, leave

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    staff = relationship("Staff", back_populates="daily_attendance")
    shift = relationship("Shift", back_populates="daily_attendance")

    __table_args__ = (
        UniqueConstraint('staff_id', 'work_date', name='uq_daily_attendance_staff_date'),
    )


# =====================================================
# 5. HUMAN ACTION RECOGNITION
# =====================================================

class StaffAction(Base):
    """Sự kiện hành động nhân viên"""
    __tablename__ = "staff_actions"

    id = Column(String(36), primary_key=True, default=default_uuid)
    staff_id = Column(String(36), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    camera_id = Column(String(36), ForeignKey("cameras.id", ondelete="SET NULL"))

    action_type = Column(String(50), nullable=False)
    action_label = Column(String(100))
    confidence_score = Column(Numeric(5, 4), nullable=False)

    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime)
    duration_seconds = Column(Integer)

    is_productive = Column(Boolean, default=True)
    proof_image_url = Column(String(500))
    extra_data = Column(JSON, default={})

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    staff = relationship("Staff", back_populates="actions")
    camera = relationship("Camera", back_populates="staff_actions")

    __table_args__ = (
        Index('idx_staff_actions_staff_started', 'staff_id', 'started_at'),
        Index('idx_staff_actions_started', 'started_at'),
    )


class DailyStaffPerformance(Base):
    """Tổng hợp hành động theo ngày cho từng nhân viên"""
    __tablename__ = "daily_staff_performance"

    id = Column(String(36), primary_key=True, default=default_uuid)
    staff_id = Column(String(36), ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    work_date = Column(Date, nullable=False)

    # Thời gian theo loại hành động (tính bằng giây)
    cooking_seconds = Column(Integer, default=0)
    washing_seconds = Column(Integer, default=0)
    cleaning_seconds = Column(Integer, default=0)
    idle_seconds = Column(Integer, default=0)
    phone_usage_seconds = Column(Integer, default=0)
    standing_seconds = Column(Integer, default=0)
    sitting_seconds = Column(Integer, default=0)
    other_seconds = Column(Integer, default=0)

    # Tổng hợp
    total_work_seconds = Column(Integer, default=0)
    total_idle_seconds = Column(Integer, default=0)
    productivity_rate = Column(Numeric(5, 4))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    staff = relationship("Staff", back_populates="daily_performance")

    __table_args__ = (
        UniqueConstraint('staff_id', 'work_date', name='uq_daily_performance_staff_date'),
    )


# =====================================================
# 6. FOOD QUALITY CONTROL
# =====================================================

class FoodItem(Base):
    """Danh mục món ăn"""
    __tablename__ = "food_items"

    id = Column(String(36), primary_key=True, default=default_uuid)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50))
    category = Column(String(100))  # appetizer, main, dessert, drink
    price = Column(Numeric(10, 2))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    branch = relationship("Branch", back_populates="food_items")
    master_images = relationship("FoodMasterImage", back_populates="food_item", cascade="all, delete-orphan")
    qc_results = relationship("FoodQCResult", back_populates="food_item")

    __table_args__ = (
        UniqueConstraint('branch_id', 'code', name='uq_food_item_branch_code'),
    )


class FoodMasterImage(Base):
    """Ảnh mẫu chuẩn (Master Images)"""
    __tablename__ = "food_master_images"

    id = Column(String(36), primary_key=True, default=default_uuid)
    food_item_id = Column(String(36), ForeignKey("food_items.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(500), nullable=False)
    embedding_data = Column(JSON, default=list)  # Feature embedding
    captured_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    food_item = relationship("FoodItem", back_populates="master_images")
    qc_results = relationship("FoodQCResult", back_populates="master_image")


class FoodQCResult(Base):
    """Kết quả kiểm tra QC"""
    __tablename__ = "food_qc_results"

    id = Column(String(36), primary_key=True, default=default_uuid)
    camera_id = Column(String(36), ForeignKey("cameras.id", ondelete="SET NULL"))
    food_item_id = Column(String(36), ForeignKey("food_items.id", ondelete="CASCADE"), nullable=False)

    result_status = Column(String(20), nullable=False)  # pass, fail, warning
    similarity_score = Column(Numeric(5, 4))

    # Chi tiết phân tích
    color_match = Column(Boolean)
    portion_match = Column(Boolean)
    topping_present = Column(Boolean)

    proof_image_url = Column(String(500))
    master_image_id = Column(String(36), ForeignKey("food_master_images.id", ondelete="SET NULL"))
    staff_id = Column(String(36), ForeignKey("staff.id", ondelete="SET NULL"))
    checked_by = Column(String(50), default="ai")  # ai, manual

    checked_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    camera = relationship("Camera", back_populates="food_qc_results")
    food_item = relationship("FoodItem", back_populates="qc_results")
    master_image = relationship("FoodMasterImage", back_populates="qc_results")
    staff = relationship("Staff", back_populates="food_qc_results")

    __table_args__ = (
        Index('idx_food_qc_food_checked', 'food_item_id', 'checked_at'),
        Index('idx_food_qc_checked', 'checked_at'),
    )


class DailyFoodQC(Base):
    """Tổng hợp QC theo ngày"""
    __tablename__ = "daily_food_qc"

    id = Column(String(36), primary_key=True, default=default_uuid)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    food_item_id = Column(String(36), ForeignKey("food_items.id", ondelete="CASCADE"), nullable=False)
    work_date = Column(Date, nullable=False)

    total_checks = Column(Integer, default=0)
    pass_count = Column(Integer, default=0)
    fail_count = Column(Integer, default=0)
    warning_count = Column(Integer, default=0)

    pass_rate = Column(Numeric(5, 4))
    estimated_loss = Column(Numeric(10, 2))

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    food_item = relationship("FoodItem")

    __table_args__ = (
        UniqueConstraint('branch_id', 'food_item_id', 'work_date', name='uq_daily_food_qc_branch_food_date'),
    )


# =====================================================
# 7. CUSTOMER ANALYTICS
# =====================================================

class CustomerEvent(Base):
    """Sự kiện khách hàng"""
    __tablename__ = "customer_events"

    id = Column(String(36), primary_key=True, default=default_uuid)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    camera_id = Column(String(36), ForeignKey("cameras.id", ondelete="SET NULL"))

    event_type = Column(String(20), nullable=False)  # entry, exit, dwell
    session_id = Column(String(100))
    zone = Column(String(100))  # entrance, counter, dining, exit

    detected_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    dwell_time_seconds = Column(Integer)

    # Thông tin ẩn danh (không lưu face)
    body_embedding_data = Column(JSON, default=list)  # Re-ID embedding
    clothing_color = Column(String(50))
    is_staff = Column(Boolean, default=False)

    extra_data = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    branch = relationship("Branch")
    camera = relationship("Camera", back_populates="customer_events")

    __table_args__ = (
        Index('idx_customer_events_branch_detected', 'branch_id', 'detected_at'),
        Index('idx_customer_events_detected', 'detected_at'),
        Index('idx_customer_events_session', 'session_id'),
    )


class HourlyCustomerStats(Base):
    """Tổng hợp khách hàng theo giờ"""
    __tablename__ = "hourly_customer_stats"

    id = Column(String(36), primary_key=True, default=default_uuid)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    camera_id = Column(String(36), ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False)

    stat_date = Column(Date, nullable=False)
    stat_hour = Column(Integer, nullable=False)  # 0-23

    entry_count = Column(Integer, default=0)
    exit_count = Column(Integer, default=0)
    peak_concurrent = Column(Integer, default=0)
    avg_dwell_time_seconds = Column(Integer)

    # Relationships
    branch = relationship("Branch")
    camera = relationship("Camera", back_populates="hourly_customer_stats")

    __table_args__ = (
        UniqueConstraint('branch_id', 'camera_id', 'stat_date', 'stat_hour', name='uq_hourly_stats_branch_camera_date_hour'),
    )


class DailyCustomerStats(Base):
    """Tổng hợp khách hàng theo ngày"""
    __tablename__ = "daily_customer_stats"

    id = Column(String(36), primary_key=True, default=default_uuid)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)

    stat_date = Column(Date, nullable=False)

    total_entry = Column(Integer, default=0)
    total_exit = Column(Integer, default=0)
    peak_concurrent = Column(Integer, default=0)
    avg_dwell_time_seconds = Column(Integer)

    hourly_distribution = Column(JSON)  # JSON for hourly breakdown

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    branch = relationship("Branch")

    __table_args__ = (
        UniqueConstraint('branch_id', 'stat_date', name='uq_daily_customer_stats_branch_date'),
    )


# =====================================================
# 8. REPORTS & NOTIFICATIONS
# =====================================================

class DailyReport(Base):
    """Báo cáo tổng hợp hàng ngày"""
    __tablename__ = "daily_reports"

    id = Column(String(36), primary_key=True, default=default_uuid)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    report_date = Column(Date, nullable=False)

    # Nhân sự
    total_staff = Column(Integer)
    total_work_hours = Column(Numeric(10, 2))
    total_idle_hours = Column(Numeric(10, 2))
    labor_efficiency = Column(Numeric(5, 4))

    # Tài chính
    theoretical_labor_cost = Column(Numeric(12, 2))
    actual_labor_cost = Column(Numeric(12, 2))
    savings_amount = Column(Numeric(12, 2))

    # Chất lượng
    food_qc_pass_rate = Column(Numeric(5, 4))
    failed_dish_count = Column(Integer)
    estimated_food_loss = Column(Numeric(10, 2))

    # Khách hàng
    total_customers = Column(Integer)
    peak_hour = Column(String(10))
    avg_service_time_minutes = Column(Integer)

    # Metadata
    generated_at = Column(DateTime, default=datetime.utcnow)
    generated_by = Column(String(50), default="system")

    # Relationships
    branch = relationship("Branch", back_populates="daily_reports")

    __table_args__ = (
        UniqueConstraint('branch_id', 'report_date', name='uq_daily_report_branch_date'),
    )


class Notification(Base):
    """Thông báo"""
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=default_uuid)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)

    type = Column(String(50), nullable=False)  # food_qc_fail, late_staff, system_alert
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    priority = Column(String(20), default="normal")  # low, normal, high, urgent

    # Liên kết
    reference_type = Column(String(50))  # staff, camera, food
    reference_id = Column(String(36))

    # Trạng thái
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    branch = relationship("Branch")


class NotificationSetting(Base):
    """Cấu hình thông báo"""
    __tablename__ = "notification_settings"

    id = Column(String(36), primary_key=True, default=default_uuid)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)

    notify_type = Column(String(50), nullable=False)
    channels = Column(JSON, default=list)  # ['telegram', 'email', 'push']
    is_enabled = Column(Boolean, default=True)
    threshold = Column(JSON)

    __table_args__ = (
        UniqueConstraint('branch_id', 'notify_type', name='uq_notification_setting_branch_type'),
    )


# =====================================================
# 9. AUDIT LOGS
# =====================================================

class AuditLog(Base):
    """Audit Logs"""
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=default_uuid)

    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="SET NULL"))

    action = Column(String(100), nullable=False)  # create, update, delete, login
    entity_type = Column(String(50))
    entity_id = Column(String(36))

    old_values = Column(JSON)
    new_values = Column(JSON)

    ip_address = Column(String(50))
    user_agent = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_audit_logs_entity', 'entity_type', 'entity_id'),
        Index('idx_audit_logs_user', 'user_id', 'created_at'),
        Index('idx_audit_logs_branch', 'branch_id', 'created_at'),
    )
