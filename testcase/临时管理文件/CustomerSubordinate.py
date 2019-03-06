import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

api='api/v1.2/Customer/Subordinate?key=&departmentIds=&pageIndex=1&pageSize=1000'
case_describe = '获取我下级的客户'

class CustomerSubordinate(unittest.TestCase): 
    def test_CustomerSubordinate(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_basedata('crm_url')+api
        session =  readconfig.get_basedata('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            customersubordinateid = readdb.GetCustomerSubordinateinfo(readconfig.get_basedata('employeeid'))
            responecustomersubordinateid = []
            for i in range(len(r.json()['list'])):
                responecustomersubordinateid.append(r.json()['list'][i]['id'])
                self.assertIn(r.json()['list'][i]['id'].upper(),customersubordinateid,case_describe + ",接口：{0}".format(api))
            self.assertEqual(len(responecustomersubordinateid),len(customersubordinateid),case_describe + ",接口：{0}".format(api))
            self.assertEqual(r.json()['count'],len(customersubordinateid),case_describe + ",接口：{0}".format(api))
        else:
            self.assertEqual(r.status_code,200,case_describe + ",接口：{0}".format(api))   