import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 
import uuid

api='api/v1.2/Customer/All?key=&departmentIds=&pageIndex=1&pageSize=1000'
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
        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()

        if r.status_code==200:
            customerindepartmentid = readdb.GetCustomerInDepartmentinfo(key,departmentId)
        #     responecustomerindepartmentid = []
        #     for i in range(len(r.json()['list'])):
        #         responecustomerindepartmentid.append(r.json()['list'][i]['id'])
        #         self.assertIn(r.json()['list'][i]['id'].upper(),customerindepartmentid,case_describe)
        #     self.assertEqual(len(responecustomerindepartmentid),len(customerindepartmentid),case_describe)
        #     self.assertEqual(r.json()['count'],len(customerindepartmentid),case_describe)
        # else:
        #     self.assertEqual(r.status_code,200,case_describe)   