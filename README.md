# Python文件(文件夹)分享
## Information
- Pyhton版本为3.8.2
- 使用数据库为MySQL

## 使用
- 需要Python3及PyMySQL
- 在MySQL库中执行CreateFolderTable.sql以创建所需存储过程
- 在config.json中添加数据库连接
### Windows
``Python3 Share.py``

### Linux
- 需要执行权限
- 需要手动设置换行符
```bash
chmod 750 ./Share.py
vim ./Share.py
:set ff=unix
```
``Python3 Share.py`` OR ``./Share.py``

### Parameters
#### Upload
``upload -d <待上传目录>``
#### Download
``download -d <下载保存目录>``
``DownloadFrom : 选择数据库中的表(文件夹)``