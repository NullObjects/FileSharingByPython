#! /usr/bin/python3
# -*-coding:utf-8-*-
import os
from Foo import Foo
from Model import FileModel, PackageModel


class Download(object):
    """
    数据流写入文件类.
    """

    def __init__(self):
        """
        初始化写入.
        """
        self.all_files = []
        self.count = 0
        self.finished = 0

    def download_from_db(self, folder_name, folder_dir):
        """
        从数据库下载数据.

        Args:
            folder_name:选中的数据
            folder_dir:下载目录
        """
        connection = Foo.db_init()
        if connection is None:
            return
        if not folder_dir.endswith(os.sep):
            folder_dir += os.sep

        try:
            cursor = connection.cursor()
            # 查询总量
            cursor.execute("SELECT COUNT(PackageID) FROM " + folder_name)
            self.count = int(cursor.fetchone()[0])
            self.finished = 0
            if self.count != 0:
                # 查询文件名
                cursor.execute("SELECT DISTINCT PackageName FROM " + folder_name)
                files = cursor.fetchall()
                for file in files:
                    # 添加文件
                    self.all_files.append(
                        FileModel.FileModel(folder_dir + file[0].replace('\\', os.sep).replace('/', os.sep)))
                    # 查询文件包数量
                    cursor.execute("SELECT COUNT(PackageIndex) FROM " + folder_name +
                                   " WHERE PackageName = %s", (file[0]))
                    package_count = int(cursor.fetchone()[0])
                    # 遍历获取文件包
                    for index in range(package_count):
                        cursor.execute("SELECT PackageData FROM " + folder_name +
                                       " WHERE PackageName = %s AND PackageIndex = %s", (file[0], index))
                        # 添加文件包
                        self.all_files[len(self.all_files) - 1].Packages.append(
                            PackageModel.PackageModel(
                                index,
                                file[0].replace('\\', os.sep).replace('/', os.sep),
                                cursor.fetchone()[0]))
                        # 刷新进度显示
                        self.finished += 1
                        Foo.progress_refresh(self.count, self.finished)
                # 下载完成
                cursor.close()
                connection.close()
                print('GetData Completed')
        except Exception as ex:
            print("GetData Error:\n" + str(ex))
            return

    def write_to_files(self):
        """
        文件包组合写入.
        """
        # 遍历写入文件
        for file in self.all_files:
            write_data = []
            # 遍历添加文件包
            for package in file.Packages:
                write_data.append(package.PackageData)
            # 写入文件
            self._binary_data_restoration(write_data, file.FileName)

    def _binary_data_restoration(self, write_data, file_name):
        """
        二进制数据流写入文件.

        Args:
            write_data: 数据流列表
            file_name: 指定存储文件
        """
        # 目录不存在则创建目录
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        # 写入数据
        with open(file_name, 'wb') as write_file:
            for data in write_data:
                write_file.write(data)
