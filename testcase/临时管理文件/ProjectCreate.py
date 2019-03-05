import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import  json 
import uuid


sheet_name = "ProjectCreate"
api='api/Project/create'

excel = ReadExcl.Xlrd()

@ddt.ddt
class ProjectCreate(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_ProjectCreate(self, data):
        excel = ReadExcl.Xlrd()
        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        projectName = str(data["projectName"])
        department = str(data["department"])
        if department =='investment':
            amount = int(data["amount"])
            estimate = int(data["estimate"])
            conditions = str(data["conditions"])
            commitment = str(data["commitment"])
            newSituation = str(data["newSituation"])
            departmentId = readconfig.get_basedata('investmentdepartmentId')
            payload ={
                "projectName": projectName,
                "customerId": readconfig.get_customer("investmentcustomerid"),
                "status": 63,
                "departmentId": departmentId,
                "investmentProject": {
                "amount": amount,
                "estimate": estimate,
                "conditions": conditions,
                "commitment": commitment,
                "newSituation": newSituation
                }
            }
        elif department =='factoring':
            sellerName = str(data["sellerName"])
            buyerName = str(data["buyerName"])
            businessTarget = str(data["businessTarget"])
            businessType = str(data["businessType"])
            guarantee = str(data["guarantee"])
            quota = int(data["quota"])
            period = str(data["period"])
            interestRate1= str(data["interestRate1"])
            interestRate2= str(data["interestRate2"])
            interestRate3= str(data["interestRate3"])
            departmentId = readconfig.get_basedata('factoringdepartmentId')
            payload ={
                "projectName": projectName,
                "customerId": readconfig.get_customer("actoringdecustomerid"),
                "status": 63,
                "departmentId": departmentId,
                "factoringProject": {
                    "sellerName": sellerName,
                    "buyerName": buyerName,
                    "businessTarget": businessTarget,
                    "businessType": businessType,
                    "guarantee": guarantee,
                    "quota": quota,
                    "period": period,
                    "interestRate1": interestRate1,
                    "interestRate2": interestRate2,
                    "interestRate3": interestRate3
                }
            }
        case_describe = str(data["case_describe"])
        expected_code = int(data["expected_code"])

        #填写求求参数h
        url = readconfig.get_basedata('crm_url')+api
        session =  readconfig.get_basedata('session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        r = requests.post(url=url,data = json.dumps(payload),headers = headers)
        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()

        #数据对比
        if r.status_code==200 or r.status_code ==204:
            projectinfo = readdb.GetProjectDetailsinfo(requestid)

            if department =='investment':
                self.assertEqual(projectinfo['projectname'],projectName,case_describe)
                self.assertEqual(projectinfo['status'],63,case_describe)
                self.assertEqual(projectinfo['departmentid'],int(departmentId),case_describe)
                self.assertEqual(int(projectinfo['amount']),int(amount),case_describe)
                self.assertEqual(int(projectinfo['estimate']),int(estimate),case_describe)
                self.assertEqual(projectinfo['conditions'],conditions,case_describe)
                self.assertEqual(projectinfo['commitment'],commitment,case_describe)
                self.assertEqual(projectinfo['newsituation'],newSituation,case_describe)
                readconfig.set_project('projectinvestmentid',requestid)
            elif department =='factoring':
                self.assertEqual(projectinfo['projectname'],projectName,case_describe)
                self.assertEqual(projectinfo['status'],63,case_describe)
                self.assertEqual(projectinfo['departmentid'],int(departmentId),case_describe)
                self.assertEqual(projectinfo['buyername'],buyerName,case_describe)
                self.assertEqual(projectinfo['businesstarget'],businessTarget,case_describe)
                self.assertEqual(projectinfo['businesstype'],businessType,case_describe)
                self.assertEqual(projectinfo['guarantee'],guarantee,case_describe)
                self.assertEqual(projectinfo['quota'],quota,case_describe)
                self.assertEqual(projectinfo['period'],period,case_describe)
                self.assertEqual(int(projectinfo['interestrate1']),int(interestRate1),case_describe)
                self.assertEqual(int(projectinfo['interestrate2']),int(interestRate2),case_describe)
                self.assertEqual(int(projectinfo['interestrate3']),int(interestRate3),case_describe)
                readconfig.set_project('projectfactoringid',requestid)
        self.assertEqual(r.status_code,expected_code,case_describe)

