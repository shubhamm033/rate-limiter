from strategy.token_bucket import TokenBucket
from strategy.sliding_window_count import SlidingWindowCount
from strategy.fixed_window import FixedWindow
from strategy.sliding_window import SlidingWindow


class StrategyFactory:

    @staticmethod
    def get_strategy(type):

        if type == 'token_bucket':
            return TokenBucket()
        elif type == 'sliding_window_count':
            return SlidingWindowCount()
        elif type == 'fixed_window':
            return FixedWindow()
        elif type == 'sliding_window':
            return SlidingWindow()
        else:
            return TokenBucket()
