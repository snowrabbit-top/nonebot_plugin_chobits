"""
机器人生命周期控制器
"""

import os
import sys
import psutil

from nonebot import get_driver, get_adapter, on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Adapter


class LifeCycle:

    def stop(self):
        """
        停止机器人
        """
        os.kill(os.getpid(), 9)

    def restart(self):
        """
        重启机器人
        """
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def kill_children_processes(self):
        """清理子进程（防止僵尸进程）"""
        current_pid = os.getpid()
        parent = psutil.Process(current_pid)
        for child in parent.children(recursive=True):
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass

    async def safe_restart(self):
        """安全重启流程"""
        # 终止子进程
        self.kill_children_processes()
        # 跨平台重启
        os.execl(sys.executable, sys.executable, *sys.argv)

    def command(self):
        """
        命令列表
        """
        driver = get_driver()
        console_adapter = get_adapter(Adapter)
        bots = console_adapter.bots
        print(bots)

        @driver.on_startup
        async def handle_startup():
            """
            开机处理
            :param bot:
            :return:
            """
            print("机器人已开机")

        @driver.on_shutdown
        async def handle_shutdown():
            """
            关机处理
            :param bot:
            :return:
            """
            print("机器人已关机")

        @driver.on_bot_connect
        async def handle_bot_connect(bot: Bot):
            """
            Bot 连接处理
            :param bot:
            :return:
            """
            print("bot已连接")
            print(bot)

        @driver.on_bot_disconnect
        async def handle_bot_disconnect(bot: Bot):
            """
            Bot 断开连接处理
            :param bot:
            :return:
            """
            print("bot已断开")
            print(bot)

        restart = on_command(cmd="restart", aliases={"重启"})

        @restart.handle()
        async def handle_restart(bot: Bot, event: Event):
            await restart.send("正在重启...")
            await self.safe_restart()

        stop = on_command(cmd="stop", aliases={"停止"})

        @stop.handle()
        async def handle_stop(bot: Bot, event: Event):
            await stop.finish("正在停止...")
            os.kill(os.getpid(), 9)

        test = on_command(cmd="test", aliases={"测试"})

        @test.handle()
        async def handle_test(bot: Bot, event: Event):
            print("----------------")
            print("test： 测试成功")
            print("----------------")
            print(console_adapter.bots)
            await test.finish("测试成功")
