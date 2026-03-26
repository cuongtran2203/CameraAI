"""
Pydantic Schemas - API Request/Response Models
Camera Analyst System
"""
from __future__ import annotations

from datetime import datetime, date, time
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# =====================================================
# BASE SCHEMAS
# =====================================================

class BaseSchema(BaseModel):
    """Base schema with common config"""
    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseSchema):
    """Paginated response wrapper"""
    total: int
    page: int
    page_size: int
    data: List[Any]


# =====================================================
# AUTH SCHEMAS
# =====================================================

class UserCreate(BaseSchema):
    """Create user request"""
    branch_id: Optional[str] = None
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    role: str = "staff"


class UserUpdate(BaseSchema):
    """Update user request"""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseSchema):
    """User response"""
    id: str
    email: str
    full_name: str
    phone: Optional[str]
    avatar_url: Optional[str]
    role: str
    is_active: bool
    last_login: Optional[datetime]
    created_at: Optional[datetime] = None


class LoginRequest(BaseSchema):
    """Login request"""
    email: EmailStr
    password: str


class TokenResponse(BaseSchema):
    """Token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# =====================================================
# COMPANY & BRANCH SCHEMAS
# =====================================================

class CompanyCreate(BaseSchema):
    """Create company request"""
    name: str
    code: str
    address: Optional[str] = None
    phone: Optional[str] = None
    logo_url: Optional[str] = None


class CompanyResponse(BaseSchema):
    """Company response"""
    id: str
    name: str
    code: str
    address: Optional[str]
    phone: Optional[str]
    logo_url: Optional[str]
    is_active: bool
    created_at: datetime


class BranchCreate(BaseSchema):
    """Create branch request"""
    company_id: str
    name: str
    code: str
    address: Optional[str] = None
    timezone: str = "Asia/Ho_Chi_Minh"


class BranchResponse(BaseSchema):
    """Branch response"""
    id: str
    company_id: str
    name: str
    code: str
    address: Optional[str]
    timezone: str
    is_active: bool
    created_at: datetime


# =====================================================
# STAFF SCHEMAS
# =====================================================

class StaffCreate(BaseSchema):
    """Create staff request"""
    branch_id: str
    employee_code: str
    full_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None
    salary_per_hour: Optional[float] = None


class StaffUpdate(BaseSchema):
    """Update staff request"""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    position: Optional[str] = None
    salary_per_hour: Optional[float] = None
    is_active: Optional[bool] = None


class StaffResponse(BaseSchema):
    """Staff response"""
    id: str
    branch_id: str
    employee_code: str
    full_name: str
    phone: Optional[str]
    email: Optional[str]
    department: Optional[str]
    position: Optional[str]
    hire_date: Optional[date]
    salary_per_hour: Optional[float]
    is_active: bool
    created_at: datetime


class StaffFaceCreate(BaseSchema):
    """Add staff face request"""
    staff_id: str
    image_url: str
    embedding: List[float]
    quality_score: Optional[float] = None
    is_primary: bool = False


class StaffFaceResponse(BaseSchema):
    """Staff face response"""
    id: str
    staff_id: str
    image_url: Optional[str]
    quality_score: Optional[float]
    is_primary: bool
    created_at: datetime


# =====================================================
# SHIFT SCHEMAS
# =====================================================

class ShiftCreate(BaseSchema):
    """Create shift request"""
    branch_id: str
    name: str
    start_time: time
    end_time: time
    is_night_shift: bool = False


class ShiftResponse(BaseSchema):
    """Shift response"""
    id: str
    branch_id: str
    name: str
    start_time: time
    end_time: time
    is_night_shift: bool
    created_at: datetime


class ShiftScheduleCreate(BaseSchema):
    """Create shift schedule request"""
    staff_id: str
    shift_id: str
    work_date: date


class ShiftScheduleResponse(BaseSchema):
    """Shift schedule response"""
    id: str
    staff_id: str
    shift_id: str
    work_date: date
    status: str
    created_at: datetime


# =====================================================
# CAMERA SCHEMAS
# =====================================================

class CameraAIEnabled(BaseSchema):
    """Camera AI enabled settings"""
    face_recognition: bool = True
    har: bool = True
    food_qc: bool = True
    customer_flow: bool = True


class CameraCreate(BaseSchema):
    """Create camera request"""
    branch_id: str
    name: str
    code: str
    rtsp_url: str
    ai_hls_url: Optional[str] = None  # AI processed HLS stream
    location: Optional[str] = None
    stream_type: str = "rtsp"
    resolution: str = "1080p"
    fps: int = 30
    ai_enabled: Optional[CameraAIEnabled] = None


class CameraUpdate(BaseSchema):
    """Update camera request"""
    name: Optional[str] = None
    rtsp_url: Optional[str] = None
    ai_hls_url: Optional[str] = None  # AI processed HLS stream
    location: Optional[str] = None
    ai_enabled: Optional[CameraAIEnabled] = None
    is_active: Optional[bool] = None


class CameraResponse(BaseSchema):
    """Camera response"""
    id: str
    branch_id: str
    name: str
    code: str
    rtsp_url: str
    ai_hls_url: Optional[str] = None  # AI processed HLS stream
    location: Optional[str] = None
    stream_type: str
    resolution: Optional[str] = None
    fps: Optional[int] = None
    ai_enabled: Optional[dict] = None
    is_active: bool
    last_online: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class CameraAIConfigCreate(BaseSchema):
    """Create camera AI config request"""
    # Face Recognition
    face_recognition_enabled: bool = True
    face_similarity_threshold: float = 0.85
    liveness_detection_enabled: bool = True

    # HAR
    har_enabled: bool = True
    idle_threshold_minutes: int = 5
    actions_to_detect: Optional[List[str]] = None

    # Food QC
    food_qc_enabled: bool = False
    food_similarity_threshold: float = 0.90
    trigger_method: str = "motion"

    # Customer Flow
    customer_flow_enabled: bool = True
    staff_exclusion_enabled: bool = True
    min_dwell_time_seconds: int = 10


class CameraAIConfigResponse(BaseSchema):
    """Camera AI config response"""
    id: str
    camera_id: str
    face_recognition_enabled: bool
    face_similarity_threshold: float
    liveness_detection_enabled: bool
    har_enabled: bool
    idle_threshold_minutes: int
    actions_to_detect: List[str]
    food_qc_enabled: bool
    food_similarity_threshold: float
    trigger_method: str
    customer_flow_enabled: bool
    staff_exclusion_enabled: bool
    min_dwell_time_seconds: int
    created_at: datetime
    updated_at: datetime


# =====================================================
# ATTENDANCE SCHEMAS
# =====================================================

class AttendanceRecordCreate(BaseSchema):
    """Create attendance record request"""
    staff_id: str
    camera_id: Optional[str] = None
    event_type: str  # check_in, check_out
    timestamp: Optional[datetime] = None
    confidence_score: Optional[float] = None
    image_url: Optional[str] = None


class AttendanceRecordResponse(BaseSchema):
    """Attendance record response"""
    id: str
    staff_id: str
    camera_id: Optional[str]
    event_type: str
    timestamp: datetime
    confidence_score: Optional[float]
    image_url: Optional[str]
    is_auto_generated: bool
    created_at: datetime


class DailyAttendanceResponse(BaseSchema):
    """Daily attendance response"""
    id: str
    staff_id: str
    work_date: date
    shift_id: Optional[str]
    check_in_time: Optional[time]
    check_out_time: Optional[time]
    total_hours: Optional[float]
    status: str


# =====================================================
# STAFF ACTION SCHEMAS
# =====================================================

class StaffActionCreate(BaseSchema):
    """Create staff action request"""
    staff_id: str
    camera_id: Optional[str] = None
    action_type: str
    action_label: Optional[str] = None
    confidence_score: float
    started_at: datetime
    ended_at: Optional[datetime] = None
    is_productive: bool = True


class StaffActionResponse(BaseSchema):
    """Staff action response"""
    id: str
    staff_id: str
    camera_id: Optional[str]
    action_type: str
    action_label: Optional[str]
    confidence_score: float
    started_at: datetime
    ended_at: Optional[datetime]
    duration_seconds: Optional[int]
    is_productive: bool
    created_at: datetime


class DailyPerformanceResponse(BaseSchema):
    """Daily staff performance response"""
    id: str
    staff_id: str
    work_date: date
    cooking_seconds: int
    washing_seconds: int
    cleaning_seconds: int
    idle_seconds: int
    phone_usage_seconds: int
    standing_seconds: int
    sitting_seconds: int
    other_seconds: int
    total_work_seconds: int
    total_idle_seconds: int
    productivity_rate: Optional[float]


# =====================================================
# FOOD QC SCHEMAS
# =====================================================

class FoodItemCreate(BaseSchema):
    """Create food item request"""
    branch_id: str
    name: str
    code: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None


class FoodItemResponse(BaseSchema):
    """Food item response"""
    id: str
    branch_id: str
    name: str
    code: Optional[str]
    category: Optional[str]
    price: Optional[float]
    is_active: bool
    created_at: datetime


class FoodMasterImageCreate(BaseSchema):
    """Create master image request"""
    food_item_id: str
    image_url: str
    embedding: Optional[List[float]] = None
    notes: Optional[str] = None


class FoodMasterImageResponse(BaseSchema):
    """Master image response"""
    id: str
    food_item_id: str
    image_url: str
    notes: Optional[str]
    is_active: bool
    created_at: datetime


class FoodQCResultResponse(BaseSchema):
    """Food QC result response"""
    id: str
    camera_id: Optional[str]
    food_item_id: str
    result_status: str
    similarity_score: Optional[float]
    color_match: Optional[bool]
    portion_match: Optional[bool]
    topping_present: Optional[bool]
    proof_image_url: Optional[str]
    staff_id: Optional[str]
    checked_by: str
    checked_at: datetime


# =====================================================
# CUSTOMER ANALYTICS SCHEMAS
# =====================================================

class CustomerEventResponse(BaseSchema):
    """Customer event response"""
    id: str
    branch_id: str
    camera_id: Optional[str]
    event_type: str
    session_id: Optional[str]
    zone: Optional[str]
    detected_at: datetime
    dwell_time_seconds: Optional[int]
    clothing_color: Optional[str]
    is_staff: bool


class HourlyCustomerStatsResponse(BaseSchema):
    """Hourly customer stats response"""
    id: str
    branch_id: str
    camera_id: str
    stat_date: date
    stat_hour: int
    entry_count: int
    exit_count: int
    peak_concurrent: int
    avg_dwell_time_seconds: Optional[int]


class DailyCustomerStatsResponse(BaseSchema):
    """Daily customer stats response"""
    id: str
    branch_id: str
    stat_date: date
    total_entry: int
    total_exit: int
    peak_concurrent: int
    avg_dwell_time_seconds: Optional[int]
    hourly_distribution: Optional[dict]


# =====================================================
# DASHBOARD SCHEMAS
# =====================================================

class DashboardStatsResponse(BaseSchema):
    """Dashboard stats response"""
    timestamp: datetime
    staff: dict
    actions: dict
    food_qc: dict
    customers: dict


class StaffSummary(BaseSchema):
    """Staff summary for dashboard"""
    total_online: int
    total_scheduled: int
    attendance_rate: float


class ActionSummary(BaseSchema):
    """Action summary for dashboard"""
    productive_count: int
    idle_count: int
    top_actions: List[dict]


class FoodQCSummary(BaseSchema):
    """Food QC summary for dashboard"""
    total_checked: int
    pass_count: int
    fail_count: int
    warning_count: int
    pass_rate: float


class CustomerSummary(BaseSchema):
    """Customer summary for dashboard"""
    current_in_store: int
    entry_today: int
    avg_dwell_time_minutes: int
    peak_hour: Optional[str]


# =====================================================
# REPORT SCHEMAS
# =====================================================

class DailyReportResponse(BaseSchema):
    """Daily report response"""
    id: str
    branch_id: str
    report_date: date

    # Staff
    total_staff: Optional[int]
    total_work_hours: Optional[float]
    total_idle_hours: Optional[float]
    labor_efficiency: Optional[float]

    # Finance
    theoretical_labor_cost: Optional[float]
    actual_labor_cost: Optional[float]
    savings_amount: Optional[float]

    # Quality
    food_qc_pass_rate: Optional[float]
    failed_dish_count: Optional[int]
    estimated_food_loss: Optional[float]

    # Customers
    total_customers: Optional[int]
    peak_hour: Optional[str]
    avg_service_time_minutes: Optional[int]

    generated_at: datetime


# =====================================================
# IMAGE COMPARE SCHEMAS
# =====================================================

class ImageAnalysisSchema(BaseSchema):
    """Image analysis result from AI"""
    dense_caption: str
    ingredients: List[str] = []


class ImageCompareResponse(BaseSchema):
    """Image compare response from AI service"""
    score: float = Field(description="Final similarity score (0.0 - 1.0)")
    base_score: float = Field(description="Visual similarity score from embedding")
    ingredient_score: float = Field(description="Ingredient similarity score")
    is_match: bool = Field(description="True if score >= threshold (0.75)")
    image_a: ImageAnalysisSchema
    image_b: ImageAnalysisSchema
    status: Optional[str] = Field(
        default=None,
        description="'pass' if is_match, else 'fail'"
    )


# =====================================================
# FOOD SEARCH (RETRIEVAL) SCHEMAS
# =====================================================

class FoodSearchItem(BaseSchema):
    """A single search result item from AI retrieval"""
    id: str = Field(description="Image ID in database")
    image_path: str = Field(description="Path to matched image")
    description: str = Field(description="AI description of the matched food")
    ingredients: List[str] = Field(default_factory=list)
    base_score: float = Field(description="Visual embedding similarity (0.0 - 1.0)")
    ingredient_score: float = Field(description="Ingredient similarity (0.0 - 1.0)")
    score: float = Field(description="Final combined score (0.0 - 1.0)")


class FoodSearchResponse(BaseSchema):
    """Full search/retrieval response from AI service"""
    query_description: str = Field(description="AI description of uploaded image")
    query_ingredients: List[str] = Field(default_factory=list)
    top_k: List[FoodSearchItem] = Field(default_factory=list)


# =====================================================
# NOTIFICATION SCHEMAS
# =====================================================

class NotificationCreate(BaseSchema):
    """Create notification request"""
    branch_id: str
    type: str
    title: str
    message: str
    priority: str = "normal"
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None


class NotificationResponse(BaseSchema):
    """Notification response"""
    id: str
    branch_id: str
    type: str
    title: str
    message: str
    priority: str
    reference_type: Optional[str]
    reference_id: Optional[str]
    is_read: bool
    read_at: Optional[datetime]
    created_at: datetime


# =====================================================
# KAFKA MESSAGE SCHEMAS
# =====================================================

class KafkaCommand(BaseSchema):
    """Kafka command message"""
    message_id: str
    command: str  # START_STREAM, STOP_STREAM, RESTART
    camera_id: str
    timestamp: datetime
    options: dict


class AIDetectionBase(BaseSchema):
    """Base AI detection message"""
    timestamp: datetime
    camera_id: str


class FaceDetection(AIDetectionBase):
    """Face detection message"""
    detections: List[dict] = []


class ActionDetection(AIDetectionBase):
    """Action detection message"""
    actions: List[dict] = []


class FoodDetection(AIDetectionBase):
    """Food detection message"""
    detections: List[dict] = []


class CustomerDetection(AIDetectionBase):
    """Customer detection message"""
    events: List[dict] = []


class AIProcessedMessage(AIDetectionBase):
    """Aggregated AI processed message for dashboard"""
    summary: dict = {}
