import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

api='api/v1.2/Customer/My?key=&departmentIds=&pageIndex=1&pageSize=100'
case_describe = '获取我负责的客户'

class CustomerMy(unittest.TestCase): 
    def test_CustomerMy(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_basedata('crm_url')+api
        session =  readconfig.get_basedata('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)

        if r.status_code==200:
            customermyresponsibleid = readdb.GetCustomerMyinfo(readconfig.get_basedata('employeeid'))
            responecustomermyresponsibleid = []
            for i in range(len(r.json()['list'])):
                responecustomermyresponsibleid.append(r.json()['list'][i]['id'])
                self.assertIn(r.json()['list'][i]['id'].upper(),customermyresponsibleid,case_describe)
            self.assertEqual(len(responecustomermyresponsibleid),len(customermyresponsibleid),case_describe)
            self.assertEqual(r.json()['count'],len(customermyresponsibleid),case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)   