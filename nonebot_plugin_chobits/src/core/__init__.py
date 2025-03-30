"""
机器人
"""
from .life_cycle import LifeCycle
from .echo import Echo
from .corpus import Corpus
from .group_manage import GroupManage

from ..utils.mysql import MySql
from ..utils.redis import Redis


class Chobits:
    """
    生命周期
    """
    life_cycle = LifeCycle()
    """
    Echo 插件
    """
    echo = Echo()
    """
    MySQL 工具
    """
    mysql = MySql()
    """
    Redis 工具
    """
    redis = Redis()
    """
    群管理功能
    """
    group_manage = GroupManage()
    """
    语料库功能
    """
    corpus = Corpus()
