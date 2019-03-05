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
        self.cf.read(configPath,encoding='utf-8')

    #获取基础信息
    def get_basedata(self,name):
        value = self.cf.get("BASEDATA",name)
        return value
    
    #重设基础信息
    def set_basedata(self,name,value):
        self.cf.set("BASEDATA",name,value)
        self.save()

    #获取动态信息
    def get_dynamicdata(self,name):
        value = self.cf.get("DYNAMICDATA",name)
        return value

    #重设动态信息
    def set_dynamicdata(self,name,value):
        self.cf.set("DYNAMICDATA",name,value)
        self.save()

    #写入ini文件
    def save(self):
        self.cf.write(open(configPath, "w"))

        
# if __name__ == "__main__":
#     a = ReadConfig()
#     a.get_url('url')