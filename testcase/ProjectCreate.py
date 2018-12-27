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
            payload ={
                "projectName": projectName,
                "customerId": "87A79C43-D2B0-42B0-9949-9BFB4A2991E3",
                "status": 63,
                "departmentId": readconfig.get_member('investmentdepartmentId'),
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
            payload ={
                "projectName": projectName,
                "customerId": "87A79C43-D2B0-42B0-9949-9BFB4A2991E3",
                "status": 63,
                "departmentId": readconfig.get_member('factoringdepartmentId'),
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

        #填写求求参数h
        url = readconfig.get_url('url')+api
        session =  readconfig.get_member('session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        r = requests.post(url=url,data = json.dumps(payload),headers = headers)
        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()

        #数据对比
        if r.status_code==200 or r.status_code ==204:
            projectinfo = readdb.GetProject(requestid)
        #     customerlabelsid = readdb.GetCustomerLabelsinfo(customerinfo['correlationId'])
        #     self.assertEqual(customerinfo['name'],name,case_describe)
        #     self.assertEqual(customerinfo['shortName'],shortName,case_describe)
        #     self.assertEqual(customerinfo['city'],city,case_describe)
        #     self.assertEqual(customerinfo['state'],state,case_describe)
        #     self.assertEqual(customerinfo['customerProspectId'],str(customerProspectId),case_describe)
        #     self.assertEqual(customerinfo['customerTypeId'],str(customerTypeId),case_describe)
        #     self.assertEqual(customerinfo['customerKind'],str(customerKind),case_describe)
        #     for i in range(len(customerlabelsid)):
        #         self.assertIn(customerlabelsid[i],labels,case_describe)
        #         self.assertEqual(len(customerlabelsid),len(labels),case_describe)

            if department =='investment':
                readconfig.set_project('projectinvestmentid',requestid)
            elif department =='factoring':
                readconfig.set_project('projectfactoringid',requestid)
        # self.assertEqual(r.status_code,data['expected_code'],case_describe)

