import re

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment


class Echo:

    def command(self):
        """
        命令列表
        """
        echo = on_command(cmd="echo")

        @echo.handle()
        async def handle_echo(bot: Bot, event: Event):
            """
            把消息全部复读出来
            :param bot:
            :param event:
            :return:
            """
            message = event.get_message()
            new_message_list = []
            index = 0
            # 遍历所有的消息都填充到新的消息列表中
            for item in message:
                # 消息类型为text时，去掉echo和空格
                if index == 0 and item.type == 'text':
                    result = re.sub(r'echo ?', '', str(item), count=1)
                    new_message_list.append(MessageSegment.text(result))
                else:
                    new_message_list.append(item)
                index += 1
            new_message = Message(new_message_list)
            await echo.finish(new_message)
