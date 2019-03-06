import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import  json 
import uuid


sheet_name = "ContactCreate"
api='api/Contact'

excel = ReadExcl.Xlrd()

@ddt.ddt
class TestContactCreate(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_ContactCreate(self, data):
        name = str(data['name'])
        labels = list(map(int,str(data["labels"]).split(',')))
        phone = str(data['phone'])
        expected_code = int(data["expected_code"])
        case_describe = str(data["case_describe"])
        
        excel = ReadExcl.Xlrd()
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_basedata('crm_url')+api
        session =  readconfig.get_basedata('session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        payload ={
            "name": name+str(data["case_id"]),
            "phone": phone,
            "labelIds":labels
            }

        r = requests.post(url=url,data = json.dumps(payload),headers = headers)
    
        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        if r.status_code == expected_code:
            contactinfo = readdb.GetContactDetailsinfo(r.json()['id'])
            self.assertEqual(contactinfo['name'],name+str(data["case_id"]),case_describe + ",接口：{0}".format(api))
            self.assertEqual(contactinfo['phone'],phone,case_describe + ",接口：{0}".format(api))
            for i in range(len(labels)):
                self.assertIn(labels[i],contactinfo['labels'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(len(labels),len(contactinfo['labels']),case_describe + ",接口：{0}".format(api))
            readconfig.set_contact("Contact"+str(data["case_id"]),r.json()['id'])
        self.assertEqual(r.status_code,expected_code,case_describe + ",接口：{0}".format(api))   

