import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

# api1='api/Label/Customer/all'
api2 = 'api/v1.2/Customer/Add'
case_describe = '获取客户属性'

class CustomerProperty(unittest.TestCase): 
    # def test_CustomerPropertyLabel(self):
    #     readconfig=ReadConfig.ReadConfig()
    #     readdb = ReadDB.Pyodbc()

    #     url = readconfig.get_url('url')+api1
    #     session =  readconfig.get_member('session')
    #     headers = {'Content-Type': "application/json",'Authorization':session}
    #     r = requests.get(url=url, headers = headers)
    #     print(r.json())
    #     if r.status_code==200:
    #         customerpropertylabel = readdb.PropertyLabel(readconfig.get_labelmodule('customermodule'))
    #         for i in range(len(r.json())):
    #             for ii in range(len(customerpropertylabel)):
    #                 if r.json()[i]['id'] == customerpropertylabel[ii]['id']:
    #                     self.assertEqual(r.json()[i]['groupName'],customerpropertylabel[ii]['groupname'],case_describe)
    #                     self.assertEqual(r.json()[i]['departmentId'],customerpropertylabel[ii]['departmentid'],case_describe)
    #                     # self.assertEqual(r.json()[i]['functionModule'],contactpropertylabel[ii]['functionmodule'],case_describe)
    #                     self.assertEqual(r.json()[i]['isMultiple'],customerpropertylabel[ii]['ismultiple'],case_describe)
    #                     self.assertEqual(r.json()[i]['backgroundColor'],customerpropertylabel[ii]['backgroundcolor'],case_describe)
    #                     self.assertEqual(r.json()[i]['foregroundColor'],customerpropertylabel[ii]['foregroundcolor'],case_describe)

    #                     for iii in range(len(r.json()[i]['labels'])):
    #                         for iiii in range(len(customerpropertylabel[ii]['labels'])):
    #                             if r.json()[i]['labels'][iii]['id'] == customerpropertylabel[ii]['labels'][iiii]['id']:
    #                                 self.assertEqual(r.json()[i]['labels'][iii]['name'],r.json()[i]['labels'][iii]['name'],case_describe)
    #                                 self.assertEqual(len(r.json()[i]['labels']),len(customerpropertylabel[ii]['labels']),case_describe)
    #     else:
    #         self.assertEqual(r.status_code,200,case_describe)

    def test_CustomerProperty(self):
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        url = readconfig.get_url('url')+api2
        session =  readconfig.get_member('session')
        headers = {'Content-Type': "application/json",'Authorization':session}
        r = requests.get(url=url, headers = headers)
        if r.status_code==200:
            customerpropertylabel = readdb.PropertyLabel(readconfig.get_labelmodule('customermodule'))
            for i in range(len(r.json()['customerLabel'])):
                for ii in range(len(customerpropertylabel)):
                    if r.json()['customerLabel'][i]['id'] == customerpropertylabel[ii]['id']:
                        self.assertEqual(r.json()['customerLabel'][i]['groupName'],customerpropertylabel[ii]['groupname'],case_describe)
                        self.assertEqual(r.json()['customerLabel'][i]['departmentId'],customerpropertylabel[ii]['departmentid'],case_describe)
                        # self.assertEqual(r.json()['customerLabel'][i]['functionModule'],contactpropertylabel[ii]['functionmodule'],case_describe)
                        self.assertEqual(r.json()['customerLabel'][i]['isMultiple'],customerpropertylabel[ii]['ismultiple'],case_describe)
                        self.assertEqual(r.json()['customerLabel'][i]['backgroundColor'],customerpropertylabel[ii]['backgroundcolor'],case_describe)
                        self.assertEqual(r.json()['customerLabel'][i]['foregroundColor'],customerpropertylabel[ii]['foregroundcolor'],case_describe)

                        for iii in range(len(r.json()['customerLabel'][i]['labels'])):
                            for iiii in range(len(customerpropertylabel[ii]['labels'])):
                                if r.json()['customerLabel'][i]['labels'][iii]['id'] == customerpropertylabel[ii]['labels'][iiii]['id']:
                                    self.assertEqual(r.json()['customerLabel'][i]['labels'][iii]['name'],r.json()['customerLabel'][i]['labels'][iii]['name'],case_describe)
                                    self.assertEqual(len(r.json()['customerLabel'][i]['labels']),len(customerpropertylabel[ii]['labels']),case_describe)

            myDepartments =  readdb.GetMyDepartments(readconfig.get_member('employeeid'))
            for a in range(len(r.json()['myDepartments'])):
                for aa in range(len(myDepartments)):
                    if r.json()['myDepartments'][a]['id'] == myDepartments[aa]['id']:
                        self.assertEqual(r.json()['myDepartments'][a]['name'],myDepartments[aa]['name'],case_describe)
                        self.assertEqual(r.json()['myDepartments'][a]['queryLabelDepartmentId'],myDepartments[aa]['querylabeldepartmentid'],case_describe)
            self.assertEqual(len(r.json()['myDepartments']),len(myDepartments),case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)
            


