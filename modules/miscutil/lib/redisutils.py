from nydus.db import create_cluster

from invenio.config import CFG_REDIS_HOSTS

_REDIS_CONN = {}


def get_redis(dbhost=None):
    """Connects to a redis using nydus

    We simlulate a redis cluster by connecting to several redis servers
    in the background and using a consistent hashing ring to choose which
    server stores the data.
    Returns a redis object that can be used like a regular redis object
    see http://redis.io/
    """
    global _REDIS_CONN

    key = dbhost
    if dbhost is None:
        dbhost = CFG_REDIS_HOSTS

    redis = _REDIS_CONN.get(key, None)
    if redis:
        return redis

    hosts_dict = {}
    for server_num, server_info in enumerate(CFG_REDIS_HOSTS):
        hosts_dict[server_num] = server_info

    redis = create_cluster({
        'backend': 'nydus.db.backends.redis.Redis',
        'router': 'nydus.db.routers.keyvalue.ConsistentHashingRouter',
        'hosts': hosts_dict
    })
    _REDIS_CONN[key] = redis
    return redis
