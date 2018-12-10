import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

apitype='api/Customer/Types'
apiprospects='api/Customer/Prospects'
apilabels='api/Customer/labels'
case_describe = '获取客户属性'

class CustomerProperty(unittest.TestCase): 
    def test_CustomerPropertyTypes(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_url('url')+apitype
        session =  readconfig.get_member('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            customerpropertytypes = readdb.CustomerPropertyTypes()
            for i in range(len(r.json())):
                for ii in range(len(customerpropertytypes)):
                    if r.json()[i]['id'] == customerpropertytypes[ii][0]:
                        self.assertEqual(r.json()[i]['id'],customerpropertytypes[ii][0],case_describe)
                        self.assertEqual(r.json()[i]['title'],customerpropertytypes[ii][1],case_describe)
                        self.assertEqual(r.json()[i]['description'],customerpropertytypes[ii][2],case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)  

    def test_CustomerPropertyProspect(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_url('url')+apiprospects
        session =  readconfig.get_member('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            customerpropertyprospects = readdb.CustomerPropertyProspect()
            for i in range(len(r.json())):
                for ii in range(len(customerpropertyprospects)):
                    if r.json()[i]['id'] == customerpropertyprospects[ii][0]:
                        self.assertEqual(r.json()[i]['id'],customerpropertyprospects[ii][0],case_describe)
                        self.assertEqual(r.json()[i]['title'],customerpropertyprospects[ii][1],case_describe)
                        self.assertEqual(r.json()[i]['description'],customerpropertyprospects[ii][2],case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)

    def test_CustomerPropertyLabels(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_url('url')+apilabels
        session =  readconfig.get_member('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            customerpropertylabel = readdb.CustomerPropertyLabels()
            for i in range(len(customerpropertylabel)):
                for ii in range(len(r.json())):
                    if customerpropertylabel[i][0] == r.json()[ii]['id']:
                        self.assertEqual(customerpropertylabel[i][1],r.json()[ii]['groupName'])
                        self.assertEqual(customerpropertylabel[i][2],r.json()[ii]['backgroundColor'])
                        self.assertEqual(customerpropertylabel[i][3],r.json()[ii]['foregroundColor'])
                        for iii in range(len(r.json()[ii]['labels'])):
                            if customerpropertylabel[i][4] ==r.json()[ii]['labels'][iii]['id']:
                                self.assertEqual(customerpropertylabel[i][5],r.json()[ii]['labels'][iii]['name'])
