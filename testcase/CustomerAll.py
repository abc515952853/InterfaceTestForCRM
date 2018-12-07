import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import  json 

api='api/Customer'
case_describe = '获取所有客户'

class CustomerAll(unittest.TestCase): 
    def setUp(self):
        """
        :return:
        """

    def tearDown(self):
        """
        :return:
        """

    def test_CustomerAll(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_url('url')+api
        session =  readconfig.get_member('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            customerallid = readdb.GetCustomerAllinfo(readconfig.get_member('employeeid'))
            responecustomerallid = []
            for i in range(len(r.json())):
                responecustomerallid.append(r.json()[i]['id'])
                self.assertIn(r.json()[i]['id'].upper(),customerallid,case_describe)
            self.assertEqual(len(responecustomerallid),len(customerallid),case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)   