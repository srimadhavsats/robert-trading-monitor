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
