from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class LocationEvent(BaseModel):
    vehicle_id: str = Field(..., description="Unique vehicle identifier")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    timestamp: int = Field(..., description="Unix timestamp in milliseconds")

class ZoneStatus(BaseModel):
    vehicle_id: str
    current_zone: Optional[str] = None
    previous_zone: Optional[str] = None
    last_event: Optional[LocationEvent] = None
    last_updated: Optional[int] = None

class ZoneTransition(BaseModel):
    vehicle_id: str
    from_zone: Optional[str]
    to_zone: Optional[str]
    event: LocationEvent
    transition_type: str  