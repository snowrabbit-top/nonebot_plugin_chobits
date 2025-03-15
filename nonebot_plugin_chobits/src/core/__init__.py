"""
机器人
"""

from .corpus import Corpus
from .group_manage import GroupManage
from ..utils.mysql import MySql
from ..utils.redis import Redis


class Chobits:
    """
    MySQL 工具
    """
    mysql = MySql()
    """
    Redis 工具
    """
    redis = Redis()
    """
    语料库功能
    """
    corpus = Corpus()
    """
    群管理功能
    """
    group_manage = GroupManage()
