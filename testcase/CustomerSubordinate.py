import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

api='api/Customer/subordinate?key=&departmentId=&pageIndex=1&pageSize=1000'
case_describe = '获取我下级的客户'

class CustomerSubordinate(unittest.TestCase): 
    def test_CustomerSubordinate(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_url('url')+api
        session =  readconfig.get_member('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            customersubordinateid = readdb.GetCustomerSubordinateinfo(readconfig.get_member('employeeid'))
            responecustomersubordinateid = []
            for i in range(len(r.json())):
                responecustomersubordinateid.append(r.json()[i]['id'])
                self.assertIn(r.json()[i]['id'].upper(),customersubordinateid,case_describe)
            readconfig.set_customer('customersubordinateid',r.json()[0]['id'])
            self.assertEqual(len(responecustomersubordinateid),len(customersubordinateid),case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)   