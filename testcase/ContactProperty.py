import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

api='api/Label/Contact/all'
case_describe = '获取联系人标签'

class ContactProperty(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.readdb = ReadDB.Pyodbc()
        self.readconfig=ReadConfig.ReadConfig()

    @classmethod
    def tearDownClass(self):
        self.readdb.DBClose()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ContactPropertyLabel(self):
        url = self.readconfig.get_basedata('crm_url')+api
        session =  self.readconfig.get_basedata('member_session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            contactpropertylabel = self.readdb.PropertyLabel(self.readconfig.get_basedata('labelgroup_module_contact'))
            contactlabels = []
            for i in range(len(r.json())):
                for ii in range(len(contactpropertylabel)):
                    if r.json()[i]['id'] == contactpropertylabel[ii]['id']:
                        self.assertEqual(r.json()[i]['groupName'],contactpropertylabel[ii]['groupname'],case_describe + ",接口：{0}".format(api))
                        self.assertEqual(r.json()[i]['departmentId'],contactpropertylabel[ii]['departmentid'],case_describe + ",接口：{0}".format(api))
                        # self.assertEqual(r.json()[i]['functionModule'],contactpropertylabel[ii]['functionmodule'],case_describe + ",接口：{0}".format(api))
                        self.assertEqual(r.json()[i]['isMultiple'],contactpropertylabel[ii]['ismultiple'],case_describe + ",接口：{0}".format(api))
                        self.assertEqual(r.json()[i]['backgroundColor'],contactpropertylabel[ii]['backgroundcolor'],case_describe + ",接口：{0}".format(api))
                        self.assertEqual(r.json()[i]['foregroundColor'],contactpropertylabel[ii]['foregroundcolor'],case_describe + ",接口：{0}".format(api))

                        for iii in range(len(r.json()[i]['labels'])):
                            for iiii in range(len(contactpropertylabel[ii]['labels'])):
                                if r.json()[i]['labels'][iii]['id'] == contactpropertylabel[ii]['labels'][iiii]['id']:
                                    contactlabels.append(str(r.json()[i]['labels'][iii]['id']))
                                    self.assertEqual(r.json()[i]['labels'][iii]['name'],r.json()[i]['labels'][iii]['name'],case_describe + ",接口：{0}".format(api))
                                    self.assertEqual(len(r.json()[i]['labels']),len(contactpropertylabel[ii]['labels']),case_describe + ",接口：{0}".format(api))
            self.readconfig.set_dynamicdata('labelgroup_module_contact_label',','.join(contactlabels))
        self.assertEqual(r.status_code,200,case_describe + ",接口：{0}".format(api))  
