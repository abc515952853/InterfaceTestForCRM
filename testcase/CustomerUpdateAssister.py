import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 
import uuid

api='api/Customer/{0}/SetAssisterId'
sheet_name = "CustomerUpdateAssister"

excel = ReadExcl.Xlrd()

@ddt.ddt
class CustomerUpdateAssister(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_CustomerUpdateAssister(self,data):
        type = int(data["type"])
        customertab = str(data["customertab"])
        case_describe = str(data["case_describe"])
        expected_code = int(data["expected_code"])

        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        correlationid = readconfig.get_customer(customertab)
        if type == 0:
            assisterId = readconfig.get_member("assisterid")
        elif  type == 1:
            assisterId = readconfig.get_member("employeeid")
        else: 
            assisterId = ''

        url = readconfig.get_url('url')+api.format(correlationid)
        session =  readconfig.get_member('session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        payload ={
            "assisterId":assisterId
        }
        r = requests.post(url=url,data = json.dumps(payload),headers = headers)

        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        #数据对比
        if r.status_code==200:
            customerdetails = readdb.GetCustomerDetailsinfo(correlationid)
            self.assertEqual(customerdetails['assisterId'],assisterId,case_describe)
        self.assertEqual(r.status_code,expected_code,case_describe)   