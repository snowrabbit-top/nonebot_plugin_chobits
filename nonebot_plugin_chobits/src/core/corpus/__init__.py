"""
语料库
"""
import nonebot

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from ....src.utils.redis import Redis
from ....src.utils.mysql import MySql


class Corpus:
    """
    MySql 工具
    """
    mysql = None
    """
    Redis 工具
    """
    redis = None
    """
    表名
    """
    table = "corpus"

    def __init__(self):
        """
        初始化
        """
        self.mysql = MySql()
        self.redis = Redis()

    def get_corpus_list(self, where):
        """
        获取语料列表
        :param where:
        :return:
        """
        return self.mysql.select_column(table=self.table, where=where)

    def cache_corpus(self, info):
        """
        缓存语料
        :param info:
        :return:
        """
        self.redis.hash_set(key="corpus", field=info["key"], value=info["value"])

    def cache_del_corpus(self, key):
        """
        删除缓存语料
        :param key:
        :return:
        """
        self.redis.hash_del(key="corpus", field=key)

    def cache_corpus_list(self):
        """
        缓存全部语料
        :return:
        """
        corpus_list = self.get_corpus_list(where={})
        for info in corpus_list:
            self.cache_corpus(info=info)

    def add_corpus(self, data):
        """
        添加语料
        :param data:
        :return:
        """
        flag = self.mysql.insert(table=self.table, data=data)
        if flag:
            self.cache_corpus(info=data)
            return True
        else:
            return False

    def del_corpus(self, where):
        """
        删除语料
        :param where:
        :return:
        """
        return self.mysql.delete(table=self.table, where=where)

    def update_corpus(self, data, where):
        """
        更新语料
        :param data:
        :param where:
        :return:
        """
        return self.mysql.update(table=self.table, data=data, where=where)

    def get_corpus(self, where):
        """
        获取语料
        :param where:
        :return:
        """
        return self.mysql.find_info(table=self.table, where=where)

    def command(self):
        """
        语料库命令列表
        :return:
        """
        menu = on_command(cmd="corpus -h", aliases={"语料库帮助", "语料库命令"})

        @menu.handle()
        async def handle_menu(bot: Bot, event: Event):
            message = """语料库
日常对话自动回复
    示例: 
        用户: XXX
        Bot: XXX
添加语料
    示例:
        命令: 添加语料库
        Bot: 请输入语料(键和值之间换行分开)
        用户:
            早安
            早安~
            """
            await menu.finish(message)
