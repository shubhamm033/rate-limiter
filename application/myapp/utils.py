import redis


def fetch_redis_client():
    redis_client = redis.StrictRedis(host='ec2-43-204-144-53.ap-south-1.compute.amazonaws.com', port=6379, db=0,
                                     password='password')

    return redis_client
