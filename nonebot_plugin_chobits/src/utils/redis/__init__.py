"""
Redis 缓存数据库操作
    效果: 便于对缓存进行操作

configure: 配置 Redis 数据库
create_connection: 创建 Redis 连接
set_key: 设置键值
get_key: 获取键值
delete_key: 删除键值
get_keys: 获取键值
delete_keys: 删除某类键值
get_all_keys: 获取所有键值
delete_all_keys: 删除所有键值
lpush_key: 向列表开头添加键值
rpush_key: 向列表结尾添加键值
lpop_key: 从列表开头弹出键值
rpop_key: 从列表结尾弹出键值
lrange_key: 获取列表区间
lindex_key: 获取列表索引
lset_key: 设置列表索引
lrem_key: 删除列表值
hash_set: 设置哈希值
hash_get: 获取哈希值
hash_get_all: 获取哈希所有值
hash_del: 删除哈希值

使用类库:
    redis-py:
        安装: pip install redis
"""
import nonebot
import redis

from typing import Any, Awaitable
from ..tool import parse_json_or_string, safe_json_serialize


class Redis:
    """
    Redis 配置
    """
    host = "localhost"
    port = 6379
    password = None
    db = 0
    """
    Redis 连接
    """
    connection = None

    def __init__(self):
        """
        初始化 Redis
        """
        flag = self.configure()
        if flag:
            self.connection = self.create_connection()
            if self.connection is None:
                # 抛出异常
                raise Exception("创建连接失败")
        else:
            # 抛出异常
            raise Exception("请查看 Redis 配置信息")

    def __str__(self) -> str:
        """
        返回 Redis 配置信息
        """
        return f"Redis({self.host}:{self.port})"

    def __del__(self):
        """
        删除 Redis 连接
        """
        self.connection.close()

    def configure(self) -> bool:
        """
        配置 Redis 数据库
        """
        if hasattr(nonebot.get_driver().config, "chobits_redis"):
            config = nonebot.get_driver().config.chobits_redis
            if "host" in config:
                self.host = config["host"]
            else:
                print("未配置Redis host")
                return False
            if "port" in config:
                self.port = config["port"]
            else:
                print("未配置Redis port")
                return False
            if "password" in config:
                self.password = config["password"]
            if "db" in config:
                self.db = config["db"]
            print("Redis 连接成功")
            return True
        else:
            print("未配置MySQL")
            return False

    def create_connection(self) -> redis.Redis:
        """
        创建 Redis 连接
        """
        return redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password
        )

    def set_key(self, key: str, value: Any) -> bool:
        """
        设置键值
        :return:
        """
        value = safe_json_serialize(value)
        return self.connection.set(key, value)

    def get_key(self, key: str) -> str | None | Any:
        """
        获取键值
        :return:
        """
        value: str = self.connection.get(key)
        return parse_json_or_string(value)

    def delete_key(self, key: str) -> bool:
        """
        删除键值
        :return:
        """
        return self.connection.delete(key)

    def get_keys(self, pattern: str) -> list[str]:
        """
        获取键值
        :return:
        """
        return self.connection.keys(pattern)

    def delete_keys(self, pattern: str) -> bool:
        """
        删除某类键值
        :return:
        """
        return self.connection.delete(*self.get_keys(pattern))

    def get_all_keys(self) -> list[str]:
        """
        获取所有键值
        :return:
        """
        return self.connection.keys("*")

    def delete_all_keys(self) -> bool:
        """
        删除所有键值
        :return:
        """
        return self.connection.delete("*")

    def lpush_key(self, key: str, value: Any) -> int:
        """
        向列表开头添加键值
        :return:
        """
        value = safe_json_serialize(value)
        return self.connection.lpush(key, value)

    def rpush_key(self, key: str, value: Any) -> int:
        """
        向列表结尾添加键值
        :return:
        """
        value = safe_json_serialize(value)
        return self.connection.rpush(key, value)

    def lpop_key(self, key: str) -> str | None | Any:
        """
        从列表开头弹出键值
        :return:
        """
        value: str = self.connection.lpop(key)
        return parse_json_or_string(value)

    def rpop_key(self, key: str) -> str | None | Any:
        """
        从列表结尾弹出键值
        :return:
        """
        value: str = self.connection.rpop(key)
        return parse_json_or_string(value)

    def lrange_key(self, key: str, start: int, end: int) -> list[str]:
        """
        获取列表区间
        :return:
        """
        return self.connection.lrange(key, start, end)

    def lindex_key(self, key: str, index: int) -> str | None | Any:
        """
        获取列表索引
        :return:
        """
        value: str = self.connection.lindex(key, index)
        return parse_json_or_string(value)

    def lset_key(self, key: str, index: int, value: Any) -> Awaitable[str] | str:
        """
        设置列表索引
        :return:
        """
        value = safe_json_serialize(value)
        return self.connection.lset(key, index, value)

    def lrem_key(self, key: str, count: int, value: Any) -> int:
        """
        删除列表值
        :return:
        """
        value = safe_json_serialize(value)
        return self.connection.lrem(key, count, value)

    def hash_set(self, key: str, field: str, value: Any) -> Awaitable[int] | int:
        """
        设置哈希值
        :return:
        """
        value = safe_json_serialize(value)
        return self.connection.hset(key, field, value)

    def hash_get(self, key: str, field: str) -> str | None | Any:
        """
        获取哈希值
        :return:
        """
        value: str = self.connection.hget(key, field)
        return parse_json_or_string(value)

    def hash_get_all(self, key: str) -> dict[str, str]:
        """
        获取哈希所有值
        :return:
        """
        return self.connection.hgetall(key)

    def hash_del(self, key: str, field: str) -> int:
        """
        删除哈希值
        :return:
        """
        return self.connection.hdel(key, field)
