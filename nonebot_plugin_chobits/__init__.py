from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
from .src.core import Chobits

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_chobits",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)
# 实例化
chobits = Chobits()
# 注册命令
chobits.life_cycle.command()
chobits.echo.command()
chobits.corpus.command()
chobits.group_manage.command()
