import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

api='api/Customer/accessorial?key=&departmentId=&pageIndex=1&pageSize=1000'
case_describe = '获取分享给我的客户'

class CustomerAccessorial(unittest.TestCase): 
    def test_CustomerAccessorial(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_url('url')+api
        session =  readconfig.get_member('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            customeraccessorialid = readdb.GetCustomerAccessorialinfo(readconfig.get_member('employeeid'))
            responecustomeraccessorialid = []
            for i in range(len(r.json())):
                responecustomeraccessorialid.append(r.json()[i]['id'])
                self.assertIn(r.json()[i]['id'].upper(),customeraccessorialid,case_describe)
            readconfig.set_customer('customeraccessorialid',r.json()[0]['id'])
            self.assertEqual(len(responecustomeraccessorialid),len(customeraccessorialid),case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)   