from db_connection_pool import DbTool
import json


# print(json.dumps(DbTool('postgresql', 'test_postgresql').selectall("select * from company limit 30"),ensure_ascii=True))
print(DbTool('postgresql', 'test_postgresql').selectall("select * from company limit 30"))