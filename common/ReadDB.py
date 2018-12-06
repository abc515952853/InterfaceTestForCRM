import pymssql
import ReadConfig
import uuid
import time


class Pymssql:
    def __init__(self,):
        readconfig=ReadConfig.ReadConfig()
        DBIp = readconfig.get_db('ip')
        DBUserName = readconfig.get_db('username')
        DBPassWord = readconfig.get_db('password')
        DBName= readconfig.get_db('dbname')
        self.conn = pymssql.connect(DBIp,DBUserName,DBPassWord,DBName)
        self.cursor = self.conn.cursor()

########################################获取测试结果########################################
    def GetCustomer(self,phone):
        sql = "select a.id,a.nickname,c.ShortName,b.id,b.CompanyId  from [dbo].[User] a \
        inner join [dbo].[Customer] b on a.id = b.userid \
        inner join [dbo].[company] c on c.id = b.CompanyId where a.phone = {0} ".format(phone)
        self.cursor.execute(sql)
        customer= self.cursor.fetchone()
        customerinfo = {'userid':str(customer[0]),'nickname':customer[1],'companyshort':customer[2],'customerid':str(customer[3]),'companyid':str(customer[4])}
        return customerinfo

    def GetUser(self,phone):
        sql = "select a.id,b.id,c.id,a.nickname  from [dbo].[User] a\
        inner join [dbo].[Customer] b on a.id = b.userid \
        inner join [dbo].[Blog] c on c.CustomerId = b.id where a.phone = {0} ".format(phone)
        self.cursor.execute(sql)
        User= self.cursor.fetchone()
        userinfo = {'userid':str(User[0]),'customerid':str(User[1]),'blogid':str(User[2]),'nickname':str(User[3])}
        return userinfo

    def GetBlog(self,phone):
        sql ="select c.id,a.phone,d.ShortName,a.nickname,c.Status  from [dbo].[User] a\
        inner join [dbo].[Customer] b on a.id = b.userid \
        inner join [dbo].[Blog] c on c.CustomerId = b.id \
		inner join [dbo].[company] d on b.CompanyId = d.id  where a.phone = {0} ".format(phone)
        self.cursor.execute(sql)
        blog= self.cursor.fetchone()
        bloginfo = {'blogid':str(blog[0]),'phone':blog[1],'companyName':blog[2],'nickname':blog[3],'status':blog[4]}
        return bloginfo

    def GetClientinfo(self,cleintid):
        cleintid = "'"+cleintid+"'"
        time.sleep(1)
        sql = "select  display,phone,customerId,companyId,level,remarks,status from [dbo].[Client] where id={0}".format(cleintid)
        self.cursor.execute(sql)
        client= self.cursor.fetchone()
        if client is not None:
            clientinfo = {'display':client[0],'phone':client[1],'customerId':str(client[2]),'companyId':str(client[3]),'level':client[4],'remarks':client[5],'status':client[6]}
        return clientinfo

    def GetClientAllinfo(self,customerid):
        customerid = "'"+customerid+"'"
        sql = "select * from [dbo].[Client] where customerid={0}".format(customerid)
        self.cursor.execute(sql)
        clientallinfo= self.cursor.fetchall()
        clientallid = []
        for i in range(len(clientallinfo)):
            clientallid.append(str(clientallinfo[i][0]))
        return clientallid

    def GetClientMaintainNumber(self,customerid):
        customerid = "'"+customerid+"'"
        sql = "select count(*) from [dbo].[Client] where [status]=1 and customerid={0}".format(customerid)
        self.cursor.execute(sql)
        maintainfo= self.cursor.fetchone()
        maintainnumber = maintainfo[0]
        return maintainnumber

    def GetUserMoney(self,userid):
        userid = "'"+userid+"'"
        sql = "select moneyout from [dbo].[User] where id={0}".format(userid)
        time.sleep(1)
        self.cursor.execute(sql)
        usermoneyinfo= self.cursor.fetchone()
        return usermoneyinfo[0]

    def GetClientMaintainOrder(self,orderid):
        orderid = "'"+orderid+"'"
        sql = "select TotalPrice from [dbo].[ClientMaintainOrder] where id={0}".format(orderid)
        time.sleep(1)
        self.cursor.execute(sql)
        ordertotalprice= self.cursor.fetchone()
        return ordertotalprice[0]


########################################布置测试环境########################################

    def SetCustomerMoney(self,money,userid):
        userid = "'"+userid+"'"
        sql = "update [dbo].[User] set MoneyIn={0},MoneyOut=0 where id={1}".format(money,userid)
        self.cursor.execute(sql)
        self.conn.commit()
        





        
        