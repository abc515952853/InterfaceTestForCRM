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

    def GetCustomerMyresponsibleinfo(self,employeeid):
        employeeid = "'"+employeeid+"'"
        sql = "SELECT * FROM [dbo].[Customer] WHERE [CreatorId]={0}".format(employeeid)
        self.cursor.execute(sql)
        customerallinfo= self.cursor.fetchall()
        customerallid = []
        for i in range(len(customerallinfo)):
            customerallid.append(str(customerallinfo[i][0]))
        return customerallid
    
    def GetCustomerAccessorialinfo(self,employeeid):
        employeeid = "'"+employeeid+"'"
        sql = "SELECT * FROM [dbo].[Customer] WHERE [AssisterId]={0}".format(employeeid)
        self.cursor.execute(sql)
        customerallinfo= self.cursor.fetchall()
        customerallid = []
        for i in range(len(customerallinfo)):
            customerallid.append(str(customerallinfo[i][0]))
        return customerallid

    def GetCustomerSubordinateinfo(self,employeeid):
        employeeid = "'"+employeeid+"'"
        sql = " WITH cte AS(\
		SELECT i=1, a.* FROM [dbo].[Department] a\
		WHERE a.id in(SELECT DepartmentId FROM [syzb_test_crm].[dbo].[EmployeeInDepartment] WHERE EmployeeId={0} and IsLeader=1)\
		UNION ALL\
		SELECT i=c.i+1,d.* FROM cte c \
		INNER JOIN [dbo].[Department] d ON c.id = d.ParentId) \
        select h.* FROM cte e inner join [dbo].[EmployeeInDepartment] f on  e.id = f.DepartmentId\
        inner join [dbo].[Customer] h on f.EmployeeId =h.CreatorId".format(employeeid)
        self.cursor.execute(sql)
        customerallinfo= self.cursor.fetchall()
        customerallid = []
        for i in range(len(customerallinfo)):
            customerallid.append(str(customerallinfo[i][0]))
        return customerallid

    def GetCustomerDetailsinfo(self,correlationid):
        correlationid = "'"+correlationid+"'"
        sql = "SELECT TOP 1000 [CorrelationId],[Name],[ShortName],[City],[State],[CustomerProspectId],[CustomerTypeId],[CreatorId],[Synopsis],[CustomerKind] \
        FROM [syzb_test_crm].[dbo].[Customer] WHERE [CorrelationId]={0}".format(correlationid)
        self.cursor.execute(sql)
        customerone= self.cursor.fetchone()
        customeroneinfo ={
            'correlationId':str(customerone[0]),
            'name':customerone[1],
            'shortName':customerone[2],
            'city':str(customerone[3]),
            'state':str(customerone[4]),
            'customerProspectId':str(customerone[5]),
            'customerTypeId':str(customerone[6]),
            'creatorId':str(customerone[7]),
            'synopsis':str(customerone[8]),
            'customerKind':str(customerone[9])
        }
        return customeroneinfo


    def  CustomerPropertyTypes(self):
        sql = "SELECT [Id],[Title],[Description] FROM [dbo].[CustomerType]"
        self.cursor.execute(sql)
        PropertyTypesinfo= self.cursor.fetchall()
        PropertyTypesid = []
        for i in range(len(PropertyTypesinfo)):
            PropertyTypesid.append(PropertyTypesinfo[i])
        return PropertyTypesid
    
    def CustomerPropertyProspect(self):
        sql = "SELECT [Id],[Title],[Description] FROM [dbo].[CustomerProspect]"
        self.cursor.execute(sql)
        PropertyProspectinfo= self.cursor.fetchall()
        PropertyProspectid = []
        for i in range(len(PropertyProspectinfo)):
            PropertyProspectid.append(PropertyProspectinfo[i])
        return PropertyProspectid
    
    def CustomerPropertyLabels(self):
        sql = "SELECT a.id,a.GroupName,a.BackgroundColor,a.ForegroundColor,b.Id,b.name FROM [dbo].[LabelGroup] a inner join [dbo].[Label] b on a.id = b.[LabelGroupId]"
        self.cursor.execute(sql)
        PropertyLabelsinfo= self.cursor.fetchall()
        return PropertyLabelsinfo


        
        