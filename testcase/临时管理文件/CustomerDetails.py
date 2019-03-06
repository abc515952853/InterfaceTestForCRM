import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

api='api/Customer/{0}'
sheet_name = "CustomerDetails"

excel = ReadExcl.Xlrd()

@ddt.ddt
class CustomerDetails(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_CustomerDetails(self,data):
        customertab = str(data["customertab"])
        case_describe = str(data["case_describe"])

        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        correlationid = readconfig.get_customer(customertab)
        url = readconfig.get_basedata('crm_url')+api.format(correlationid)
        session =  readconfig.get_basedata('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)

        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        #数据对比
        if r.status_code==200:
            customerdetails = readdb.GetCustomerDetailsinfo(correlationid)
            self.assertEqual(customerdetails['name'],r.json()['name'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(customerdetails['shortName'],r.json()['shortName'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(customerdetails['city'],r.json()['city'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(customerdetails['state'],r.json()['state'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(int(customerdetails['customerProspectId']),r.json()['customerProspectId'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(int(customerdetails['customerTypeId']),r.json()['customerTypeId'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(int(customerdetails['customerKind']),r.json()['customerKind'],case_describe + ",接口：{0}".format(api))
        else:
            self.assertEqual(r.status_code,200,case_describe + ",接口：{0}".format(api))   