import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json
import random 

api='api/Contact/{0}'
case_describe = '获取联系人属性'

class ContactDetails(unittest.TestCase): 
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

    def test_ContactDetails(self):
        contactids = list(map(str,str(self.readconfig.get_dynamicdata("contact_id")).split(','))) 
        contactid = random.sample(contactids,1)[0] 
    
        url = self.readconfig.get_basedata('crm_url')+api.format(contactid)
        session =  self.readconfig.get_basedata('member_session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        
        if r.status_code == 200:
            contactinfo = self.readdb.GetContactDetailsinfo(contactid)
            print(contactinfo['birthday'],r.json()['birthday'])
            self.assertEqual(contactinfo['name'],r.json()['name'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(contactinfo['phone'],r.json()['phone'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(contactinfo['email'],r.json()['email'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(contactinfo['wechat'],r.json()['wechat'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(contactinfo['birthday'],r.json()['birthday'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(contactinfo['state'],r.json()['state'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(contactinfo['street'],r.json()['street'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(contactinfo['city'],r.json()['city'],case_describe + ",接口：{0}".format(api))
            # self.assertEqual(contactinfo['companyname'],r.json()['companyname'],case_describe + ",接口：{0}".format(api))
            # self.assertEqual(contactinfo['job'],r.json()['job'],case_describe + ",接口：{0}".format(api))
            la =[]
            for ii in range(len(r.json()['labels'])):
                la.append(r.json()['labels'][ii]['id'])
            for i in range(len(contactinfo['labels'])):
                self.assertIn(contactinfo['labels'][i],la,case_describe + ",接口：{0}".format(api))
            self.assertEqual(len(contactinfo['labels']),len(la),case_describe + ",接口：{0}".format(api))
        self.assertEqual(r.status_code,200,case_describe + ",接口：{0}".format(api))     