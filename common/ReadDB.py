import pyodbc
import ReadConfig
import uuid
import time


class Pyodbc:
    def __init__(self,):
        driver = 'SQL Server Native Client 11.0'  # 因版本不同而异
        readconfig=ReadConfig.ReadConfig()
        DBIp = readconfig.get_db('ip')
        DBUserName = readconfig.get_db('username')
        DBPassWord = readconfig.get_db('password')
        DBName= readconfig.get_db('dbname')
        self.conn = pyodbc.connect(driver=driver, server=DBIp, user=DBUserName, password=DBPassWord, database=DBName)
        self.cursor = self.conn.cursor()

########################################获取测试结果########################################
    def GetCustomer(self,name):
        time.sleep(1)
        name = "'"+name+"'"
        sql = "SELECT TOP 1 [CorrelationId],[Name],[ShortName],[City],[State],[CustomerProspectId],[CustomerTypeId],[CreatorId],[Synopsis],[CustomerKind]\
         from [dbo].[Customer] where name ={0}  order by CreateTime desc ".format(name)
        self.cursor.execute(sql)
        customer= self.cursor.fetchone()
        customerinfo = {
            'correlationId':str(customer[0]),
            'name':customer[1],
            'shortName':customer[2],
            'city':str(customer[3]),
            'state':str(customer[4]),
            'customerProspectId':str(customer[5]),
            'customerTypeId':str(customer[6]),
            'creatorId':str(customer[7]),
            'synopsis':str(customer[8]),
            'customerKind':str(customer[9])
        }
        return customerinfo






        
        