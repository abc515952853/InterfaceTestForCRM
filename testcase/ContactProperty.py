import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

label='api/Label'
case_describe = '获取联系人属性'

class ContactProperty(unittest.TestCase): 
    def test_ContactPropertyLabel(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        # url = readconfig.get_url('url')+apitype
        # session =  readconfig.get_member('session')
        # headers = {'Content-Type': "application/json",'Authorization':session}
        # r = requests.get(url=url, headers = headers)
        # if r.status_code==200:
        #     customerpropertytypes = readdb.CustomerPropertyTypes()
        #     for i in range(len(r.json())):
        #         for ii in range(len(customerpropertytypes)):
        #             if r.json()[i]['id'] == customerpropertytypes[ii][0]:
        #                 self.assertEqual(r.json()[i]['id'],customerpropertytypes[ii][0],case_describe)
        #                 self.assertEqual(r.json()[i]['title'],customerpropertytypes[ii][1],case_describe)
        #                 self.assertEqual(r.json()[i]['description'],customerpropertytypes[ii][2],case_describe)
        # else:
        #     self.assertEqual(r.status_code,200,case_describe)  
