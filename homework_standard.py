import os
import sqlite3
from snmpv2_get import snmpv2_get
import datetime
import time


def get_info_writedb(ip, rocommunity, dbname, seconds):
    # 如果数据库存在
    if os.path.exists(dbname):
        os.remove(dbname)  # 删除数据库
    # 如果不存在，创建并链接数据库
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    # 创建数据库的表
    cursor.execute("create table routerdb(id INTEGER PRIMARY KEY AUTOINCREMENT, time timestamp, cpu int)")

    while seconds > 0:
        # 通过SNMP获得CPU利用率
        cpu_info = snmpv2_get("1.1.1.200", "tcpipro", "1.3.6.1.4.1.9.9.109.1.1.1.1.3.2", port=161)[1]
        # 获取现在时间
        time_info = datetime.datetime.now()
        # 将CPU 和 时间写入数据库的表中
        cursor.execute(f'insert into routerdb(time,cpu) values("{time_info}","{cpu_info}")')
        # 等待5秒
        time.sleep(5)
        # 传过来的时间减去5秒
        seconds -= 5
        conn.commit()


if __name__ == '__main__':
    get_info_writedb('1.1.1.200', 'tcpipro', 'deviceinfo.sqlite', 1000)
