from typing import List, Tuple, Optional, Dict, Any
from models import LocationEvent, ZoneTransition
import config

class GeofenceEngine:
    def __init__(self):
        self.zones = config.GEO_ZONES
        self.vehicle_states: Dict[str, str] = {}  # vehicle_id -> current_zone
        
    def point_in_polygon(self, point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
        """Ray casting algorithm to check if point is inside polygon"""
        lat, lon = point
        inside = False
        
        j = len(polygon) - 1
        for i in range(len(polygon)):
            lat_i, lon_i = polygon[i]
            lat_j, lon_j = polygon[j]
            
            if ((lon_i > lon) != (lon_j > lon)) and \
               (lat < (lat_j - lat_i) * (lon - lon_i) / (lon_j - lon_i) + lat_i):
                inside = not inside
            j = i
            
        return inside
    
    def detect_zone(self, event: LocationEvent) -> Optional[str]:
        """Detect which zone the vehicle is currently in"""
        point = (event.latitude, event.longitude)
        
        for zone_name, polygon in self.zones.items():
            if self.point_in_polygon(point, polygon):
                return zone_name
                
        return None
    
    def process_location_event(self, event: LocationEvent) -> ZoneTransition:
        """Process location event and detect zone transitions"""
        current_zone = self.detect_zone(event)
        previous_zone = self.vehicle_states.get(event.vehicle_id)
        
        # Determine transition type
        if current_zone != previous_zone:
            if current_zone is None and previous_zone is not None:
                transition_type = "EXIT"
            elif current_zone is not None and previous_zone is None:
                transition_type = "ENTER"
            else:
                transition_type = "TRANSITION"
        else:
            transition_type = "NONE"
        
        # Update vehicle state
        self.vehicle_states[event.vehicle_id] = current_zone
        
        config.logger.info(
            f"Vehicle {event.vehicle_id}: {previous_zone} -> {current_zone} "
            f"({transition_type})"
        )
        
        return ZoneTransition(
            vehicle_id=event.vehicle_id,
            from_zone=previous_zone,
            to_zone=current_zone,
            event=event,
            transition_type=transition_type
        )
    
    def get_vehicle_status(self, vehicle_id: str) -> Dict[str, Any]:
        """Get current status for a vehicle"""
        current_zone = self.vehicle_states.get(vehicle_id)
        
        return {
            "vehicle_id": vehicle_id,
            "current_zone": current_zone,
            "is_in_zone": current_zone is not None
        }