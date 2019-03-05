import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 
import uuid

api='api/Contact/{0}/Address'
sheet_name = "ContactUpdateAddress"

excel = ReadExcl.Xlrd()

@ddt.ddt
class ContactUpdateAddress(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_ContactUpdateAddress(self,data):
        street = str(data["street"])
        city = str(data["city"])
        state = str(data["state"])
        case_describe = str(data["case_describe"])
        expected_code = int(data["expected_code"])

        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        contactid = readconfig.get_contact('contact1')
        url = readconfig.get_url('crmurl')+api.format(contactid)
        session =  readconfig.get_basedata('session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        payload ={
            "address": {
                "street": street,
                "city": city,
                "state": state
            }
        }
        r = requests.post(url=url,data = json.dumps(payload),headers = headers)

        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        #数据对比
        if r.status_code == expected_code:
            contactdetails = readdb.GetContactDetailsinfo(contactid)
            self.assertEqual(contactdetails['street'],street,case_describe)
            self.assertEqual(contactdetails['city'],city,case_describe)
            self.assertEqual(contactdetails['state'],state,case_describe)
        else:
            self.assertEqual(r.status_code,expected_code,case_describe)   