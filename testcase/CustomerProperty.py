import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

api='api/Label/Customer/all'
case_describe = '获取客户标签'

class CustomerProperty(unittest.TestCase): 
    def test_CustomerPropertyLabel(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_url('url')+api
        session =  readconfig.get_member('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            customerpropertylabel = readdb.PropertyLabel(readconfig.get_labelmodule('customermodule'))
            for i in range(len(r.json())):
                for ii in range(len(customerpropertylabel)):
                    if r.json()[i]['id'] == customerpropertylabel[ii]['id']:
                        self.assertEqual(r.json()[i]['groupName'],customerpropertylabel[ii]['groupname'],case_describe)
                        self.assertEqual(r.json()[i]['departmentId'],customerpropertylabel[ii]['departmentid'],case_describe)
                        # self.assertEqual(r.json()[i]['functionModule'],contactpropertylabel[ii]['functionmodule'],case_describe)
                        self.assertEqual(r.json()[i]['isMultiple'],customerpropertylabel[ii]['ismultiple'],case_describe)
                        self.assertEqual(r.json()[i]['backgroundColor'],customerpropertylabel[ii]['backgroundcolor'],case_describe)
                        self.assertEqual(r.json()[i]['foregroundColor'],customerpropertylabel[ii]['foregroundcolor'],case_describe)

                        for iii in range(len(r.json()[i]['labels'])):
                            for iiii in range(len(customerpropertylabel[ii]['labels'])):
                                if r.json()[i]['labels'][iii]['id'] == customerpropertylabel[ii]['labels'][iiii]['id']:
                                    self.assertEqual(r.json()[i]['labels'][iii]['name'],r.json()[i]['labels'][iii]['name'],case_describe)
                                    self.assertEqual(len(r.json()[i]['labels']),len(customerpropertylabel[ii]['labels']),case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)  


