from datetime import datetime
from .base import BaseStrategy


class FixedWindow(BaseStrategy):

    def __init__(self):
        super().__init__()

    def rate_limiting_check(self, identifier, connection):
        self.identifier = identifier
        self.connection = connection

        rule = self.fetch_rules()
        time_unit = rule.get("time_unit")
        allowed_request = int(rule.get("allowed_requests"))
        current_time = self.change_format(datetime.now(), time_unit).strftime('%Y-%m-%d %H:%M:%S')
        self.identifier.append(current_time)

        current_state = self.fetch_current_state()

        state_identifier = ":".join(self.identifier)
        current_request_count = 0
        state_data = {}
        if current_state:
            current_request_count = int(current_state.get("current_count"))

            if current_request_count >= allowed_request:
                return True

        state_data.update({"current_count": current_request_count + 1})
        self.connection.hset(state_identifier, mapping=state_data)
        return False
