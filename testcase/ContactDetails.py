import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

api='api/Contact/{0}'
case_describe = '获取联系人属性'

class ContactDetails(unittest.TestCase): 
    def test_ContactDetails(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        contactid = readconfig.get_contact('contact1')
        url = readconfig.get_basedata('crm_url')+api.format(contactid)
        session =  readconfig.get_basedata('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        
        if r.status_code == 200:
            #Name,Phone,Email,Wechat,Birthday
            contactinfo = readdb.GetContactDetailsinfo(contactid)
            self.assertEqual(contactinfo['name'],r.json()['name'],case_describe)
            self.assertEqual(contactinfo['phone'],r.json()['phone'],case_describe)
            self.assertEqual(contactinfo['email'],r.json()['email'],case_describe)
            self.assertEqual(contactinfo['wechat'],r.json()['wechat'],case_describe)
            self.assertEqual(contactinfo['birthday'].strftime('%Y-%m-%d %H:%M'),r.json()['birthday'],case_describe)
            self.assertEqual(contactinfo['state'],r.json()['state'],case_describe)
            self.assertEqual(contactinfo['street'],r.json()['street'],case_describe)
            self.assertEqual(contactinfo['city'],r.json()['city'],case_describe)
            # self.assertEqual(contactinfo['companyname'],r.json()['companyname'],case_describe)
            # self.assertEqual(contactinfo['job'],r.json()['job'],case_describe)
            la =[]
            for ii in range(len(r.json()['labels'])):
                la.append(r.json()['labels'][ii]['id'])
            for i in range(len(contactinfo['labels'])):
                self.assertIn(contactinfo['labels'][i],la,case_describe)
            self.assertEqual(len(contactinfo['labels']),len(la),case_describe)
        self.assertEqual(r.status_code,200,case_describe)     