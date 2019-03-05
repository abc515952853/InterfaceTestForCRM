import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 
import uuid

api='api/Customer/{0}/Prospect'
sheet_name = "CustomerUpdateProspect"

excel = ReadExcl.Xlrd()

@ddt.ddt
class CustomerUpdateProspect(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_CustomerUpdateProspect(self,data):
        Type = int(data["type"])
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
            "customerProspectId":Type
        }
        r = requests.post(url=url,data = json.dumps(payload),headers = headers)

        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        #数据对比
        if r.status_code==200:
            customerdetails = readdb.GetCustomerDetailsinfo(correlationid)
            self.assertEqual(int(customerdetails['customerProspectId']),Type,case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)  