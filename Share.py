#! /usr/bin/python3
import json
import pymysql
from Share import UPload, Download

class Share(object):
    def __init__(self):
        """
        功能选择.
        """
        while(True):
            print('===== ===== ===== ===== ===== ===== ===== =====')
            __command = input('UPload/Download -> Share, Quit - > Exit\n')
            # 退出
            if(__command.upper() == 'QUIT' or __command.upper() == 'EXIT'):
                break
            else:
                # 检查参数
                if(len(__command.split(' -d ')) != 2):
                    print('Need -d(Dir) Parameter')
                    continue
                # 执行指令
                __instruction = __command.split(' -d ')[0]
                __parameter = __command.split(' -d ')[1]
                # 上传
                if(__instruction.upper() == 'UPLOAD'):
                    self.__UPload(__parameter)
                # 下载
                elif(__instruction.upper() == 'DOWNLOAD'):
                    self.__Download(__parameter)
                else:
                    print('Command Error')

    def __DBInit(self):
        """
        数据库连接初始化
        """
        #新建连接
        with open('config.json') as __configJson:
            __config = json.load(__configJson)
        __dbConfig = __config['connections'][int(__config['connectionSelect'])]
        try:
            self.__connection = pymysql.connect(host=__dbConfig['host'],
                                           database=__dbConfig['database'],
                                           user=__dbConfig['user'],
                                           password=__dbConfig['password'])
            return True
        #连接字典错误
        except Exception as ex:
            print('Exception:\n' + str(ex))
            return False

    def __UPload(self, dir):
        """
        将指定目录上传.

        Args:
            dir:指定目录
        """
        print('You can ignore charset waring')
        __upload = UPload.UPload()
        __upload.GetUPloadFiles(dir)
        __upload.UPloadToDB()
   
    def __Download(self, dir):
        """
        下载指定文件夹.

        Args:
            folderName:待下载文件夹
        """
        if (not self.__DBInit()):
            return
        try:
            __cursor = self.__connection.cursor()
            __cursor.execute("SHOW TABLES")
            __tableList = ""
            for __table in __cursor.fetchall():
                __tableList += __table[0] + '\t'
        except Exception as ex:
            print('Get Folder From DB ERROR:\n' + str(ex))
            return
        __folderName = input(__tableList + "\nDownload From:\n")#保存路径
        __download = Download.Download()
        __download.DownloadFromDB(__folderName, dir)
        __download.WriteTOFiles()

if __name__ == "__main__":
    Share()