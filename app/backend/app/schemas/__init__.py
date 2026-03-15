# Schemas package
from app.schemas.schemas import (
    # Base
    BaseSchema, PaginatedResponse,
    # Auth
    LoginRequest, TokenResponse, UserCreate, UserUpdate, UserResponse,
    # Company & Branch
    CompanyCreate, CompanyResponse, BranchCreate, BranchResponse,
    # Staff
    StaffCreate, StaffUpdate, StaffResponse, StaffFaceCreate, StaffFaceResponse,
    # Shift
    ShiftCreate, ShiftResponse, ShiftScheduleCreate, ShiftScheduleResponse,
    # Camera
    CameraCreate, CameraUpdate, CameraResponse,
    CameraAIConfigCreate, CameraAIConfigResponse,
    # Attendance
    AttendanceRecordCreate, AttendanceRecordResponse, DailyAttendanceResponse,
    # Staff Action
    StaffActionCreate, StaffActionResponse, DailyPerformanceResponse,
    # Food QC
    FoodItemCreate, FoodItemResponse,
    FoodMasterImageCreate, FoodMasterImageResponse,
    FoodQCResultResponse,
    # Customer
    CustomerEventResponse, HourlyCustomerStatsResponse, DailyCustomerStatsResponse,
    # Dashboard
    DashboardStatsResponse, StaffSummary, ActionSummary, FoodQCSummary, CustomerSummary,
    # Report
    DailyReportResponse,
    # Notification
    NotificationCreate, NotificationResponse,
    # Kafka
    KafkaCommand, FaceDetection, ActionDetection, FoodDetection, CustomerDetection, AIProcessedMessage
)

__all__ = [
    "BaseSchema", "PaginatedResponse",
    "LoginRequest", "TokenResponse", "UserCreate", "UserUpdate", "UserResponse",
    "CompanyCreate", "CompanyResponse", "BranchCreate", "BranchResponse",
    "StaffCreate", "StaffUpdate", "StaffResponse", "StaffFaceCreate", "StaffFaceResponse",
    "ShiftCreate", "ShiftResponse", "ShiftScheduleCreate", "ShiftScheduleResponse",
    "CameraCreate", "CameraUpdate", "CameraResponse",
    "CameraAIConfigCreate", "CameraAIConfigResponse",
    "AttendanceRecordCreate", "AttendanceRecordResponse", "DailyAttendanceResponse",
    "StaffActionCreate", "StaffActionResponse", "DailyPerformanceResponse",
    "FoodItemCreate", "FoodItemResponse",
    "FoodMasterImageCreate", "FoodMasterImageResponse",
    "FoodQCResultResponse",
    "CustomerEventResponse", "HourlyCustomerStatsResponse", "DailyCustomerStatsResponse",
    "DashboardStatsResponse", "StaffSummary", "ActionSummary", "FoodQCSummary", "CustomerSummary",
    "DailyReportResponse",
    "NotificationCreate", "NotificationResponse",
    "KafkaCommand", "FaceDetection", "ActionDetection", "FoodDetection", "CustomerDetection", "AIProcessedMessage"
]
