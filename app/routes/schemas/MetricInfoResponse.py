from pydantic import BaseModel, RootModel


class MetricInfoResponse(BaseModel):
    type: str
    description: str


class MetricInfoListResponse(RootModel[list[MetricInfoResponse]]):
    pass
