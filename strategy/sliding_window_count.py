from .base import BaseStrategy
from datetime import datetime, timedelta


class SlidingWindowCount(BaseStrategy):

    def __init__(self):
        super().__init__()
        self.transform_factor = {"second": 1, "minute": 60, "hour": 3600}

    def rate_limiting_check(self, connection, identifier):
        self.identifier = identifier
        self.connection = connection

        rule = self.fetch_rules()
        time_unit = rule.get("time_unit")
        allowed_request = int(rule.get("allowed_requests"))

        current_state = self.fetch_current_state_list_data()
        current_time = datetime.now()
        threshold_time = str(current_time - timedelta(seconds=self.transform_factor[time_unit]))

        state_identifier = ":".join(self.identifier)
