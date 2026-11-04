from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, field_validator


class ReportDataRequest(BaseModel):
    description: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=500),
    ] = Field(description="Reason given by the user to download the report")
    data: (
        Annotated[
            str,
            StringConstraints(strip_whitespace=True, max_length=280),
        ]
        | None
    ) = Field(
        default=None,
        description="Additional data about the downloaded report",
    )

    @field_validator("description", "data")
    @classmethod
    def validate_no_null_characters(cls, value: str | None) -> str | None:
        if value is not None and "\x00" in value:
            raise ValueError("Text must not contain null characters")
        return value

    @field_validator("data")
    @classmethod
    def empty_data_to_none(cls, value: str | None) -> str | None:
        return value or None

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Description example",
                "data": "Data example",
            }
        }
