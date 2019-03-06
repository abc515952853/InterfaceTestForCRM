import pyodbc
import ReadConfig
import uuid
import time


class Pyodbc:
    def __init__(self,):
        driver = 'SQL Server Native Client 11.0'  # 因版本不同而异
        readconfig=ReadConfig.ReadConfig()
        DBIp = readconfig.get_basedata('db_ip')
        DBUserName = readconfig.get_basedata('db_username')
        DBPassWord = readconfig.get_basedata('db_password')
        DBName= readconfig.get_basedata('db_dbname')
        self.conn = pyodbc.connect(driver=driver, server=DBIp, user=DBUserName, password=DBPassWord, database=DBName)
        self.cursor = self.conn.cursor()

    def DBClose(self):
        self.conn.close()
    
    def DBDelete(self,formname):
        sql = "delete [dbo].{}".format(formname)
        self.cursor.execute(sql)
        self.conn.commit()


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

    def GetCustomerMyinfo(self,employeeid):
        time.sleep(1)
        employeeid = "'"+employeeid+"'"
        sql = "SELECT  distinct CustomerId FROM [dbo].[CustomerInDepartment] where DepartmentId in \
        (SELECT DepartmentId FROM [dbo].[EmployeeInDepartment] where EmployeeId={0})".format(employeeid)
        self.cursor.execute(sql)
        customerallinfo= self.cursor.fetchall()
        customerallid = []
        for i in range(len(customerallinfo)):
            customerallid.append(str(customerallinfo[i][0]))
        return customerallid
    

    def GetCustomerSubordinateinfo(self,employeeid):
        time.sleep(1)
        employeeid = "'"+employeeid+"'"
        sql = " WITH cte AS(SELECT i=1, a.* FROM [dbo].[Department] a\
		WHERE a.id in(SELECT DepartmentId FROM [dbo].[EmployeeInDepartment] WHERE EmployeeId={0} and IsLeader=1)\
		UNION ALL\
		SELECT i=c.i+1,d.* FROM cte c \
		INNER JOIN [dbo].[Department] d ON c.id = d.ParentId) \
        SELECT distinct CustomerId FROM [dbo].[CustomerInDepartment] a\
        inner join [dbo].[Customer] b on a.CustomerId =b.CorrelationId  where DepartmentId in (SELECT id FROM cte UNION  SELECT DepartmentId FROM [dbo].[EmployeeInDepartment] where EmployeeId={0})".format(employeeid)
        self.cursor.execute(sql)
        customerallinfo= self.cursor.fetchall()
        customerallid = []
        for i in range(len(customerallinfo)):
            customerallid.append(str(customerallinfo[i][0]))
        return customerallid

    def GetCustomerDetailsinfo(self,correlationid):
        time.sleep(1)
        correlationid = "'"+correlationid+"'"
        sql = "SELECT [CorrelationId],[Name],[ShortName],[City],[State],[CustomerProspectId],[CustomerTypeId],[CreatorId],[Synopsis],[CustomerKind],[assisterId] \
        FROM [dbo].[Customer] WHERE [CorrelationId]={0}".format(correlationid)
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
            'customerKind':str(customerone[9]),
            'assisterId':str(customerone[10])
        }
        return customeroneinfo


    def  CustomerPropertyTypes(self):
        time.sleep(1)
        sql = "SELECT [Id],[Title],[Description] FROM [dbo].[CustomerType]"
        self.cursor.execute(sql)
        PropertyTypesinfo= self.cursor.fetchall()
        PropertyTypesid = []
        for i in range(len(PropertyTypesinfo)):
            PropertyTypesid.append(PropertyTypesinfo[i])
        return PropertyTypesid
    
    def CustomerPropertyProspect(self):
        time.sleep(1)
        sql = "SELECT [Id],[Title],[Description] FROM [dbo].[CustomerProspect]"
        self.cursor.execute(sql)
        PropertyProspectinfo= self.cursor.fetchall()
        PropertyProspectid = []
        for i in range(len(PropertyProspectinfo)):
            PropertyProspectid.append(PropertyProspectinfo[i])
        return PropertyProspectid
    
    def CustomerPropertyLabels(self):
        time.sleep(1)
        sql = "SELECT a.id,a.GroupName,a.BackgroundColor,a.ForegroundColor,b.Id,b.name FROM [dbo].[LabelGroup] a inner join [dbo].[Label] b on a.id = b.[LabelGroupId]"
        self.cursor.execute(sql)
        PropertyLabelsinfo= self.cursor.fetchall()
        return PropertyLabelsinfo

    def GetCustomerInDepartmentinfo(self,key,departmentId):
        if departmentId == '1' or departmentId=='':
            sql = "SELECT CorrelationId FROM [dbo].[Customer] where  Name like '%{}%'".format(key)
        else: 
            sql = "SELECT CorrelationId FROM [dbo].[Customer] where CorrelationId in \
            (SELECT CustomerId FROM [dbo].[CustomerInDepartment] where DepartmentId={}) and Name like '%{}%'".format(departmentId,key)
        self.cursor.execute(sql)
        CustomerInDepartmentinfo= self.cursor.fetchall()
        CustomerInDepartmentid = []
        for i in range(len(CustomerInDepartmentinfo)):
            CustomerInDepartmentid.append(CustomerInDepartmentinfo[i][0])
        return CustomerInDepartmentid


    def GetCustomerLabelsinfo(self,correlationid):
        time.sleep(1)
        correlationid = "'"+correlationid+"'"
        sql = "SELECT LabelId FROM [dbo].[CustomerLabel] where CustomerId={0}".format(correlationid)
        self.cursor.execute(sql)
        labelsinfo= self.cursor.fetchall()
        Labelsid = []
        for i in range(len(labelsinfo)):
            Labelsid.append(labelsinfo[i][0])
        return Labelsid

    def PropertyLabel(self,Module):
        sql = "SELECT [Id],[GroupName],[DepartmentId],[FunctionModule],[IsMultiple],[BackgroundColor],[ForegroundColor] FROM [dbo].[LabelGroup] WHERE [FunctionModule]={0}".format(Module)
        self.cursor.execute(sql)
        labelgroupsinfo= self.cursor.fetchall()
        labelgroups = []
        Labelgroup = {}
        for i in range(len(labelgroupsinfo)):
            sql = "SELECT [Id],[Name] FROM [dbo].[Label] WHERE [LabelGroupId]={0}".format(labelgroupsinfo[i][0])
            self.cursor.execute(sql)
            labelsinfo= self.cursor.fetchall()
            Labels =[]
            Label = {}
            for ii in range(len(labelsinfo)):
                Label ={"id":labelsinfo[ii][0],"name":labelsinfo[ii][1]}
                Labels.append(Label)         
            Labelgroup = {"id":labelgroupsinfo[i][0],"groupname":labelgroupsinfo[i][1],"departmentid":labelgroupsinfo[i][2],"functionmodule":labelgroupsinfo[i][3],"ismultiple":labelgroupsinfo[i][4],"labels":Labels,"backgroundcolor":labelgroupsinfo[i][5],"foregroundcolor":labelgroupsinfo[i][6]}
            labelgroups.append(Labelgroup)
        return labelgroups
    
    def GetContactDetailsinfo(self,contactid):
        time.sleep(1)
        contactid = "'"+contactid+"'"
        sql = "SELECT CorrelationId,Name,Phone,Email,Wechat,Birthday,Street,city,state,Companyname,Job FROM [dbo].[Contact] WHERE CorrelationId = {0}".format(contactid)
        self.cursor.execute(sql)
        contactinfo= self.cursor.fetchone()
        if contactinfo[5] is None:
            birthday = None
        else:
            birthday = contactinfo[5].strftime('%Y-%m-%d %H:%M')

        contact = {"correlationid":contactinfo[0],"name":contactinfo[1],"phone":contactinfo[2],"email":contactinfo[3],"wechat":contactinfo[4],"birthday":birthday,\
        "street":contactinfo[6],"city":contactinfo[7],"state":contactinfo[8],"companyname":contactinfo[9],"job":contactinfo[10]}
        sql = "SELECT [LabelId] FROM [dbo].[ContactLabel] where ContactId={0}".format(contactid)
        self.cursor.execute(sql)
        labelinfo= self.cursor.fetchall()
        labels = []
        for i in range(len(labelinfo)):
            labels.append(labelinfo[i][0])
        contact['labels'] = labels
        return contact

    def GetMyDepartments(self,employeeid):
        employeeid = "'"+employeeid+"'"
        sql = "SELECT a.DepartmentId,b.Name,b.ParentId,c.Name FROM [dbo].[EmployeeInDepartment] a \
        inner join [dbo].[Department] b on a.DepartmentId = b.id \
        left join [dbo].[Department] c on b.ParentId = c.id  WHERE EmployeeId={0}".format(employeeid)
        self.cursor.execute(sql)
        departinfo= self.cursor.fetchall()
        departments = []
        for i in range(len(departinfo)):
            department = {"id":departinfo[i][0],"name":departinfo[i][1]}
            if departinfo[i][2] == 1 or departinfo[i][2] is None:
                department['querylabeldepartmentid'] = departinfo[i][0]
            else:
                department['querylabeldepartmentid'] = departinfo[i][2]
                department['name']=departinfo[i][3]+'('+ department['name']+')'
            departments.append(department)
        return departments
    
    def GetProjectDetailsinfo(self,projectid):
        time.sleep(1)
        projectid = "'"+projectid+"'"
        sql ="SELECT *  FROM [dbo].[Project] WHERE Id={0}".format(projectid)
        self.cursor.execute(sql)
        projectinfo= self.cursor.fetchone()
        project = {
            'id':projectinfo[0],
            'projectname':projectinfo[1],
            'customerid':projectinfo[2],
            'projectteamid':projectinfo[3],
            'lastupdatetime':projectinfo[4],
            'createtime':projectinfo[5],
            'status':projectinfo[6],
            'project_type':projectinfo[7],
            'sellername':projectinfo[8],
            'buyername':projectinfo[9],
            'businesstarget':projectinfo[10],
            'businesstype':projectinfo[11],
            'guarantee':projectinfo[12],
            'quota':projectinfo[13],
            'period':projectinfo[14],
            'interestrate1':projectinfo[15],
            'interestrate2':projectinfo[16],
            'interestrate3':projectinfo[17],
            'amount':projectinfo[18],
            'estimate':projectinfo[19],
            'conditions':projectinfo[20],
            'commitment':projectinfo[21],
            'newsituation':projectinfo[22],
            'creator':projectinfo[23],
            'creatorid':projectinfo[24],
            'departmentid':projectinfo[25]
        }
        return project

    def GetProjectInCustomerinfo(self,projectid):
        projectid = "'"+projectid+"'"
        sql = "SELECT id FROM [dbo].[Project] where CustomerId={}".format(projectid)
        self.cursor.execute(sql)
        ProjectInCustomerinfo= self.cursor.fetchall()
        ProjectInCustomerid = []
        for i in range(len(ProjectInCustomerinfo)):
            ProjectInCustomerid.append(ProjectInCustomerinfo[i][0])
        return ProjectInCustomerid

    def GetEmployinfo(self,employeeid):
        employeeid = "'"+employeeid+"'"
        employeeinfo = {}
        sql = "SELECT workPlace,avatar,jobNumber,position,mobile,Name,isSenior FROM [dbo].[Employee] where id ={}".format(employeeid)
        self.cursor.execute(sql)
        employeebaseinfo= self.cursor.fetchone()
        employeeinfo = {
            "workPlace":employeebaseinfo[0],
            "avatar":employeebaseinfo[1],
            "jobNumber":employeebaseinfo[2],
            "position":employeebaseinfo[3],
            "mobile":employeebaseinfo[4],
            "name":employeebaseinfo[5],
            "isSenior":employeebaseinfo[6],
            "departments":[]
        }
        employeedepart = {}
        sql = "SELECT  a.DepartmentId,b.Name,a.IsLeader FROM [dbo].[EmployeeInDepartment] a inner join [dbo].[Department] b on a.DepartmentId = b.id where EmployeeId ={}".format(employeeid)
        self.cursor.execute(sql)
        employdepartinfo= self.cursor.fetchall()
        for i in range(len(employdepartinfo)):
            employdepart = {
                "departmentId":employdepartinfo[i][0],
                "name":employdepartinfo[i][1],
                "isLeader":employdepartinfo[i][2],}
            employeeinfo["departments"].append(employdepart)
        return employeeinfo

    def GetAppVersionOpenRecord(self,employeeid):
        employeeid = "'"+employeeid+"'"
        sql = "SELECT top 1 EmployeeId,AppVersionId FROM [dbo].[AppVersionOpenRecord] WHERE EmployeeId={} order by CreateTime desc".format(employeeid)
        self.cursor.execute(sql)
        appversionopenrecord= self.cursor.fetchone()
        return appversionopenrecord



########################################创建测试结果########################################

    def AddVersion(self,agentid,version):
        time.sleep(1)
        agentid = "'"+agentid+"'"
        version = "'"+version+"'"
        sql ="insert into [dbo].[AppVersion]([AgentId],[Version],[Content],[IsAppShow],[CreateTime])values({0},{1},'功能更新：XXX',0,getdate())".format(agentid,version)
        self.cursor.execute(sql)

        self.cursor.execute('SELECT @@IDENTITY')
        lastrowid = self.cursor.fetchone()[0]

        self.conn.commit()

        return lastrowid

    def UpdateVersion(self):
        sql = " update [dbo].[AppVersion] set IsAppShow=1 where id = (select top 1 id from [dbo].[AppVersion] order by CreateTime desc )"
        self.cursor.execute(sql)
        self.conn.commit()




            
        

        
        