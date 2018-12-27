import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import  json 
import uuid


sheet_name = "CustomerCreate"
api='api/Customer/create'

excel = ReadExcl.Xlrd()

@ddt.ddt
class TestCustomerCreate(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_CustomerCreate(self, data):
        name = str(data["name"])+str(data["case_id"])
        synopsis = str(data["synopsis"])
        shortName = str(data["shortName"])
        city = str(data["city"])
        state = str(data["state"])
        customerKind = int(data["customerKind"])
        departtype = int(data["departtype"])
        labels = list(map(int,str(data["labels"]).split(',')))
        case_describe = str(data["case_describe"])

        excel = ReadExcl.Xlrd()
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()
        
        #填写求求参数h
        url = readconfig.get_url('url')+api
        session =  readconfig.get_member('session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}

        if data["shortName"] != '':
            shortName = shortName+str(data["case_id"])
        if data["synopsis"] != '':
            synopsis = synopsis+str(data["case_id"])

        if departtype == 1:
            departid = readconfig.get_member('investmentdepartmentId')
            idtype = 'investmentcustomerid'
        elif departtype ==2:
            departid = readconfig.get_member('factoringdepartmentid')
            idtype = idtype = 'actoringdecustomerid'
        payload ={
            "name": name,
            "shortName": shortName,
            "city": city,
            "state": state,
            "synopsis":synopsis,    
            "customerKind":customerKind,
            "labelIds":labels,
            "departmentId":departid
            }

        r = requests.post(url=url,data = json.dumps(payload),headers = headers)

        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        #数据对比
        if r.status_code==200 or r.status_code ==204:
            customerinfo = readdb.GetCustomer(name)
            customerlabelsid = readdb.GetCustomerLabelsinfo(customerinfo['correlationId'])
            self.assertEqual(customerinfo['name'],name,case_describe)
            self.assertEqual(customerinfo['shortName'],shortName,case_describe)
            self.assertEqual(customerinfo['city'],city,case_describe)
            self.assertEqual(customerinfo['state'],state,case_describe)
            self.assertEqual(customerinfo['customerKind'],str(customerKind),case_describe)
            for i in range(len(customerlabelsid)):
                self.assertIn(customerlabelsid[i],labels,case_describe)
                self.assertEqual(len(customerlabelsid),len(labels),case_describe)
        self.assertEqual(r.status_code,data['expected_code'],case_describe)
        readconfig.set_customer(idtype,customerinfo['correlationId'])
            

