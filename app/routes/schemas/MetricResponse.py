from pydantic import BaseModel, Field, RootModel


class BaseMetricResult(BaseModel):
    id: str

    model_config = {
        "extra": "forbid",
        "populate_by_name": True,
    }


class LossPersistenceSingleResponse(BaseMetricResult):
    """
    Response model for forest loss and persistence metrics in a given period.
    """

    Perdida: float
    Persistencia: float
    No_Bosque: float = Field(alias="No Bosque")


class LossPersistenceListResponse(
    RootModel[list[LossPersistenceSingleResponse]]
):
    pass


class CoverageResponse(BaseMetricResult):
    """
    Response model for land cover metrics in a given year.
    """

    Natural: float
    Secundaria: float
    Transformada: float


class CurrentHFResponse(BaseMetricResult):
    """
    Response model for Human Footprint metrics in a given year.
    """

    Natural: float
    Baja: float
    Media: float
    Alta: float
    Muy_Alta: float = Field(alias="Muy Alta")


class CurrentHFAverageResponse(BaseMetricResult):
    """
    Response model for Human Footprint average in a given year.
    """

    average: float


class ParamoResponse(BaseMetricResult):
    """
    Response model for paramos area in a given year.
    """

    paramo: float


class TropicalDryForestResponse(BaseMetricResult):
    """
    Response model for tropical dry forest area in a given year.
    """

    bosqueSeco: float


class WetlandResponse(BaseMetricResult):
    """
    Response model for wetland area in a given year.
    """

    humedal: float
