#! /usr/bin/python3
# -*-coding:utf-8-*-F
from Foo import Foo
from Share import Upload, Download


class Share(object):
    def __init__(self):
        """
        功能选择.
        """
        while True:
            print('===== ===== ===== ===== ===== ===== ===== =====')
            command = input('Upload/Download -> Share, Quit - > Exit\n')
            # 退出
            if command.upper() == 'QUIT' or command.upper() == 'EXIT':
                break
            else:
                # 检查参数
                if len(command.split(' -d ')) != 2:
                    print('Need -d(Dir) Parameter')
                    continue
                # 执行指令
                instruction = command.split(' -d ')[0]
                parameter = command.split(' -d ')[1]
                # 上传
                if instruction.upper() == 'UPLOAD':
                    self._upload(parameter)
                # 下载
                elif instruction.upper() == 'DOWNLOAD':
                    self._download(parameter)
                else:
                    print('Command Error')

    def _upload(self, folder_dir):
        """
        将指定目录上传.

        Args:
            folder_dir:指定目录
        """
        print('You can ignore charset waring')
        upload = Upload.Upload()
        upload.get_upload_files(folder_dir)
        upload.upload_to_db()

    def _download(self, folder_dir):
        """
        下载指定文件夹.

        Args:
            folder_dir:待下载文件夹
        """
        # 显示可下载文件夹
        connection = Foo.db_init()
        if connection is None:
            return
        try:
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            table_list = ""
            for table in cursor.fetchall():
                table_list += table[0] + '\t'
        except Exception as ex:
            print('Get Folder From DB ERROR:\n' + str(ex))
            return

        folder_name = input("\nDownload From:\n" + table_list)  # 保存路径
        download = Download.Download()
        download.download_from_db(folder_name, folder_dir)
        download.write_to_files()


if __name__ == "__main__":
    Share()
