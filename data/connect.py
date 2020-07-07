from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
# HOSTNAME = '130.211.244.227'
HOSTNAME = '172.17.0.1'
USERNAME = ''#数据库名称
# USERNAME = 'root'
PASSWORD = ''#填写数据库密码
# PORT = '3306'
PORT = ''#端口号
DATABASE = 'yishuifengxing_weblog'
Db_url = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8'%(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    PORT,
    DATABASE
)
print(Db_url)
engine = create_engine(Db_url)
Base = declarative_base(engine)
Sessoin = sessionmaker(engine)
session = Sessoin()


if __name__ == '__main__':
    connection = engine.connect()
    result = connection.execute('select 1')
    print(result.fetchone())
