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
    
    #获取ini所有Session
    def get_sections(self):
        sections =  self.cf.sections()
        return sections

    #获取ini所有Session中的options
    def get_options(self,section):
        options =  self.cf.options(section)
        return options

    #追加动态信息
    def append_dynamicdata(self,name,value):
        if name in self.get_options("DYNAMICDATA"):
            contactids = self.get_dynamicdata(name)+','+value
            self.set_dynamicdata(name,contactids)
        else:
            self.set_dynamicdata(name,value)

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