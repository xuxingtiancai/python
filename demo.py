#os
os.path.isdir()
os.makedirs()
os.walk().next()

#config
config = ConfigParser.RawConfigParser()
config.read('test.conf')

#logging
h = logging.handlers.RotatingFileHandler('log', maxBytes = 102400000, backupCount = 30)
h.setLevel(logging.ERROR)
root_logger = logging.getLogger('root')
root_logger.addHandler(h)
root_logger.setLevel(logging.ERROR)

logging.error(e, exc_info=1)

#redis
goods_redis = redis.StrictRedis(host, port, db=0)
redis_value = goods_redis.get(key)

#
