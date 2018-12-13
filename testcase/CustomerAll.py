import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 
import uuid

api='api/Customer/all?key={0}&departmentId={1}&pageIndex=1&pageSize=1000'
sheet_name = "CustomerAll"

excel = ReadExcl.Xlrd()

@ddt.ddt
class CustomerAll(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_CustomerAll(self,data):
        key = str(data["key"])
        departmentId = str(data["departmentId"])
        case_describe = str(data["case_describe"])

        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_url('url')+api.format(key,departmentId)
        session =  readconfig.get_member('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            customerindepartmentid = readdb.GetCustomerInDepartmentinfo(key,departmentId)
            responecustomerindepartmentid = []
            for i in range(len(r.json()['list'])):
                responecustomerindepartmentid.append(r.json()['list'][i]['id'])
                self.assertIn(r.json()['list'][i]['id'].upper(),customerindepartmentid,case_describe)
            self.assertEqual(len(responecustomerindepartmentid),len(customerindepartmentid),case_describe)
            self.assertEqual(r.json()['count'],len(customerindepartmentid),case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)   