class FileModel(object):
    """
    文件模型.
    """
    @property
    def FileName(self):
        """
        文件信息.
        """
        return self.__fileName
    @FileName.setter
    def FileName(self, value):
        """
        文件信息.
        """
        self.__fileName = value

    @property
    def Packages(self):
        """
        文件对应文件包.
        """
        return self.__packages
    @Packages.setter
    def Packages(self, value):
        """
        文件对应文件包.
        """
        self.__packages = value

    def __init__(self, fileName):
        """
        初始化模型.

        Args:
            fileName: 文件名
        """
        self.FileName = fileName
        self.Packages = []