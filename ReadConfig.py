import os
import codecs
import configparser

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")


class ReadConfig:
    def __init__(self):
        fd = open(configPath)
        data = fd.read()

        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    #获取URL信息
    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value
    
    #获取DB信息
    def get_db(self,name):
        value = self.cf.get("DB",name)
        return value

    #获取TESTCASE信息
    def get_xls(self,name):
        value = self.cf.get("TESTCASE",name)
        return value

    #重设TESTCASE信息    
    def set_xls(self,name,value):
        self.cf.set("MEMTESTCASEBER",name,value)
    
    #获取MEMBER信息
    def get_member(self,name):
        value = self.cf.get("MEMBER",name)
        return value
    
    #重设MEMBER信息
    def set_member(self,name,value):
        self.cf.set("MEMBER",name,value)
        self.save()

    #获取CLIENT信息
    def get_client(self,name):
        value = self.cf.get("CLIENT",name)
        return value

    #重设CLIENT信息
    def set_client(self,name,value):
        self.cf.set("CLIENT",name,value)
        self.save()

    #写入ini文件
    def save(self):
        self.cf.write(open(configPath, "w"))

    #获取EMAIL信息
    def get_email(self,name):
        value = self.cf.get("EMAIL",name)
        return value
           

# if __name__ == "__main__":
#     a = ReadConfig()
#     a.get_url('url')