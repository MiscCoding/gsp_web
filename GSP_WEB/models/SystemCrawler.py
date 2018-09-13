from sqlalchemy import and_

from GSP_WEB.models.CommonCode import CommonCode


class SystemCrawler():

    def __init__(self):
        self.extensions = "tar,7z,zip,xz,gz,rar,zip,lzh,lha,pdf,dll,xls,xlsx,xlsm,xlsb,mht,mhtml,xltx,xltm,xlt,csv,prn,dif,slk,xlam,xla,xps,ods,xlw,doc,docx,docm,dotx,dot,rtf,odt,wps,ppt,pptx,pptm,potx,pot,thmx,ppsx,ppsm,pps,ppam,ppa,mp4,wmv,emf,odp,hwp,cell,show,swf,js,bat,exe,msi,apk,png,jpg,jpeg,gif"
        self.depth = 2
        self.max_size = 200000000
        self.timeout = 5

    def getOptions(self):
        try:
            self.depth = CommonCode.query.filter(and_(CommonCode.GroupCode=="cl", CommonCode.Code=="001")).first().EXT1
            self.extensions = CommonCode.query.filter(and_(CommonCode.GroupCode=="cl", CommonCode.Code=="002")).first().EXT1
            self.max_size = CommonCode.query.filter(and_(CommonCode.GroupCode=="cl", CommonCode.Code=="003")).first().EXT1
            self.timeout = CommonCode.query.filter(and_(CommonCode.GroupCode == "cl", CommonCode.Code == "004")).first().EXT1
        except Exception:
            return