from typing import List, Dict

from app.models.models import ProtConn, DPC, SpeciesStats, Polygon
from app.utils.errors import NotFoundError


class AbstractIndicator:
    def __init__(self, indicator_table: str):
        indicators_map = {
            "prot_conn": ProtConn,
            "dpc": DPC,
            "species": SpeciesStats,
        }
        self.indicator_obj = indicators_map[indicator_table]
        if self.indicator_obj is None:
            raise NotFoundError(
                "indicator not defined",
                usr_msg=f"There was an error calculating the values.",
            )

    async def get_values_by_polygon(
        self, polygon: Polygon, slug_grupo: str | None = None
    ) -> Dict[str, str | float] | List[Dict[str, str | float]]:
        """
        Returns the values for the configurated indicator and given polygon
        """
        filters: Dict[str, Polygon | str] = {"polygon": polygon}
        if (
            slug_grupo is not None
            and self.indicator_obj.describe()["table"] == "species_stats"
        ):
            filters["group_slug"] = slug_grupo

        result = await self.indicator_obj.filter(**filters)
        if len(result) == 0:
            raise NotFoundError(
                "data not found",
                usr_msg=f"There are no values in the database for the given metric and polygon",
            )
        if self.indicator_obj.describe()["table"] == "dpc":
            return sorted(
                (val.get_result_for_metric() for val in result),
                key=lambda item: item["dpc"],
                reverse=True,
            )
        if self.indicator_obj.describe()["table"] == "species_stats":
            return result[0].get_result_for_metric()
        else:
            return self.indicator_obj.get_result_for_metric(result[0])
