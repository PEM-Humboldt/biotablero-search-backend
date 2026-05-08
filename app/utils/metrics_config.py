from typing import Type, TypedDict, Union


from app.routes.schemas.MetricResponse import (
    LossPersistenceListResponse,
    CoverageResponse,
    CurrentHFResponse,
    CurrentHFAverageResponse,
    TimelineHFListResponse,
    TimelineHFSingleResponse,
    LossPersistenceSingleResponse,
    ParamoResponse,
    TropicalDryForestResponse,
    WetlandResponse,
    ProtectedAreasTypesResponse,
    ProtConnResponse,
    DPCListResponse,
    DPCSingleResponse,
)

MetricResponse = Union[
    LossPersistenceListResponse,
    CoverageResponse,
    CurrentHFResponse,
    CurrentHFAverageResponse,
    TimelineHFListResponse,
    ParamoResponse,
    TropicalDryForestResponse,
    WetlandResponse,
    ProtectedAreasTypesResponse,
    ProtConnResponse,
    DPCListResponse,
    DPCSingleResponse,
]


class MetricConfig(TypedDict):
    model: Type[MetricResponse]
    example: MetricResponse
    description: str


class MetricsConfigType(TypedDict):
    lossPersistence: MetricConfig
    coverage: MetricConfig
    currentHF: MetricConfig
    currentHF_average: MetricConfig
    timelineHF: MetricConfig
    paramo: MetricConfig
    tropicalDryForest: MetricConfig
    wetland: MetricConfig
    coverage_paramo: MetricConfig
    coverage_tropicalDryForest: MetricConfig
    coverage_wetland: MetricConfig
    protectedAreas: MetricConfig
    protConn: MetricConfig
    dpc: MetricConfig


# This config contains everything related to FastAPI and Pydantic validations
# Anything related to processing logic must be stored in database
METRICS_CONFIG: MetricsConfigType = {
    "lossPersistence": {
        "model": LossPersistenceListResponse,
        "example": LossPersistenceListResponse(
            [
                LossPersistenceSingleResponse(
                    Perdida=1971.3859302816563,
                    Persistencia=161349.158786824,
                    **{"No Bosque": 192519.67643274338},
                    id="2016-2021",
                ),
                LossPersistenceSingleResponse(
                    Perdida=1572.6614325195167,
                    Persistencia=162684.80917653913,
                    **{"No Bosque": 191582.75054079038},
                    id="2011-2015",
                ),
                LossPersistenceSingleResponse(
                    Perdida=844.3758017993621,
                    Persistencia=164716.61720378936,
                    **{"No Bosque": 190279.2281442603},
                    id="2006-2010",
                ),
                LossPersistenceSingleResponse(
                    Perdida=1164.8889557696975,
                    Persistencia=165904.73952933252,
                    **{"No Bosque": 188770.59266474683},
                    id="2000-2005",
                ),
            ]
        ),
        "description": "Forest loss and persistence",
    },
    "coverage": {
        "model": CoverageResponse,
        "example": CoverageResponse(
            id="2021",
            Natural=180000.0,
            Secundaria=25000.0,
            Transformada=12000.0,
        ),
        "description": "Land cover",
    },
    "currentHF": {
        "model": CurrentHFResponse,
        "example": CurrentHFResponse(
            id="2021",
            Natural=1971.38,
            Baja=161349.15,
            Media=192519.67,
            Alta=194312.67,
            **{"Muy Alta": 194312.67},
        ),
        "description": "Categorized human footprint index",
    },
    "currentHF_average": {
        "model": CurrentHFAverageResponse,
        "example": CurrentHFAverageResponse(
            id="2018",
            average=12.34,
        ),
        "description": "Average human footprint index",
    },
    "timelineHF": {
        "model": TimelineHFListResponse,
        "example": TimelineHFListResponse(
            [
                TimelineHFSingleResponse(
                    id="2018",
                    poligono=23.8,
                    paramo=18.4,
                    bosqueSeco=26.1,
                    humedal=21.2,
                ),
                TimelineHFSingleResponse(
                    id="2022",
                    poligono=24.5,
                    paramo=19.0,
                    bosqueSeco=26.9,
                    humedal=21.6,
                ),
            ]
        ),
        "description": "Human footprint trend by year for whole polygon and ecosystems",
    },
    "paramo": {
        "model": ParamoResponse,
        "example": ParamoResponse(
            id="Paramos30",
            paramo=25091,
        ),
        "description": "Paramo area",
    },
    "tropicalDryForest": {
        "model": TropicalDryForestResponse,
        "example": TropicalDryForestResponse(
            id="BosqueSeco30",
            bosqueSeco=1730,
        ),
        "description": "Tropical dry forest area",
    },
    "wetland": {
        "model": WetlandResponse,
        "example": WetlandResponse(
            id="Humedales30",
            humedal=9287,
        ),
        "description": "Wetland area",
    },
    "coverage_paramo": {
        "model": CoverageResponse,
        "example": CoverageResponse(
            id="2021",
            Natural=180000.0,
            Secundaria=25000.0,
            Transformada=12000.0,
        ),
        "description": "Land cover in paramos area",
    },
    "coverage_tropicalDryForest": {
        "model": CoverageResponse,
        "example": CoverageResponse(
            id="2021",
            Natural=180000.0,
            Secundaria=25000.0,
            Transformada=12000.0,
        ),
        "description": "Land cover in Tropical dry forest areas",
    },
    "coverage_wetland": {
        "model": CoverageResponse,
        "example": CoverageResponse(
            id="2021",
            Natural=180000.0,
            Secundaria=25000.0,
            Transformada=12000.0,
        ),
        "description": "Land cover in Wetland areas",
    },
    "protectedAreas": {
        "model": ProtectedAreasTypesResponse,
        "example": ProtectedAreasTypesResponse(
            id="2021",
            **{"Distritos Nacionales de Manejo Integrado": 5000.0},
            **{"Distritos Regionales de Manejo Integrado": 10000.0},
            **{"Distritos de Conservación de Suelos": 15000.0},
            **{"Parque Nacional Natural": 20000.0},
            **{"Parques Naturales Regionales": 25000.0},
            **{"Reserva Natural": 30000.0},
            **{"Reserva Natural de la Sociedad Civil": 35000.0},
            **{"Reservas Forestales Protectoras Nacionales": 500.0},
            **{"Reservas Forestales Protectoras Regionales": 3000.0},
            **{"Santuario de Fauna": 40000.0},
            **{"Santuario de Fauna y Flora": 1000.0},
            **{"Santuario de Flora": 2000.0},
            **{"Vía Parque": 1000.0},
            **{"Área Natural Única": 2000.0},
            **{"Áreas de Recreación": 45000.0},
            **{"No Protegida": 100000.0},
        ),
        "description": "Protected areas types",
    },
    "protConn": {
        "model": ProtConnResponse,
        "example": ProtConnResponse(
            id="protConn",
            prot=26.3568,
            unprot=73.6432,
            prot_conn=20.8921,
            prot_unconn=5.4647,
        ),
        "description": "Protected Areas connectivity index",
    },
    "dpc": {
        "model": DPCListResponse,
        "example": DPCListResponse(
            [
                DPCSingleResponse(
                    id="5010",
                    dpc=84.6393104,
                    pa_id=473,
                    pa_name="Serranía de los Yariguíes",
                ),
                DPCSingleResponse(
                    id="5016",
                    dpc=8.6459074,
                    pa_id=540,
                    pa_name="DRMI de los Páramos de Guantiva y La Rusia, Bosques de Roble y sus Zonas aledañas",
                ),
                DPCSingleResponse(
                    id="5008",
                    dpc=2.8891138,
                    pa_id=464,
                    pa_name="Del Humedal San Silvestre",
                ),
                DPCSingleResponse(
                    id="5020",
                    dpc=1.7596195,
                    pa_id=757,
                    pa_name="Pan de Azucar el Consuelo",
                ),
                DPCSingleResponse(
                    id="5011",
                    dpc=1.4764853,
                    pa_id=475,
                    pa_name="Del Rio Minero y sus Zonas Aledañas",
                ),
            ]
        ),
        "description": "Cconnectivity probability change index",
    },
    # TODO: implementar estas:
    # "persistenceHF": {},
    # "sciPersistenceHF": {},
    # "protectedAreas_paramo": {},
    # "protectedAreas_tropicalDryForest": {},
    # "protectedAreas_wetland": {},
    # "sciPersistenceHF_protectedAreas": {}
}

ALLOWED_METRICS = list(METRICS_CONFIG.keys())
