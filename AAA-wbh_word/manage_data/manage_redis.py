# -*- coding: utf-8 -*-
import redis
def make_synchronized(func):
    import threading
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


class Singleton(object):
    _instance = None

    @make_synchronized
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

class RedisPool(Singleton):
    __first_init = False

    def __init__(self):
        if self.__class__.__first_init:
            return
        self.pool = redis.ConnectionPool(host='192.168.1.119', port=32379, db=3, password='cmVkaXNfdW5p')
        self.__class__.__first_init = True

    def redis_instance(self):
        redsiPoolClient = redis.Redis(connection_pool=self.pool)
        return redsiPoolClient

    @staticmethod
    def redis_check(name, key):
        value = RedisPool().redis_instance().hget(name=name, key=key)
        if value:
            return str(value, 'utf-8')
        else:
            return None

    @staticmethod
    def redis_set(name, key, value):
        """
        :param name: classified locate
        :param key:  key
        :param value: value
        :return:
        """
        RedisPool().redis_instance().hset(name=name, key=key, value=value)
        return

    @staticmethod
    def redis_hkeys(name):
        """
        获取所有哈希表中的字段
        :param key:
        :param value:
        :return:
        """
        value = RedisPool().redis_instance().hkeys(name=name)
        if value:
            return str(value)
        else:
            return None

    @staticmethod
    def hgetall(name):
        """
        获取在哈希表中指定 key 的所有字段和值
        :param name: 主机名称
        :return: 返回一个字典
        """
        return RedisPool().redis_instance().hgetall(name=name)

    @staticmethod
    def redis_sadd(key, value):
        """
        向集合添加一个或多个成员
        :param key:
        :param value:
        :return:
        """
        RedisPool().redis_instance().sadd(key, value)
        return

    @staticmethod
    def redis_sismember(key, value):
        """
        判断key集合中是否在
        :param key:
        :param value:
        :return:
        """
        return RedisPool().redis_instance().sismember(key, value)

    @staticmethod
    def redis_smembers(key):
        """
        smembers
        :param key:
        :param value:
        :return:
        """
        return RedisPool().redis_instance().smembers(key)

    @staticmethod
    def redis_del(key):
        """
        删除 key
        :param key:
        :return:
        """
        return RedisPool().redis_instance().delete(key)

    @staticmethod
    def redis_srandmember(key):
        """
        返回集合中的一个随机元素
        :param key:
        :return:
        """
        value = RedisPool().redis_instance().srandmember(key)
        if value:
            return str(value, 'utf-8')
        else:
            return None

    @staticmethod
    def redis_scard(key):
        """
        返回集合中的一个随机元素
        :param key:
        :return:
        """
        value = RedisPool().redis_instance().scard(key)
        if value:
            return value
        else:
            return None

    @staticmethod
    def redis_srem(name, key):
        """
        移除集合中一个或多个成员
        :param key:
        :return:
        """
        try:
            value = RedisPool().redis_instance().srem(name, key)
            return True if value else None
        except Exception:
            return 0

    @staticmethod
    def redis_lpush(key, value):
        """
        将一个或多个值插入到列表头部
        :param key:
        :return:
        """
        if len(value) > 1:
            RedisPool().redis_instance().lpush(key, *value)
        else:
            RedisPool().redis_instance().lpush(key, value)
        return

    @staticmethod
    def redis_lpushx(key, value):
        """
        将一个值插入到已存在的列表头部
        :param key:
        :return:
        """
        RedisPool().redis_instance().lpushx(key, value)
        return

    @staticmethod
    def redis_rpop(key):
        """
        移除列表的最后一个元素，返回值为移除的元素。
        :param key:
        :return:
        """
        return RedisPool().redis_instance().rpop(key)

    @staticmethod
    def redis_llen(key):
        """
        获取列表长度
        :param key:
        :return:
        """
        return RedisPool().redis_instance().llen(key)


