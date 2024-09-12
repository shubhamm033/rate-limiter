from .startegy_factory import StrategyFactory
import json


class RateLimiter:

    def __init__(self, strategy, redis_connection):
        self.strategy = strategy
        self.redis_connection = redis_connection

    # def add_algorithm_types(self):
    #     token_bucket_format = {"id": 1,
    #                            "name": "token_bucket",
    #                            "config_format": {"unit": None,
    #                                              "window": None,
    #                                              "request_allowed": None}
    #                            }
    #
    #     leaky_bucket_format = {"id": 2,
    #                            "name": "leaky_bucket",
    #                            "config_format": {"unit": None,
    #                                              "bucket_size": None,
    #                                              "leak_rate": None}
    #                            }
    #
    #     window_counter = {"id": 3,
    #                       "name": "window_counter",
    #                       "config_format": {"unit": None, "request_allowed": None}
    #                       }
    #
    #     sliding_window_log = {"id": 4,
    #                           "name": "sliding_window_log",
    #                           "config_format": {"unit": None, "request_allowed": None}
    #                           }
    #
    #     self.redis_connection.set("algo:1", json.dumps(token_bucket_format))
    #     self.redis_connection.set("algo:2", json.dumps(leaky_bucket_format))
    #     self.redis_connection.set("algo:3", json.dumps(window_counter))
    #     self.redis_connection.set("algo:4", json.dumps(sliding_window_log))

    def add_rules(self, **kwargs):
        identifiers = kwargs.get("identifiers")
        time_unit = kwargs.get("time_unit")
        rate = kwargs.get("rate")

        key = ":".join(identifiers)
        rules = {"time_unit": time_unit, "rate": rate}
        self.redis_connection.hset(key, mapping=rules)
        print(self.redis_connection.hgetall(key))

    def is_rate_limited(self, identifier):
        # based on our identifiers , we will find out the whether request is rate limited or not
        instance = StrategyFactory.get_strategy(self.strategy)
        return instance.rate_limiting_check(identifier, self.redis_connection)
