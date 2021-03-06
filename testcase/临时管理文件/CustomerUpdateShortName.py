import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 
import uuid

api='api/Customer/{0}/shortName'
sheet_name = "CustomerUpdateShortName"

excel = ReadExcl.Xlrd()

@ddt.ddt
class CustomerUpdateShortName(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_CustomerUpdateShortName(self,data):
        shortName = str(data["name"])
        customertab = str(data["customertab"])
        case_describe = str(data["case_describe"])

        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        correlationid = readconfig.get_customer(customertab)
        url = readconfig.get_basedata('crm_url')+api.format(correlationid)
        session =  readconfig.get_basedata('member_session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        payload ={
            "shortName":shortName
        }
        r = requests.post(url=url,data = json.dumps(payload),headers = headers)

        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        #数据对比
        if r.status_code==200:
            customerdetails = readdb.GetCustomerDetailsinfo(correlationid)
            self.assertEqual(customerdetails['shortName'],shortName,case_describe + ",接口：{0}".format(api))
        else:
            self.assertEqual(r.status_code,200,case_describe + ",接口：{0}".format(api))   