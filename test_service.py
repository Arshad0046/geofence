import pytest
from fastapi.testclient import TestClient
from main import app
from models import LocationEvent

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_location_event_inside_zone():
    # Test point inside downtown zone
    event = {
        "vehicle_id": "taxi_001",
        "latitude": 40.7455,
        "longitude": -73.9884,
        "timestamp": 1700000000000
    }
    
    response = client.post("/location-events", json=event)
    assert response.status_code == 200
    data = response.json()
    assert data["vehicle_id"] == "taxi_001"
    assert data["to_zone"] == "downtown"
    assert data["transition_type"] == "ENTER"

def test_location_event_outside_zones():
    # Test point outside any zone
    event = {
        "vehicle_id": "taxi_002", 
        "latitude": 40.7000,
        "longitude": -74.0000,
        "timestamp": 1700000000000
    }
    
    response = client.post("/location-events", json=event)
    assert response.status_code == 200
    data = response.json()
    assert data["to_zone"] is None

def test_vehicle_status():
    # First send an event
    event = {
        "vehicle_id": "taxi_003",
        "latitude": 40.7455,
        "longitude": -73.9884, 
        "timestamp": 1700000000000
    }
    client.post("/location-events", json=event)
    
    # Then check status
    response = client.get("/vehicles/taxi_003/status")
    assert response.status_code == 200
    data = response.json()
    assert data["vehicle_id"] == "taxi_003"
    assert data["current_zone"] == "downtown"

def test_invalid_coordinates():
    event = {
        "vehicle_id": "taxi_004",
        "latitude": 100.0,  # Invalid latitude
        "longitude": -73.9884,
        "timestamp": 1700000000000
    }
    
    response = client.post("/location-events", json=event)
    assert response.status_code == 400