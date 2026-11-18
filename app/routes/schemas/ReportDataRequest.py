from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, field_validator


class ReportDataRequest(BaseModel):
    description: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=500),
    ] = Field(description="Reason given by the user to download the report")

    @field_validator("description")
    @classmethod
    def validate_no_null_characters(cls, value: str) -> str:
        if "\x00" in value:
            raise ValueError("Text must not contain null characters")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Description example",
            }
        }
