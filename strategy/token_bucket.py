from datetime import datetime
from .base import BaseStrategy


class TokenBucket(BaseStrategy):

    def __init__(self):
        super().__init__()
        self.time_conversion = {"seconds": 1, "minutes": 60, "hour": 3600}

    def find_remaining_counter(self, rule_configs, current_identifier_state):

        last_modified = current_identifier_state.get("last_modified")
        counter = int(current_identifier_state.get("counter"))
        time_unit = rule_configs.get("time_unit")
        rate = int(rule_configs.get("rate"))
        bucket_size = int(rule_configs.get("bucket_size"))

        time_diff = (datetime.now() - datetime.strptime(last_modified, "%Y-%m-%d %H:%M:%S.%f")).seconds \
                    // self.time_conversion[time_unit]
        return min(bucket_size, counter + time_diff * rate)

    def rate_limiting_check(self, identifier, connection):

        try:
            self.identifier = identifier
            self.connection = connection

            rule_configs = self.fetch_rules()
            current_identifier_state = self.fetch_current_state()
            state_identifier = ":".join(self.identifier)

            if len(current_identifier_state) == 0:
                identifier_state = {"counter": rule_configs["rate"], "last_modified": str(datetime.now())}
                connection.hset(state_identifier, mapping=identifier_state)

            else:
                total_counter = self.find_remaining_counter(rule_configs, current_identifier_state)

                if total_counter == 0:
                    return True

                identifier_state = {"counter": total_counter - 1, "last_modified": str(datetime.now())}
                self.connection.hset(state_identifier, mapping=identifier_state)

            return False

        except Exception as e:
            return str(e)
