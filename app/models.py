from pydantic import BaseModel

class Event(BaseModel):

    event_id: str
    store_id: str
    camera_id: str
    visitor_id: str

    event_type: str

    timestamp: str

    zone_id: str | None

    dwell_ms: int

    is_staff: bool

    confidence: float

    metadata: dict
