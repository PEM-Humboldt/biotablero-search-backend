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


class AverageResponse(BaseMetricResult):
    """
    Response model the average of a cropped collection in a given year.
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


class ProtectedAreasTypesResponse(BaseMetricResult):
    """
    Response model for protected areas types in a given year.
    """

    Distritos_Nacionales_Manejo_Integrado: float = Field(
        default=0.0, alias="Distritos Nacionales de Manejo Integrado"
    )
    Distritos_Regionales_Manejo_Integrado: float = Field(
        default=0.0, alias="Distritos Regionales de Manejo Integrado"
    )
    Distritos_Conservacion_Suelos: float = Field(
        default=0.0, alias="Distritos de Conservación de Suelos"
    )
    Parque_Nacional_Natural: float = Field(
        default=0.0, alias="Parque Nacional Natural"
    )
    Parques_Naturales_Regional: float = Field(
        default=0.0, alias="Parques Naturales Regionales"
    )
    Reserva_Natural: float = Field(default=0.0, alias="Reserva Natural")
    Reserva_Natural_Sociedad_Civil: float = Field(
        default=0.0, alias="Reserva Natural de la Sociedad Civil"
    )
    Reservas_Forestales_Protectoras_Nacionales: float = Field(
        default=0.0, alias="Reservas Forestales Protectoras Nacionales"
    )
    Reservas_Forestales_Protectoras_Regionales: float = Field(
        default=0.0, alias="Reservas Forestales Protectoras Regionales"
    )
    Santuario_Fauna: float = Field(default=0.0, alias="Santuario de Fauna")
    Santuario_Fauna_Flora: float = Field(
        default=0.0, alias="Santuario de Fauna y Flora"
    )
    Santuario_Flora: float = Field(default=0.0, alias="Santuario de Flora")
    Via_Parque: float = Field(default=0.0, alias="Vía Parque")
    Area_Natural_Unica: float = Field(default=0.0, alias="Área Natural Única")
    Areas_Recreacion: float = Field(default=0.0, alias="Áreas de Recreación")
    No_Protegida: float = Field(default=0.0, alias="No Protegida")


class ProtConnResponse(BaseMetricResult):
    prot: float
    unprot: float
    prot_conn: float
    prot_unconn: float


class DPCSingleResponse(BaseMetricResult):
    dpc: float
    pa_id: int
    pa_name: str


class DPCListResponse(RootModel[list[DPCSingleResponse]]):
    pass


class RecordGapsResponse(BaseMetricResult):
    """
    Response model for record gaps frequency metric in a given year.
    """

    frequency: list[int]
    bin_edges: list[float]
