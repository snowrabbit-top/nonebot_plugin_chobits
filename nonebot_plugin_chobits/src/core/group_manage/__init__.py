"""
群管理功能
"""
import json

from nonebot import on_command, on_regex, on_request
from nonebot.adapters.onebot.v11 import Bot, Event, GroupRequestEvent, Message, MessageSegment

from ....src.utils.tool import extract_numbers, number_is_group


class GroupManage:

    def command(self):
        """
        管理功能命令列表
        :return:
        """

        # 自动同意邀请入群
        def group_invite_rule(event: Event):
            flag = isinstance(event, GroupRequestEvent)
            return flag

        invite_accept = on_request(rule=group_invite_rule)

        @invite_accept.handle()
        async def invite_accept_handle(bot: Bot, event: GroupRequestEvent):
            print("自动同意邀请入群")
            print(f"{event.user_id}邀请我入群,我已同意")
            print(event.flag)
            print(event.sub_type)
            if event.sub_type == "add":
                await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=True)

        listen = on_regex(pattern=r'.*')

        @listen.handle()
        async def handle_listen(bot: Bot, event: Event):
            for i in event.get_message():
                # 判断消息类型(可能是群推荐时)
                if i.type == "json":
                    print(type(i.data))
                    print(type(i.data['data']))
                    json_data = json.loads(i.data['data'])
                    # 群推广
                    if json_data['app'] == 'com.tencent.troopsharecard':
                        # 撤回本条消息
                        await bot.delete_msg(message_id=event.message_id)
                # 判断消息是否含有群号
                if i.type == "text":
                    number_list = extract_numbers(i.data["text"])
                    # 判断是否为列表
                    if isinstance(number_list, list):
                        for number in number_list:
                            try:
                                group_info = await bot.get_group_info(group_id=int(number))
                                if group_info:
                                    # 撤回本条消息
                                    await bot.delete_msg(message_id=event.message_id)
                            except Exception as e:
                                print(e)
            await listen.finish()

        menu = on_command(cmd="group_manage -h", aliases={"管理功能帮助", "管理功能命令"})

        @menu.handle()
        async def handle_menu(bot: Bot, event: Event):
            member_list = await bot.get_group_member_list(group_id=event.group_id)
            print(member_list)
            print("管理功能")
