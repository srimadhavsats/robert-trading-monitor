# ====================================================================
# SATS Sentinel v4.1 - API Data Schemas & Validation Models
# ====================================================================
from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    """Formal data contract for system gateway health diagnostics."""

    status: str = Field(..., description="The operational state of the Sentinel engine")
    message: str = Field(
        ..., description="Detailed availability status of the streaming data oracle"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "Sentinel v4.1 Active",
                "message": "Oracle engine is operational and ready for stream requests",
            }
        }


class ErrorResponse(BaseModel):
    """Standardized error contract for consistent API exception handling."""

    error: str = Field(..., description="The error classification code or status title")
    details: str = Field(
        ..., description="Human-readable exception details and debugging context"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Upstream Gateway Error",
                "details": "The remote exchange mirror connection timed out after 10.0 seconds.",
            }
        }
