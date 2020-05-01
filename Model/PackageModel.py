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

    def __init__(self, packageIndex, packageName, packageData):
        """
        初始化模型.

        Args:
            packageIndex: 文件包索引
            packageName: 文件包名
            packageData: 文件包数据
        """
        self.PackageIndex = packageIndex
        self.PackageName = packageName
        self.PackageData = packageData