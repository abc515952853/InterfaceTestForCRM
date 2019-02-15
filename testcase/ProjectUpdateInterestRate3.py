import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 
import uuid

api='api/Project/{0}/InterestRate3'
sheet_name = "ProjectUpdateInterestRate3"

excel = ReadExcl.Xlrd()

@ddt.ddt
class ProjectUpdateInterestRate3(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_ProjectUpdateInterestRate3(self,data):
        interestrate3 = int(data["interestrate3"])
        department = str(data["department"])
        case_describe = str(data["case_describe"])
        expected_code = int(data["expected_code"])

        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        projectid = readconfig.get_project('projectfactoringid')

        url = readconfig.get_url('crmurl')+api.format(projectid)
        session =  readconfig.get_member('session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        payload ={
            "interestrate3":interestrate3
        }
        r = requests.post(url=url,data = json.dumps(payload),headers = headers)

        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        #数据对比
        if r.status_code==expected_code:
            projectdetails = readdb.GetProjectDetailsinfo(projectid)
            self.assertEqual(projectdetails['interestrate3'],interestrate3,case_describe)
        else:
            self.assertEqual(r.status_code,expected_code,case_describe)   