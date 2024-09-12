# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from rate_limiter.rate_limiter import RateLimiter
import redis


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

    # Create a connection to the Redis server
    r = redis.Redis(
        host='ec2-43-204-144-53.ap-south-1.compute.amazonaws.com',
        port=6379,
        password='password',  # Add if Redis is password-protected
        db=0
    )

    rate_limiter = RateLimiter("token_bucket", redis_connection=r)

    # rate_limiter.add_rules(identifiers=["messaging", "marketing", "login"], time_unit="seconds", rate=10)
    #
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))
    # print(rate_limiter.is_rate_limited(["messaging", "marketing", "login", "user"]))

    rate_limiter.add_rules(identifiers=["messaging", "marketing", "auth"], time_unit="hour", rate=3)

    print(rate_limiter.is_rate_limited(["messaging", "marketing", "auth", "user"]))
    print(rate_limiter.is_rate_limited(["messaging", "marketing", "auth", "user"]))
    print(rate_limiter.is_rate_limited(["messaging", "marketing", "auth", "user"]))
    print(rate_limiter.is_rate_limited(["messaging", "marketing", "auth", "user"]))
    print(rate_limiter.is_rate_limited(["messaging", "marketing", "auth", "user"]))




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
