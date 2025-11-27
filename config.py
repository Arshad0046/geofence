import logging
from typing import List, Tuple


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("geofence_service")


GEO_ZONES = {
    "downtown": [
        (40.7505, -73.9934),  
        (40.7505, -73.9834),    
        (40.7405, -73.9834),  
        (40.7405, -73.9934)   
    ],
    "airport": [
        (40.6413, -73.7781),
        (40.6413, -73.7681),
        (40.6313, -73.7681),
        (40.6313, -73.7781)
    ],
    "central_park": [
        (40.7681, -73.9814),
        (40.7681, -73.9714),
        (40.7581, -73.9714),
        (40.7581, -73.9814)
    ]
}