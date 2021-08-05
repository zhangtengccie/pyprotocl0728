import sqlite3
from dateutil import parser
from datetime import datetime, timedelta
from mat_line import mat_line


def cpu_read_db(dbname, last_min=1):
    # 链接数据库
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    # 获取当前时间
    now = datetime.now()
    # 计算最近几分钟的时间
    before_last_min = now - timedelta(minutes=last_min)
    # 根据时间查询数据
    cursor.execute(f'select time,cpu from routerdb where time > "{before_last_min}"')
    # 从数据库得到数据
    yourresults = cursor.fetchall()
    # 返回列表套列表
    return [[parser.parse(i[0]), i[1]] for i in yourresults]


if __name__ == '__main__':
    # print(cpu_read_db('deviceinfo.sqlite',1))
    mat_line(cpu_read_db('deviceinfo.sqlite', 1))
