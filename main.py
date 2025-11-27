from fastapi import FastAPI, HTTPException, status
from models import LocationEvent, ZoneStatus, ZoneTransition
from geofence import GeofenceEngine
import config

app = FastAPI(
    title="Geofence Event Processing Service",
    description="Track vehicle zone transitions based on GPS coordinates",
    version="1.0.0"
)

# Initialize geofence engine
geofence_engine = GeofenceEngine()

@app.get("/")
async def root():
    return {"message": "Geofence Event Processing Service"}

@app.post("/location-events", response_model=ZoneTransition)
async def receive_location_event(event: LocationEvent):
    """
    Receive GPS location events from vehicles and process zone transitions
    """
    try:
        config.logger.info(f"Received location event for vehicle {event.vehicle_id}")
        
        # Validate coordinates
        if not (-90 <= event.latitude <= 90) or not (-180 <= event.longitude <= 180):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid coordinates"
            )
        
        # Process the event
        transition = geofence_engine.process_location_event(event)
        
        return transition
        
    except Exception as e:
        config.logger.error(f"Error processing event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing location event"
        )

@app.get("/vehicles/{vehicle_id}/status")
async def get_vehicle_status(vehicle_id: str):
    """
    Get current zone status for a specific vehicle
    """
    try:
        status = geofence_engine.get_vehicle_status(vehicle_id)
        return status
    except Exception as e:
        config.logger.error(f"Error getting status for {vehicle_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving vehicle status"
        )

@app.get("/vehicles")
async def list_vehicles():
    """
    List all tracked vehicles and their current zones
    """
    try:
        vehicles = []
        for vehicle_id, zone in geofence_engine.vehicle_states.items():
            vehicles.append({
                "vehicle_id": vehicle_id,
                "current_zone": zone
            })
        return {"vehicles": vehicles}
    except Exception as e:
        config.logger.error(f"Error listing vehicles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error listing vehicles"
        )

@app.get("/zones")
async def list_zones():
    """
    List all defined geographic zones
    """
    return {"zones": list(config.GEO_ZONES.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)