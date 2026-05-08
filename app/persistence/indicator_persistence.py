from typing import List, Dict

from app.models.models import ProtConn, DPC, Polygon
from app.utils.errors import NotFoundError


class AbstractIndicator:
    def __init__(self, indicator_table: str):
        indicators_map = {"prot_conn": ProtConn, "dpc": DPC}
        self.indicator_obj = indicators_map[indicator_table]
        if self.indicator_obj is None:
            raise NotFoundError(
                "indicator not defined",
                usr_msg=f"There was an error calculating the values.",
            )

    async def get_values_by_polygon(
        self, polygon: Polygon
    ) -> Dict[str, str | float] | List[Dict[str, str | float]]:
        """
        Returns the values for the configurated indicator and given polygon
        """
        result = await self.indicator_obj.filter(polygon=polygon)
        if len(result) == 0:
            raise NotFoundError(
                "data not found",
                usr_msg=f"There are no values in the database for the given metric and polygon",
            )
        if self.indicator_obj.describe()["table"] == "dpc":
            return list(map(lambda val: val.get_result_for_metric(), result))
        else:
            return self.indicator_obj.get_result_for_metric(result[0])
