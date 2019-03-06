import unittest
import ddt
from common import ReadExcl,ReadDB
import ReadConfig 
import requests
import json 

apiversion = 'api/AppVersion'
apiread = 'api/AppVersion/{0}/Read'

sheet_name = "AppVersion"

excel = ReadExcl.Xlrd()


@ddt.ddt
class AppVersion(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.readdb = ReadDB.Pyodbc()
        self.readconfig=ReadConfig.ReadConfig()

        self.readdb.DBDelete("[AppVersionOpenRecord]")
        self.readdb.DBDelete("[AppVersion]")

    @classmethod
    def tearDownClass(self):
        self.readdb.DBClose()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @ddt.data(*excel.get_xls_next(sheet_name))
    def test_AppVersion(self,data):
        isnewversion = str(data["isnewversion"])
        isshow = int(data["isshow"])
        isread = int(data["isread"])
        status = str(data["status"])
        case_describe = str(data["case_describe"])
        expected_code = int(data["expected_code"])

        lastrowid = 0

        excel = ReadExcl.Xlrd()

        session =  self.readconfig.get_basedata('member_session')
        headers = {'Content-Type': "application/json",'Authorization':session}

        if isnewversion != '':
            agentid = self.readconfig.get_basedata('dingding_agentid')
            lastrowid = int(self.readdb.AddVersion(agentid,isnewversion))
            
            self.readconfig.set_dynamicdata('app_versionid',str(lastrowid))
        
        if isshow == 1:
            self.readdb.UpdateVersion()
        
        if isread == 1:
            versionid = self.readconfig.get_dynamicdata('app_versionid')
            url = self.readconfig.get_basedata('crm_url')+apiread.format(versionid)
            r = requests.post(url=url, headers = headers)

            excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
            excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
            excel.save()

            if r.status_code==200:
                openrecord = self.readdb.GetAppVersionOpenRecord(self.readconfig.get_basedata('employee_id'))
                self.assertEqual(self.readconfig.get_basedata('employee_id'),openrecord[0],"版本打开记录版本号未对上,接口："+apiread)
                self.assertEqual(str(versionid),str(openrecord[1]),"版本打开记录版本号未对上,接口："+apiread)
            self.assertEqual(r.status_code,data['expected_code'],"版本打开记录版本号未对上,接口:"+apiread)
            
   
        url = self.readconfig.get_basedata('crm_url')+apiversion
        r = requests.get(url=url, headers = headers)

        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_code"],r.status_code,excel.set_color(r.status_code))
        excel.set_cell(sheet_name,int(data["case_id"]),excel.get_sheet_colname(sheet_name)["result_msg"],r.text,excel.set_color())
        excel.save()

        if r.status_code==200:
            self.assertEqual(str(r.json()['status']),status,case_describe + ",接口：{0}".format(apiversion))
        self.assertEqual(r.status_code,data['expected_code'],case_describe + ",接口：{0}".format(apiversion))
