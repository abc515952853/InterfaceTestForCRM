import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 
import uuid

api='api/Project/{0}'
sheet_name = "ProjectDetail"

excel = ReadExcl.Xlrd()

@ddt.ddt
class ProjectDetail(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_ProjectDetail(self,data):
        peojecttype = str(data["peojecttype"])
        case_describe = str(data["case_describe"])
        expected_code = int(data["expected_code"])

        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        projectid = readconfig.get_project(peojecttype)

        url = readconfig.get_url('url')+api.format(projectid)
        session =  readconfig.get_member('session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        r = requests.get(url=url,headers = headers)

        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        #数据对比
        if r.status_code==200 or r.status_code ==204:
            projectinfo = readdb.GetProjectDetailsinfo(projectid)

            if peojecttype =='projectinvestmentid':
                self.assertEqual(projectinfo['projectname'],r.json()['projectName'],case_describe)
                self.assertEqual(projectinfo['departmentid'],r.json()['departmentId'],case_describe)
                self.assertEqual(int(projectinfo['amount']),int(r.json()['investment']['amount']),case_describe)
                self.assertEqual(int(projectinfo['estimate']),int(r.json()['investment']['estimate']),case_describe)
                self.assertEqual(projectinfo['conditions'],r.json()['investment']['conditions'],case_describe)
                self.assertEqual(projectinfo['commitment'],r.json()['investment']['commitment'],case_describe)
                self.assertEqual(projectinfo['newsituation'],r.json()['investment']['newSituation'],case_describe)
                readconfig.set_project('projectinvestmentid',requestid)
            elif peojecttype =='projectfactoringid':
                self.assertEqual(projectinfo['projectname'],r.json()['projectName'],case_describe)
                self.assertEqual(projectinfo['departmentid'],r.json()['departmentId'],case_describe)
                self.assertEqual(projectinfo['sellername'],r.json()['factoring']['sellerName'],case_describe)
                self.assertEqual(projectinfo['buyername'],r.json()['factoring']['buyerName'],case_describe)
                self.assertEqual(projectinfo['businesstarget'],r.json()['factoring']['businessTarget'],case_describe)
                self.assertEqual(projectinfo['businesstype'],r.json()['factoring']['businessType'],case_describe)
                self.assertEqual(projectinfo['guarantee'],r.json()['factoring']['guarantee'],case_describe)
                self.assertEqual(projectinfo['quota'],r.json()['factoring']['quota'],case_describe)
                self.assertEqual(projectinfo['period'],r.json()['factoring']['period'],case_describe)
                self.assertEqual(int(projectinfo['interestrate1']),r.json()['factoring']['interestRate1'],case_describe)
                self.assertEqual(int(projectinfo['interestrate2']),r.json()['factoring']['interestRate2'],case_describe)
                self.assertEqual(int(projectinfo['interestrate3']),r.json()['factoring']['interestRate3'],case_describe)
                readconfig.set_project('projectfactoringid',requestid)
        self.assertEqual(r.status_code,expected_code,case_describe) 