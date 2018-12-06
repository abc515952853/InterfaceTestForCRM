# import pymssql

# DBIp = 'rm-bp1x18acc5y19f4k0do.sqlserver.rds.aliyuncs.com,3433'
# DBUserName = 'qianjifang'
# DBPassWord = 'dje*jeUJ3*qj^su22'
# DBName= 'syzb_test_crm'


# # DBIp = '139.196.144.98'
# # DBUserName = 'sa'
# # DBPassWord = '1qaz@WSX3edc'
# # DBName= 'QianKeTong'

# conn = pymssql.connect(DBIp,DBUserName,DBPassWord,DBName)
# cursor = conn.cursor()



import pyodbc

driver = 'SQL Server Native Client 11.0'  # 因版本不同而异
server = 'rm-bp1x18acc5y19f4k0do.sqlserver.rds.aliyuncs.com,3433'  
user = 'qianjifang'
password = 'dje*jeUJ3*qj^su22'
database = 'syzb_test_crm'
 
conn = pyodbc.connect(driver=driver, server=server, user=user, password=password, database=database)
 
cur = conn.cursor()
sql = 'SELECT * FROM [dbo].[Customer] order by CreateTime desc'  # 查询语句
cur.execute(sql)
rows = cur.fetchall()  # list
conn.close()
 
for row in rows:
    print(row)  
