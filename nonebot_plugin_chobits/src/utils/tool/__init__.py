import json


def parse_json_or_string(string):
    """
    解析JSON字符串，失败时返回原字符串
    """
    try:
        return json.loads(string)
    except json.JSONDecodeError:  # 捕获JSON格式错误
        return string
    except TypeError:  # 捕获非字符串输入（如数字、None等）
        return string


def safe_json_serialize(value):
    """序列化规则：
    1. 字符串直接返回
    2. 可序列化对象转为JSON字符串
    3. 不可序列化对象尝试取其__dict__再序列化
    4. 全部失败则抛出异常
    """
    if isinstance(value, str):
        return value

    try:
        # 尝试直接序列化
        return json.dumps(value)
    except TypeError:
        # 如果对象有__dict__属性，尝试序列化其字典
        if hasattr(value, '__dict__'):
            try:
                return json.dumps(value.__dict__)
            except TypeError:
                raise TypeError(f"无法序列化对象：{value}")
        return value
