#! /usr/bin/python3
# -*-coding:utf-8-*-

class PackageModel(object):
    """
    文件包模型.
    """

    @property
    def PackageIndex(self):
        """
        文件包索引层级.
        """
        return self.__packageIndex

    @PackageIndex.setter
    def PackageIndex(self, value):
        """
        文件包索引层级.
        """
        self.__packageIndex = value

    @property
    def PackageName(self):
        """
        完整文件包名.
        """
        return self.__packageName

    @PackageName.setter
    def PackageName(self, value):
        """
        完整文件包名.
        """
        self.__packageName = value

    @property
    def PackageData(self):
        """
        文件包数据.
        """
        return self.__packageData

    @PackageData.setter
    def PackageData(self, value):
        """
        文件包数据.
        """
        self.__packageData = value

    def __init__(self, package_index, package_name, package_data):
        """
        初始化模型.

        Args:
            package_index: 文件包索引
            package_name: 文件包名
            package_data: 文件包数据
        """
        self.PackageIndex = package_index
        self.PackageName = package_name
        self.PackageData = package_data
