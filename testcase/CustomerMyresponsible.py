import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

api='api/Customer?key=&departmentId=&pageIndex=1&pageSize=100'
case_describe = '获取我负责的客户'

class CustomerMyresponsible(unittest.TestCase): 
    def test_CustomerMyresponsible(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_url('url')+api
        session =  readconfig.get_member('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            customermyresponsibleid = readdb.GetCustomerMyresponsibleinfo(readconfig.get_member('employeeid'))
            responecustomermyresponsibleid = []
            for i in range(len(r.json()['list'])):
                responecustomermyresponsibleid.append(r.json()['list'][i]['id'])
                self.assertIn(r.json()['list'][i]['id'].upper(),customermyresponsibleid,case_describe)
            readconfig.set_customer('customerresponsibleid',r.json()['list'][0]['id'])
            self.assertEqual(len(responecustomermyresponsibleid),len(customermyresponsibleid),case_describe)
            self.assertEqual(r.json()['count'],len(customermyresponsibleid),case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)   