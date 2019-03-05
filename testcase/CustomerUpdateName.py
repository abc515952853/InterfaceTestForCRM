import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 
import uuid

api='api/Customer/{0}/name'
sheet_name = "CustomerUpdateName"

excel = ReadExcl.Xlrd()

@ddt.ddt
class CustomerUpdateName(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_CustomerUpdateName(self,data):
        name = str(data["name"])
        customertab = str(data["customertab"])
        case_describe = str(data["case_describe"])

        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        correlationid = readconfig.get_customer(customertab)
        url = readconfig.get_url('crmurl')+api.format(correlationid)
        session =  readconfig.get_basedata('session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        payload ={
            "name":name
        }
        r = requests.post(url=url,data = json.dumps(payload),headers = headers)

        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        #数据对比
        if r.status_code==202:
            customerdetails = readdb.GetCustomerDetailsinfo(correlationid)
            self.assertEqual(customerdetails['name'],name,case_describe)
        else:
            self.assertEqual(r.status_code,202,case_describe)   