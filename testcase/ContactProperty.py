import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

contactlabel='api/Label/Contact/all'
case_describe = '获取联系人标签'

class ContactProperty(unittest.TestCase): 
    def test_ContactPropertyLabel(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_url('url')+contactlabel
        session =  readconfig.get_member('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            contactpropertylabel = readdb.ContactPropertyLabel(readconfig.get_labelmodule('contactmodule'))
            for i in range(len(r.json())):
                for ii in range(len(contactpropertylabel)):
                    if r.json()[i]['id'] == contactpropertylabel[ii]['id']:
                        self.assertEqual(r.json()[i]['groupName'],contactpropertylabel[ii]['groupname'],case_describe)
                        self.assertEqual(r.json()[i]['departmentId'],contactpropertylabel[ii]['departmentid'],case_describe)
                        # self.assertEqual(r.json()[i]['functionModule'],contactpropertylabel[ii]['functionmodule'],case_describe)
                        self.assertEqual(r.json()[i]['isMultiple'],contactpropertylabel[ii]['ismultiple'],case_describe)
                        for iii in range(len(r.json()[i]['labels'])):
                            for iiii in range(len(contactpropertylabel[ii]['labels'])):
                                if r.json()[i]['labels'][iii]['id'] == contactpropertylabel[ii]['labels'][iiii]['id']:
                                    self.assertEqual(r.json()[i]['labels'][iii]['name'],r.json()[i]['labels'][iii]['name'],case_describe)
                                    self.assertEqual(len(r.json()[i]['labels']),len(contactpropertylabel[ii]['labels']),case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)  
