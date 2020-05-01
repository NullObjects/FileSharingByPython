import os
import json
import pymysql
from Model import FileModel, PackageModel


class Download(object):
    """
    数据流写入文件类.
    """
    def __init__(self):
        """
        初始化写入.
        """
        self.AllFiles = []

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

    def DownloadFromDB(self, folderName, dir):
        """
        从数据库下载数据.

        Args:
            folderName:选中的数据
            dir:下载目录
        """
        if (not self.__DBInit()):
            return
        if (not dir.endswith(os.sep)):
            dir += os.sep

        try:
            self.__cursor = self.__connection.cursor()
            # 查询总量
            self.__cursor.execute("SELECT COUNT(PackageID) FROM " + folderName)
            self.Count = int(self.__cursor.fetchone()[0])
            self.Finshed = 0
            if (self.Count != 0):
                #查询文件名
                self.__cursor.execute("SELECT DISTINCT PackageName FROM " +
                                      folderName)
                __Files = self.__cursor.fetchall()
                for __file in __Files:
                    __currentName = __file[0].replace('\\', os.sep)
                    __currentName = __file[0].replace('/', os.sep)
                    # 添加文件
                    self.AllFiles.append(
                        FileModel.FileModel(dir + __file[0].replace(
                            '\\', os.sep).replace('/', os.sep)))
                    # 查询文件包数量
                    self.__cursor.execute(
                        "SELECT COUNT(PackageIndex) FROM " + folderName +
                        " WHERE PackageName = %s", (__file[0]))
                    __packageCount = int(self.__cursor.fetchone()[0])
                    # 遍历获取文件包
                    for __index in range(__packageCount):
                        self.__cursor.execute("SELECT PackageData FROM " + folderName + " WHERE PackageName = %s AND PackageIndex = %s", (__file[0], __index))
                        # 添加文件包
                        self.AllFiles[len(self.AllFiles) - 1].Packages.append(
                            PackageModel.PackageModel(
                                __index,
                                __file[0].replace('\\',
                                                  os.sep).replace('/', os.sep),
                                self.__cursor.fetchone()[0]))
                        #刷新进度显示
                        self.Finshed += 1
                        __persent = int(self.Finshed / self.Count * 50)
                        print("\r",
                              '[' + '=' * __persent + '-' * (50 - __persent) +
                              ']' + str(self.Finshed) + '/' + str(self.Count),
                              end='\t\t',
                              flush=True)
                print('GetData Completed')
        except Exception as ex:
            print("GetData Error:\n" + str(ex))
            return

    def __BinaryDataRestoration(self, writeData, fileName):
        """
        二进制数据流写入文件.

        Args:
            writeData: 数据流列表
            fileName: 指定存储文件
        """
        #目录不存在则创建目录
        if (not os.path.exists(os.path.dirname(fileName))):
            os.makedirs(os.path.dirname(fileName))
        #写入数据
        with open(fileName, 'wb') as __writeFile:
            for __data in writeData:
                __writeFile.write(__data)

    def WriteTOFiles(self):
        """
        文件包组合写入.
        """
        #遍历写入文件
        for __file in self.AllFiles:
            __writeData = []
            #遍历添加文件包
            for __package in __file.Packages:
                __writeData.append(__package.PackageData)
            #写入文件
            self.__BinaryDataRestoration(__writeData, __file.FileName)