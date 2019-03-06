import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import  json 
import uuid
import random


sheet_name = "ContactCreate"
api='api/Contact'

excel = ReadExcl.Xlrd()

@ddt.ddt
class TestContactCreate(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.readdb = ReadDB.Pyodbc()
        self.readconfig=ReadConfig.ReadConfig()

        self.readdb.DBDelete("[ContactLabel]")
        self.readdb.DBDelete("[Contact]")

    @classmethod
    def tearDownClass(self):
        self.readdb.DBClose()

    def setUp(self):
        pass

    def tearDown(self): 
        pass 
        
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_ContactCreate(self, data):
        name = str(data['name'])
        labelcount = int(data['labelcount'])
        phone = str(data['phone'])
        expected_code = int(data["expected_code"])
        case_describe = str(data["case_describe"])

        excel = ReadExcl.Xlrd()

        contactlabels = list(map(int,str(self.readconfig.get_dynamicdata("labelgroup_module_contact_label")).split(','))) 

        labels = random.sample(contactlabels,labelcount) 

        url = self.readconfig.get_basedata('crm_url')+api
        session =  self.readconfig.get_basedata('member_session')
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
        
        if r.status_code == 201:
            contactinfo = self.readdb.GetContactDetailsinfo(r.json()['id'])
            self.assertEqual(contactinfo['name'],name+str(data["case_id"]),case_describe + ",接口：{0}".format(api))
            self.assertEqual(contactinfo['phone'],phone,case_describe + ",接口：{0}".format(api))
            for i in range(len(labels)):
                self.assertIn(labels[i],contactinfo['labels'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(len(labels),len(contactinfo['labels']),case_describe + ",接口：{0}".format(api))

            self.readconfig.append_dynamicdata("contact_id",str(r.json()['id']))

        self.assertEqual(r.status_code,expected_code,case_describe + ",接口：{0}".format(api))   

