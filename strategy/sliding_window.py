from .base import BaseStrategy
from datetime import datetime, timedelta
import threading


class SlidingWindow(BaseStrategy):

    def __init__(self):
        super().__init__()
        self.transform_factor = {"second": 1, "minute": 60, "hour": 3600}

    def rate_limiting_check(self, identifier, connection):
        self.identifier = identifier
        self.connection = connection

        rule = self.fetch_rules()
        time_unit = rule.get("time_unit")
        allowed_request = int(rule.get("allowed_requests"))

        # current_state = self.fetch_current_data_sorted_set()
        current_time = datetime.now()
        threshold_time = current_time - timedelta(seconds=self.transform_factor[time_unit])

        state_identifier = ":".join(self.identifier)

        set_data = self.connection.zrangebyscore(state_identifier,
                                                 threshold_time.timestamp(), current_time.timestamp(), withscores=True)

        pipe = self.connection.pipeline()

        flag = False
        print(len(set_data), allowed_request)
        if len(set_data) >= allowed_request:
            flag = True
        else:
            pipe.zadd(state_identifier, {str(current_time): current_time.timestamp()})
        pipe.zremrangebyscore(state_identifier, '-inf', threshold_time.timestamp())
        pipe.execute()

        return flag
