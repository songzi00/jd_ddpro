
import pymysql
# 数据库配置
connect = pymysql.connect(
        host = '127.0.0.1',
        db = 'dkbook',
        port = 3306,
        user = 'root',
        passwd = '20001124',
        charset = 'utf8',
        )
cursor = connect.cursor()