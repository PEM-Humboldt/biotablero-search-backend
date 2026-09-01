from app.models.models import (
    Collection,
    Metric,
    MetricCollection,
    MetricIndicator,
)
from enum import Enum
from typing import Dict, List, Optional


class CollectionEnum(Enum):
    HUELLA_HUMANA_CLASIFICADA = "HuellaHumanaClasificada"
    HUELLA_HUMANA_CONTINUA = "HuellaHumanaContinua"
    INDICE_VACIOS_INFORMACION = "IndiceVaciosInformacion"
    PERDIDA_PERSISTENCIA = "PerdidaYPersistencia"
    COBERTURA = "Coberturas"
    PARAMO = "Paramos"
    BOSQUE_SECO_TROPICAL = "BosqueSeco"
    HUMEDAL = "Humedales"
    AREAS_PROTEGIDAS = "AreasProtegidas"
    RIQUEZA_OBSERVADA = "RiquezaObservada"
    RIQUEZA_OBSERVADA_ANFIBIOS = "RiquezaObservadaAnfibios"
    RIQUEZA_OBSERVADA_AVES = "RiquezaObservadaAves"
    RIQUEZA_OBSERVADA_HONGOS = "RiquezaObservadaHongos"
    RIQUEZA_OBSERVADA_INVERTEBRADOS = "RiquezaObservadaInvertebrados"
    RIQUEZA_OBSERVADA_MAMIFEROS = "RiquezaObservadaMamiferos"
    RIQUEZA_OBSERVADA_REPTILES = "RiquezaObservadaReptiles"
    RIQUEZA_OBSERVADA_PLANTAS = "RiquezaObservadaPlantas"
    RIQUEZA_OBSERVADA_PECES = "RiquezaObservadaPeces"


class IndicatorEnum(Enum):
    PROT_CONN = "prot_conn"
    DPC = "dpc"
    STATSONSPECIES = "statsOnSpecies"


class OperationEnum(Enum):
    AREA_SINGLE_COLLECTION = "AREA_SINGLE-COLLECTION"
    AREA_SINGLE_COLLECTION_ALL_ITEMS = "AREA_SINGLE-COLLECTION_ALL-ITEMS"
    AREA_TWO_COLLECTIONS = "AREA_TWO-COLLECTIONS"
    AVERAGE_SINGLE_COLLECTION = "AVERAGE_SINGLE-COLLECTION"
    AVERAGE_MULTIPLE_COLLECTION_ALL_ITEMS = (
        "AVERAGE_MULTIPLE-COLLECTION_ALL-ITEMS"
    )
    AREA_CATEGORIES_SINGLE_COLLECTION = "AREA_CATEGORIES_SINGLE-COLLECTION"
    AREA_CATEGORIES_TWO_COLLECTIONS = "AREA_CATEGORIES_TWO-COLLECTIONS"
    AREA_CATEGORIES_SINGLE_COLLECTION_FILTERED = (
        "AREA_CATEGORIES_SINGLE-COLLECTION_FILTERED"
    )
    TABLE_PRECALCULATED = "TABLE_PRECALCULATED"
    SELECTED_TABLE_PRECALCULATED = "SELECTED-TABLE_PRECALCULATED"
    FREQUENCY_SINGLE_COLLECTION = "FREQUENCY_SINGLE-COLLECTION"
    FREQUENCY_SINGLE_SELECTED_COLLECTION = (
        "FREQUENCY_SINGLE-SELECTED-COLLECTION"
    )


class MetricEnum(Enum):
    COVERAGE = (
        "coverage",
        OperationEnum.AREA_SINGLE_COLLECTION,
        CollectionEnum.COBERTURA,
        None,
        None,
        "coberturas-variacion-superficie",
    )
    PARAMO = (
        "paramo",
        OperationEnum.AREA_SINGLE_COLLECTION,
        CollectionEnum.PARAMO,
    )
    TROPICAL_DRY_FOREST = (
        "tropicalDryForest",
        OperationEnum.AREA_SINGLE_COLLECTION,
        CollectionEnum.BOSQUE_SECO_TROPICAL,
    )
    WETLAND = (
        "wetland",
        OperationEnum.AREA_SINGLE_COLLECTION,
        CollectionEnum.HUMEDAL,
    )
    CURRENTHF = (
        "currentHF",
        OperationEnum.AREA_SINGLE_COLLECTION,
        CollectionEnum.HUELLA_HUMANA_CLASIFICADA,
    )
    PERSISTENCEHF = (
        "persistenceHF",
        OperationEnum.AREA_SINGLE_COLLECTION,
    )
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
    PROTECTED_AREAS = (
        "protectedAreas",
        OperationEnum.AREA_CATEGORIES_SINGLE_COLLECTION,
        CollectionEnum.AREAS_PROTEGIDAS,
    )
    PROTECTED_AREAS_PARAMO = (
        "protectedAreas_paramo",
        OperationEnum.AREA_CATEGORIES_TWO_COLLECTIONS,
        CollectionEnum.AREAS_PROTEGIDAS,
        [CollectionEnum.PARAMO],
    )

    PROTECTED_AREAS_TROPICAL_DRY_FOREST = (
        "protectedAreas_tropicalDryForest",
        OperationEnum.AREA_CATEGORIES_TWO_COLLECTIONS,
        CollectionEnum.AREAS_PROTEGIDAS,
        [CollectionEnum.BOSQUE_SECO_TROPICAL],
    )
    PROTECTED_AREAS_WETLAND = (
        "protectedAreas_wetland",
        OperationEnum.AREA_CATEGORIES_TWO_COLLECTIONS,
        CollectionEnum.AREAS_PROTEGIDAS,
        [CollectionEnum.HUMEDAL],
    )
    SCIPERSISTENCEHF_PROTECTED_AREAS = (
        "sciPersistenceHF_protectedAreas",
        OperationEnum.AREA_CATEGORIES_SINGLE_COLLECTION_FILTERED,
    )
    PROT_CONN = (
        "protConn",
        OperationEnum.TABLE_PRECALCULATED,
        None,
        None,
        IndicatorEnum.PROT_CONN,
        None,
    )
    DPC = (
        "dpc",
        OperationEnum.TABLE_PRECALCULATED,
        None,
        None,
        IndicatorEnum.DPC,
        None,
    )
    RECORDGAPS = (
        "recordGaps",
        OperationEnum.FREQUENCY_SINGLE_COLLECTION,
        CollectionEnum.INDICE_VACIOS_INFORMACION,
        None,
        None,
        "indice-de-vacios",
    )
    CURRENTRECORDSGAPS_AVERAGE = (
        "currentRecordsGaps_average",
        OperationEnum.AVERAGE_SINGLE_COLLECTION,
        CollectionEnum.INDICE_VACIOS_INFORMACION,
    )
    STATS_ON_SPECIES = (
        "statsOnSpecies",
        OperationEnum.SELECTED_TABLE_PRECALCULATED,
        None,
        None,
        IndicatorEnum.STATSONSPECIES,
        None,
        True,
        True,
    )
    RICHNESS = (
        "richness",
        OperationEnum.FREQUENCY_SINGLE_SELECTED_COLLECTION,
        CollectionEnum.RIQUEZA_OBSERVADA,
        None,
        None,
        None,
        False,
        False,
        {
            "anfibios": CollectionEnum.RIQUEZA_OBSERVADA_ANFIBIOS,
            "aves": CollectionEnum.RIQUEZA_OBSERVADA_AVES,
            "hongos": CollectionEnum.RIQUEZA_OBSERVADA_HONGOS,
            "invertebrados": CollectionEnum.RIQUEZA_OBSERVADA_INVERTEBRADOS,
            "mamiferos": CollectionEnum.RIQUEZA_OBSERVADA_MAMIFEROS,
            "reptiles": CollectionEnum.RIQUEZA_OBSERVADA_REPTILES,
            "plantas": CollectionEnum.RIQUEZA_OBSERVADA_PLANTAS,
            "peces": CollectionEnum.RIQUEZA_OBSERVADA_PECES,
        },
    )

    def __init__(
        self,
        metric_name: str,
        operation: OperationEnum,
        main_collection: Optional[CollectionEnum] = None,
        sec_collections: Optional[List[CollectionEnum]] = None,
        indicator: Optional[IndicatorEnum] = None,
        indicator_card_id: Optional[str] = None,
        has_group: bool = False,
        allows_national: bool = False,
        group_collections: Optional[Dict[str, CollectionEnum]] = None,
    ):
        self.metric_name = metric_name
        self.operation_type = operation.value
        self.main_collection = main_collection
        self.sec_collections = sec_collections
        self.indicator = indicator
        self.indicator_card_id = indicator_card_id
        self.has_group = has_group
        self.allows_national = allows_national
        self.group_collections = group_collections


collections_dict = {}
metrics_dict = {}


async def seed_collections_and_metrics():
    await Collection.all().delete()
    await Metric.all().delete()
    await MetricCollection.all().delete()
    await MetricIndicator.all().delete()

    for col in CollectionEnum:
        new_collection = Collection(name=col.value)
        await new_collection.save()
        collections_dict[col.value] = new_collection

    for metric in MetricEnum:

        new_metric = Metric(
            name=metric.metric_name,
            operation_type=metric.operation_type,
            indicator_card_id=metric.indicator_card_id,
            allows_national=metric.allows_national,
        )
        await new_metric.save()

        if metric.indicator:
            await MetricIndicator.create(
                metric=new_metric,
                indicator=metric.indicator.value,
                has_group=metric.has_group,
            )

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
        if metric.group_collections:
            for group_name, group_col in metric.group_collections.items():
                await MetricCollection.create(
                    is_primary=False,
                    metric=new_metric,
                    collection=collections_dict[group_col.value],
                    group_name=group_name,
                )
