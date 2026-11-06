from datetime import datetime

from pydantic import BaseModel


class ReportDataResponse(BaseModel):
    id: int
    creation_date: datetime
    user_name: str
    description: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "creation_date": "2026-11-02T15:30:00.000000Z",
                "user_name": "user-example@example.com",
                "description": "Description example",
            }
        }
