<!--
 * @Author         : SnowRabbit
 * @Date           : 2025-03-15 12:41:16
 * @LastEditors    : SnowRabbit
 * @LastEditTime   : 2025-03-15 12:41:16
 * @Description    : 机器人
 * @GitHub         : https://github.com/snowrabbit-top
-->

<!-- markdownlint-disable MD033 MD036 MD041 -->

<p align="center">
  <img src="docs/logo.jpg" width="200" height="200" alt="chobits">
</p>

<div align="center">

# nonebot-plugin-status

_✨ Chobits 插件 ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">
    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-status">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-status.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="python">
</p>

## 使用方式

通用:

- 发送 Command `菜单` 或者 `menu`

OneBot:

- 开发中 ······

## 配置项

配置方式：直接在 NoneBot 全局配置文件中添加以下配置项即可。

### CHOBITS_MYSQL

- 类型：`json`
- 默认值：`{"user": "root","password": "","host": "localhost","database": ""}`
- 说明：MySql 连接配置

### CHOBITS_REDIS

- 类型：`json`
- 默认值：`{"host": "localhost","port": 6379,"password": ""}`
- 说明：Redis 连接配置
