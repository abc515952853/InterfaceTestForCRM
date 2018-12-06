import unittest
import ddt
from common import ReadExcl
import ReadConfig 
import requests
import  json 
import uuid


sheet_name = "CustomerCreate"
api='api/Customer/create'

excel = ReadExcl.Xlrd()

@ddt.ddt
class TestCustomerCreate(unittest.TestCase): 
    def setUp(self):
        """
        :return:
        """

    def tearDown(self):
        """
        :return:
        """

    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_CustomerCreate(self, data):
        excel = ReadExcl.Xlrd()
        readconfig=ReadConfig.ReadConfig()
        
        #填写求求参数h
        url = readconfig.get_url('url')+api
        session =  readconfig.get_member('session')
        requestid = str(uuid.uuid1())
        headers = {'Content-Type': "application/json",'Authorization':session,"x-requestid":requestid}
        payload ={
            "name": str(data["name"]),
            "shortName": str(data["shortName"]),
            "street": str(data["street"]),
            "city": str(data["city"]),
            "state": str(data["state"]),
            "customerProspectId": int(data["customerProspectId"]),
            "customerTypeId":int(data["customerTypeId"])
            }
        r = requests.post(url=url,data = json.dumps(payload),headers = headers)
        #处理请求数据到excl用例文件
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()
        
        #存储数据到本地config数据文件
        if r.status_code==200 or r.status_code ==204:
            print(r.status_code)
        self.assertEqual(r.status_code,data['expected_code'],data["case_describe"])
