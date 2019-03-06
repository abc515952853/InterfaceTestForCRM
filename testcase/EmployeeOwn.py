import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

api = 'api/Employee/Own'
case_describe = '查询当前登录员工信息'

class EmployeeOwn(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.readdb = ReadDB.Pyodbc()
        self.readconfig=ReadConfig.ReadConfig()

    @classmethod
    def tearDownClass(self):
        self.readdb.DBClose()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_EmployeeOwn(self):
        self.readconfig=ReadConfig.ReadConfig()
        self.readdb = ReadDB.Pyodbc()

        url = self.readconfig.get_basedata('hr_url')+api
        session =  self.readconfig.get_basedata('member_session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            employeeinfo = self.readdb.GetEmployinfo(self.readconfig.get_basedata('employee_id'))
            self.assertEqual(r.json()['isSenior'],employeeinfo['isSenior'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(r.json()['workPlace'],employeeinfo['workPlace'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(r.json()['avatar'],employeeinfo['avatar'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(r.json()['jobNumber'],employeeinfo['jobNumber'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(r.json()['position'],employeeinfo['position'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(r.json()['mobile'],employeeinfo['mobile'],case_describe + ",接口：{0}".format(api))
            self.assertEqual(r.json()['name'],employeeinfo['name'],case_describe + ",接口：{0}".format(api))
            if len(r.json()['departments']) == len(employeeinfo['departments']):
                departmentids = []
                for i in range(len(r.json()['departments'])):
                    for ii in range(len(employeeinfo['departments'])):
                        if r.json()['departments'][i]['departmentId'] == employeeinfo['departments'][ii]['departmentId']:
                            self.assertEqual(r.json()['departments'][i]['isLeader'],employeeinfo['departments'][ii]['isLeader'])
                            self.assertEqual(r.json()['departments'][i]['name'],employeeinfo['departments'][ii]['name'])
                            departmentids.append(str(r.json()['departments'][i]['departmentId']))
                self.readconfig.set_dynamicdata('member_departmentid',','.join(departmentids))
            else:
                self.assertEqual(len(r.json()['departments']),len(employeeinfo['departments']),case_describe + ",接口：{0}".format(api))
        self.assertEqual(r.status_code,200,case_describe + ",接口：{0}".format(api))
            


