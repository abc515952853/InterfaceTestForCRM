import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 
import uuid

api='api/Customer/{0}/labels'
sheet_name = "CustomerUpdateLabel"

excel = ReadExcl.Xlrd()

@ddt.ddt
class CustomerUpdateLabel(unittest.TestCase): 
    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_CustomerUpdateLabel(self,data):
        labels = list(map(int,str(data["labels"]).split(',')))
        customertab = str(data["customertab"])
        case_describe = str(data["case_describe"])

        readconfig=ReadConfig.ReadConfig()
        readdb = ReadDB.Pyodbc()

        correlationid = readconfig.get_customer(customertab)
        url = readconfig.get_url('crmurl')+api.format(correlationid)
        session =  readconfig.get_member('session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        payload ={
            "labelIds":labels
        }
        r = requests.post(url=url,data = json.dumps(payload),headers = headers)

        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        #数据对比
        if r.status_code==200:
            customerlabelsid = readdb.GetCustomerLabelsinfo(correlationid)
            for i in range(len(customerlabelsid)):
                self.assertIn(customerlabelsid[i],labels,case_describe)
            self.assertEqual(len(customerlabelsid),len(labels),case_describe)
        else:
            self.assertEqual(r.status_code,200,case_describe)   