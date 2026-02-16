from app.models.models import Collection, Metric, MetricCollection
from datetime import datetime
from enum import Enum
from typing import List, Optional


class CollectionEnum(Enum):
    HUELLA_HUMANA_CLASIFICADA = "HuellaHumanaClasificada"
    HUELLA_HUMANA_CONTINUA = "HuellaHumanaContinua"
    INDICE_VACIOS_INFORMACION = "IndiceVaciosInformacion"
    # TODO: Actualizar los nombres correctos de las colleciones
    PERDIDA_PERSISTENCIA = "PerdidaYPersistencia"
    COBERTURA = "Coberturas"
    PARAMO = "EcosistremasEstrategicos"
    BOSQUE_SECO_TROPICAL = "EcosistremasEstrategicos"
    HUMEDAL = "EcosistremasEstrategicos"


class OperationEnum(Enum):
    AREA_SINGLE_COLLECTION = "AREA_SINGLE-COLLECTION"
    AREA_SINGLE_COLLECTION_ALL_ITEMS = "AREA_SINGLE-COLLECTION_ALL-ITEMS"
    AREA_TWO_COLLECTIONS = "AREA_TWO-COLLECTIONS"
    AVERAGE_SINGLE_COLLECTION = "AVERAGE_SINGLE-COLLECTION"
    AVERAGE_MULTIPLE_COLLECTION_ALL_ITEMS = (
        "AVERAGE_MULTIPLE-COLLECTION_ALL-ITEMS"
    )
    PA = "PA"
    PA_SINGLE_COLLECTION = "PA_SINGLE-COLLECTION"
    PA_SINGLE_COLLECTION_FILTERED = "PA_SINGLE-COLLECTION-FILTERED"


class MetricEnum(Enum):
    COVERAGE = (
        "coverage",
        OperationEnum.AREA_SINGLE_COLLECTION,
        CollectionEnum.COBERTURA,
    )
    PARAMO = ("paramo", OperationEnum.AREA_SINGLE_COLLECTION)
    TROPICAL_DRY_FOREST = (
        "tropicalDryForest",
        OperationEnum.AREA_SINGLE_COLLECTION,
    )
    WETLAND = ("wetland", OperationEnum.AREA_SINGLE_COLLECTION)
    CURRENTHF = (
        "currentHF",
        OperationEnum.AREA_SINGLE_COLLECTION,
        CollectionEnum.HUELLA_HUMANA_CLASIFICADA,
    )
    PERSISTENCEHF = ("persistenceHF", OperationEnum.AREA_SINGLE_COLLECTION)
    SCIPERSISTENCEHF = (
        "sciPersistenceHF",
        OperationEnum.AREA_SINGLE_COLLECTION,
    )
    LOSSPERSISTENCE = (
        "lossPersistence",
        OperationEnum.AREA_SINGLE_COLLECTION_ALL_ITEMS,
        CollectionEnum.PERDIDA_PERSISTENCIA,
    )
    COVERAGE_PARAMO = (
        "coverage_paramo",
        OperationEnum.AREA_TWO_COLLECTIONS,
        CollectionEnum.COBERTURA,
        [CollectionEnum.PARAMO],
    )
    COVERAGE_TROPICAL_DRY_FOREST = (
        "coverage_tropicalDryForest",
        OperationEnum.AREA_TWO_COLLECTIONS,
        CollectionEnum.COBERTURA,
        [CollectionEnum.BOSQUE_SECO_TROPICAL],
    )
    COVERAGE_WETLAND = (
        "coverage_wetland",
        OperationEnum.AREA_TWO_COLLECTIONS,
        CollectionEnum.COBERTURA,
        [CollectionEnum.HUMEDAL],
    )
    CURRENTHF_AVERAGE = (
        "currentHF_average",
        OperationEnum.AVERAGE_SINGLE_COLLECTION,
        CollectionEnum.HUELLA_HUMANA_CONTINUA,
    )
    TIMELINEHF = (
        "timelineHF",
        OperationEnum.AVERAGE_MULTIPLE_COLLECTION_ALL_ITEMS,
        CollectionEnum.HUELLA_HUMANA_CONTINUA,
        [
            CollectionEnum.PARAMO,
            CollectionEnum.BOSQUE_SECO_TROPICAL,
            CollectionEnum.HUMEDAL,
        ],
    )
    PROTECTED_AREAS = ("protectedAreas", OperationEnum.PA)
    PROTECTED_AREAS_PARAMO = (
        "protectedAreas_paramo",
        OperationEnum.PA_SINGLE_COLLECTION,
    )
    PROTECTED_AREAS_TROPICAL_DRY_FOREST = (
        "protectedAreas_tropicalDryForest",
        OperationEnum.PA_SINGLE_COLLECTION,
    )
    PROTECTED_AREAS_WETLAND = (
        "protectedAreas_wetland",
        OperationEnum.PA_SINGLE_COLLECTION,
    )
    SCIPERSISTENCEHF_PROTECTED_AREAS = (
        "sciPersistenceHF_protectedAreas",
        OperationEnum.PA_SINGLE_COLLECTION_FILTERED,
    )

    def __init__(
        self,
        metric_name: str,
        operation: OperationEnum,
        main_collection: Optional[CollectionEnum] = None,
        sec_collections: Optional[List[CollectionEnum]] = None,
    ):
        self.metric_name = metric_name
        self.operation_type = operation.value
        self.main_collection = main_collection
        self.sec_collections = sec_collections


collections_dict = {}
metrics_dict = {}


async def seed_collections_and_metrics():
    await Collection.all().delete()
    await Metric.all().delete()
    await MetricCollection.all().delete()

    if not await Collection.exists():
        now = datetime.now()
        for col in CollectionEnum:
            new_collection = Collection(
                name=col.value,
                updated_at=now,
            )
            await new_collection.save()
            collections_dict[col.value] = new_collection

    if not await Metric.exists():
        for metric in MetricEnum:

            new_metric = Metric(
                name=metric.metric_name,
                operation_type=metric.operation_type,
            )
            await new_metric.save()

            if metric.main_collection:
                await MetricCollection.create(
                    is_primary=True,
                    metric=new_metric,
                    collection=collections_dict[metric.main_collection.value],
                )
            if metric.sec_collections:
                for sec_col in metric.sec_collections:
                    await MetricCollection.create(
                        is_primary=False,
                        metric=new_metric,
                        collection=collections_dict[sec_col.value],
                    )
