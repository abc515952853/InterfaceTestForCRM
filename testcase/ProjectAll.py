import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 
import uuid

api='api/Project/{}/all'
sheet_name = "ProjectAll"

excel = ReadExcl.Xlrd()

@ddt.ddt
class ProjectAll(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_ProjectAll(self,data):
        peojecttype = str(data["peojecttype"])
        case_describe = str(data["case_describe"])
        expected_code = int(data["expected_code"])

        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        customerid = readconfig.get_customer(peojecttype)
        url = readconfig.get_url('crmurl')+api.format(customerid) 

        session =  readconfig.get_basedata('session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        r = requests.get(url=url, headers = headers)

        if r.status_code==200:
            projectincustomerid = readdb.GetProjectInCustomerinfo(customerid)
            responeprojectincustomerid = []
            for i in range(len(r.json())):
                responeprojectincustomerid.append(r.json()[i]['id'])
                self.assertIn(r.json()[i]['id'].upper(),projectincustomerid,case_describe)
            self.assertEqual(len(responeprojectincustomerid),len(projectincustomerid),case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)   