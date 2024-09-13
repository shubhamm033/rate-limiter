from .base import BaseStrategy
from datetime import datetime, timedelta


class SlidingWindowCount(BaseStrategy):

    def __init__(self):
        super().__init__()
        self.transform_factor = {"second": 1, "minute": 60, "hour": 3600}

    def rate_limiting_check(self, identifier, connection):
        self.identifier = identifier
        self.connection = connection
        rule = self.fetch_rules()
        time_unit = rule.get("time_unit")
        allowed_request = int(rule.get("allowed_requests"))

        current_time = datetime.now()
        last_time = current_time - timedelta(seconds=self.transform_factor[time_unit])
        last_time_format = self.change_format(last_time, time_unit).strftime('%Y-%m-%d %H:%M:%S')

        self.identifier.append(last_time_format)
        last_state = self.fetch_current_state()
        self.identifier[-1] = self.change_format(current_time, time_unit).strftime('%Y-%m-%d %H:%M:%S')

        current_state = self.fetch_current_state()
        current_time_percentage = (current_time.second) / 60
        remaining_percentage = 1 - current_time_percentage

        current_count = 0
        last_count = 0

        if current_state:
            current_count = int(current_state.get("current_count"))

        if last_state:
            last_count = int(last_state.get("current_count"))

        total_requests = int(current_time_percentage*current_count + remaining_percentage*last_count)
        state_identifier = ":".join(self.identifier)

        if total_requests >= allowed_request:
            return True

        current_state.update({"current_count": current_count + 1})
        self.connection.hset(state_identifier, mapping=current_state)

        return False
