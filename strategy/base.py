from abc import ABC, abstractmethod


class BaseStrategy(ABC):

    def __init__(self):
        self.identifier = None
        self.connection = None

    @staticmethod
    def convert_hash_to_dict(redis_hash):
        return {key.decode('utf-8'): value.decode('utf-8')
                for key, value in redis_hash.items()}

    def fetch_rules(self):

        try:
            rule_identifier = ":".join(self.identifier[:-1])
            return self.convert_hash_to_dict(self.connection.hgetall(rule_identifier))
        except Exception as e:
            return str(e)

    def fetch_current_state(self):

        try:
            state_identifier = ":".join(self.identifier)
            x = self.convert_hash_to_dict(self.connection.hgetall(state_identifier))
            return x
        except Exception as e:
            return str(e)

    @staticmethod
    def convert_list_to_readable(item_list):
        return [item.decode('utf-8') for item in item_list]

    def fetch_current_state_list_data(self):

        try:
            state_identifier = ":".join(self.identifier)
            return self.connection.lrange(state_identifier, 0, -1)
        except Exception as e:
            return str(e)

    def fetch_current_data_sorted_set(self):
        try:
            state_identifier = ":".join(self.identifier)
            return self.connection.zrange(state_identifier, 0, -1, withscores=True)
        except Exception as e:
            return str(e)

    @abstractmethod
    def rate_limiting_check(self, identifier, connection):
        pass

    @staticmethod
    def change_format(date, time_unit):
        if time_unit == 'minute':
            return date.replace(second=0)
        elif time_unit == 'hour':
            return date.replace(minute=0, second=0)
        return date
