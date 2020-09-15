#! /usr/bin/python3
# -*-coding:utf-8-*-
import os
from Foo import Foo
from Model import FileModel, PackageModel


class Upload(object):
    """
    获取上传数据类.
    """

    def __init__(self, single_reads=1024 * 1024):
        """
        初始化获取参数.

        Args:
            single_reads: 单次读取字节 Default = 1024 * 1024
        """
        self._single_reads = single_reads  # 单次读取字节
        self.folder_name = ""
        self.all_files = []
        self.count = 0
        self.finished = 0

    def get_upload_files(self, root_folder):
        """
        获取待上传数据.

        Args:
            root_folder: 根目录
        """
        if not os.path.exists(root_folder):
            return
        # 状态初始化
        replace_dir = root_folder
        if not replace_dir.endswith(os.sep):
            replace_dir += os.sep
        self.all_files = []
        split = replace_dir.split(os.sep)
        self.folder_name = split[len(split) - 2]
        self.count = 0
        # 遍历目录
        for root, dirs, files in os.walk(root_folder):
            # 遍历文件
            for file in files:
                # 获取文件名
                file_name = (root + os.sep + file).replace(replace_dir, '')
                # 添加文件
                self.all_files.append(FileModel.FileModel(file_name))
                # 获取数据流
                data_list = self._get_binary_data(root + os.sep + file)
                # 遍历数据流
                for index, data in enumerate(data_list):
                    # 添加文件包
                    self.all_files[len(self.all_files) - 1].Packages.append(
                        PackageModel.PackageModel(index, file_name, data))
                    self.count += 1

    def _get_binary_data(self, file):
        """
        获取二进制数据流.

        Args:
            file: 指定文件

        Returns:
            数据流列表
        """
        data_list = []
        read_count = 0
        with open(file, 'rb') as read_file:
            while True:
                read_file.seek(read_count)  # 设置读取位置
                # 数据不足完整一帧
                remain = os.path.getsize(file) - read_file.tell()
                if remain <= self._single_reads:
                    data_list.append(read_file.read(remain))
                # 完整一帧数据
                else:
                    data_list.append(read_file.read(self._single_reads))
                # 添加已读取字节
                read_count += len(data_list[len(data_list) - 1])
                # 读取完成
                if read_count >= os.path.getsize(file):
                    break
        return data_list

    def upload_to_db(self):
        """
        上传数据库.
        """
        connection = Foo.db_init()
        if connection is None:
            return
        # 提前创建表
        cursor = connection.cursor()
        try:
            cursor.execute("CALL CreateFolderTable(%s)", self.folder_name)
        except Exception as ex:
            print("Create Table Error:\n" + str(ex))
            return

        # 遍历所有文件
        self.finished = 0
        for file in self.all_files:
            # 遍历所有文件包
            for package in file.Packages:
                # 上传文件包
                try:
                    cursor.execute(
                        "INSERT INTO " + self.folder_name +
                        "(PackageIndex, PackageName, PackageData) VALUES(%s, %s, %s)",
                        (package.PackageIndex, package.PackageName, package.PackageData))
                except Exception as ex:
                    print("WriteData Error:\n" + str(ex))
                    return

                # 刷新进度显示
                self.finished += 1
                Foo.progress_refresh(self.count, self.finished)
        # 上传完成
        connection.commit()
        cursor.close()
        connection.close()
        print('Upload Completed')
