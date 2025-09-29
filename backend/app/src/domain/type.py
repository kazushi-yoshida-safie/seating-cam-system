from pydantic import BaseModel

class RaspiData(BaseModel):
    device_id: str
    encord: str