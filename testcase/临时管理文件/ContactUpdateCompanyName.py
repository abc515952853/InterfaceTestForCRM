import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 
import uuid

api='api/Contact/{0}/CompanyName'
sheet_name = "ContactUpdateCompanyName"

excel = ReadExcl.Xlrd()

@ddt.ddt
class ContactUpdateCompanyName(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_ContactUpdateCompanyName(self,data):
        companyname = str(data["companyname"])
        case_describe = str(data["case_describe"])
        expected_code = int(data["expected_code"])

        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        contactid = readconfig.get_contact('contact1')
        url = readconfig.get_basedata('crm_url')+api.format(contactid)
        session =  readconfig.get_basedata('member_session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        payload ={
            "companyname":companyname
        }
        r = requests.post(url=url,data = json.dumps(payload),headers = headers)

        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        #数据对比
        if r.status_code == expected_code:
            contactdetails = readdb.GetContactDetailsinfo(contactid)
            self.assertEqual(contactdetails['companyname'],companyname,case_describe + ",接口：{0}".format(api))
        else:
            self.assertEqual(r.status_code,expected_code,case_describe + ",接口：{0}".format(api))   