import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

api = 'api/Employee/Own'
case_describe = '查询当前登录员工信息'

class EmployeeOwn(unittest.TestCase): 
    def test_EmployeeOwn(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_url('hrurl')+api
        session =  readconfig.get_basedata('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            employeeinfo = readdb.GetEmployinfo(readconfig.get_basedata('employeeid'))
            self.assertEqual(r.json()['isSenior'],employeeinfo['isSenior'],case_describe)
            self.assertEqual(r.json()['workPlace'],employeeinfo['workPlace'],case_describe)
            self.assertEqual(r.json()['avatar'],employeeinfo['avatar'],case_describe)
            self.assertEqual(r.json()['jobNumber'],employeeinfo['jobNumber'],case_describe)
            self.assertEqual(r.json()['position'],employeeinfo['position'],case_describe)
            self.assertEqual(r.json()['mobile'],employeeinfo['mobile'],case_describe)
            self.assertEqual(r.json()['name'],employeeinfo['name'],case_describe)
            if len(r.json()['departments']) == len(employeeinfo['departments']):
                departmentids = []
                for i in range(len(r.json()['departments'])):
                    for ii in range(len(employeeinfo['departments'])):
                        if r.json()['departments'][i]['departmentId'] == employeeinfo['departments'][ii]['departmentId']:
                            self.assertEqual(r.json()['departments'][i]['isLeader'],employeeinfo['departments'][ii]['isLeader'])
                            self.assertEqual(r.json()['departments'][i]['name'],employeeinfo['departments'][ii]['name'])
                            departmentids.append(str(r.json()['departments'][i]['departmentId']))
                readconfig.set_basedata('departmentid',','.join(departmentids))
            else:
                self.assertEqual(len(r.json()['departments']),len(employeeinfo['departments']),case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)
            


