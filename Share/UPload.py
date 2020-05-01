import os
import json
import pymysql
from Model import FileModel, PackageModel


class UPload(object):
    """
    获取上传数据类.
    """
    def __init__(self, singleReads = 1024 * 1024):
        """
        初始化获取参数.

        Args:
            singleReads: 单次读取字节 Default = 1024 * 1024
        """
        self.__SingleReads = singleReads  #单次读取字节

    def __GetBinaryData(self, file):
        """
        获取二进制数据流.

        Args:
            file: 指定文件

        Retuen:
            数据流列表
        """
        __DataList = []
        __readCount = 0
        with open(file, 'rb') as __readFile:
            while (True):
                __readFile.seek(__readCount)  #设置读取位置
                #数据不足完整一帧
                __remain = os.path.getsize(file) - __readFile.tell()
                if (__remain <= self.__SingleReads):
                    __DataList.append(__readFile.read(__remain))
                #完整一帧数据
                else:
                    __DataList.append(__readFile.read(self.__SingleReads))
                #添加已读取字节
                __readCount += len(__DataList[len(__DataList) - 1])
                #读取完成
                if (__readCount >= os.path.getsize(file)):
                    break
        return __DataList

    def GetUPloadFiles(self, rootFolder):
        """
        获取待上传数据.

        Args:
            rootFolder: 根目录
        """
        if (not os.path.exists(rootFolder)):
            return
        #状态初始化
        __replaceDir = rootFolder
        if (not __replaceDir.endswith(os.sep)):
            __replaceDir += os.sep
        self.AllFiles = []
        __split = __replaceDir.split(os.sep)
        self.FolderName = __split[len(__split) - 2]
        self.Count = 0
        #遍历目录
        for __root, __dirs, __files in os.walk(rootFolder):
            #遍历文件
            for __file in __files:
                #获取文件名
                __fileName = (__root + os.sep + __file).replace(
                    __replaceDir, '')
                #添加文件
                self.AllFiles.append(FileModel.FileModel(__fileName))
                #获取数据流
                __dataList = self.__GetBinaryData(__root + os.sep + __file)
                #遍历数据流
                for __index, __data in enumerate(__dataList):
                    #添加文件包
                    self.AllFiles[len(self.AllFiles) - 1].Packages.append(
                        PackageModel.PackageModel(__index, __fileName, __data))
                    self.Count += 1

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

    def UPloadToDB(self):
        """
        上传数据库.
        """
        if (not self.__DBInit()):
            return
        # 提前创建表
        self.__cursor = self.__connection.cursor()
        try:
            self.__cursor.execute("CALL CreateFolderTable(%s)", (self.FolderName))
        except Exception as ex:
            print("Create Table Error:\n" + str(ex))
            return

        #遍历所有文件
        self.Finshed = 0
        for __file in self.AllFiles:
            #遍历所有文件包
            for __package in __file.Packages:
                #上传文件包
                try:
                    self.__cursor.execute(
                        "INSERT INTO " + self.FolderName +
                        "(PackageIndex, PackageName, PackageData) VALUES(%s, %s, %s)",
                        (__package.PackageIndex, __package.PackageName,
                         __package.PackageData))
                except Exception as ex:
                    print("WriteData Error:\n" + str(ex))
                    return

                #刷新进度显示
                self.Finshed += 1
                __persent = int(self.Finshed / self.Count * 50)
                print("\r",
                      '[' + '=' * __persent + '-' * (50 - __persent) + ']' +
                      str(self.Finshed) + '/' + str(self.Count),
                      end='\t\t',
                      flush=True)
        #上传完成
        self.__connection.commit()
        self.__cursor.close()
        self.__connection.close()
        print('UPload Completed')