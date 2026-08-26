from typing import List, Dict

from app.models.models import ProtConn, DPC, SpeciesStats, Polygon
from app.utils.errors import NotFoundError


class AbstractIndicator:
    def __init__(self, indicator_table: str):
        indicators_map = {
            "prot_conn": ProtConn,
            "dpc": DPC,
            "statsOnSpecies": SpeciesStats,
        }
        self.indicator_obj = indicators_map[indicator_table]
        if self.indicator_obj is None:
            raise NotFoundError(
                "indicator not defined",
                usr_msg=f"There was an error calculating the values.",
            )

    async def get_values_by_polygon(
        self,
        polygon: Polygon,
        group: str | None = None,
    ) -> Dict[str, str | float] | List[Dict[str, str | float]]:
        """
        Returns the values for the configurated indicator and given polygon
        """
        filters: Dict[str, Polygon | str] = {"polygon": polygon}
        if group is not None:
            filters["group_name"] = group

        result = await self.indicator_obj.filter(**filters)
        if len(result) == 0:
            raise NotFoundError(
                "data not found",
                usr_msg=f"There are no values in the database for the given metric and polygon",
            )
        table_name = self.indicator_obj.describe()["table"]
        if table_name == "dpc":
            return sorted(
                (val.get_result_for_metric() for val in result),
                key=lambda item: item["dpc"],
                reverse=True,
            )
        if table_name == "species_stats":
            return result[0].get_result_for_metric()
        else:
            return self.indicator_obj.get_result_for_metric(result[0])
