class UnsupportedMetricException(Exception):
    def __init__(self, metric_id: str):
        self.metric_id = metric_id
        self.usr_msg = f"Unsupported metric: '{metric_id}'"
        self.log_msg = (
            f"Metric ID '{metric_id}' is not supported in METRICS_CONFIG."
        )
        self.code = 400
