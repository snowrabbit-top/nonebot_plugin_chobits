"""
群管理功能
"""
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event


class GroupManage:

    def command(self):
        """
        管理功能命令列表
        :return:
        """
        menu = on_command(cmd="group_manage -h", aliases={"管理功能帮助", "管理功能命令"})

        @menu.handle()
        async def handle_menu(bot: Bot, event: Event):
            member_list = await bot.get_group_member_list(group_id=event.group_id)
            print(member_list)
            print("管理功能")
