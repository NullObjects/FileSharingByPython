#! /usr/bin/python3
# -*-coding:utf-8-*-
import json

import pymysql


class Foo(object):
    """
    公共方法类
    """

    @staticmethod
    def db_init():
        """
        数据库连接初始化

        Returns:
            success->pymysql.connection OR failed->none
        """
        # 新建连接
        with open('config.json') as config_json:
            config = json.load(config_json)
        db_config = config['connections'][int(config['connectionSelect'])]
        try:
            return pymysql.connect(host=db_config['host'],
                                   database=db_config['database'],
                                   user=db_config['user'],
                                   password=db_config['password'])
        # 连接字典错误
        except Exception as ex:
            print("Exception:\n" + str(ex))
            return None

    @staticmethod
    def progress_refresh(count, finished):
        """
        根据完成进度刷新显示

        Args:
            count:int 总计
            finished:int 完成
        """
        progress = int(finished / count * 50)
        print("\r", '[' + '>' * progress + '-' * (50 - progress) +
              ']' + str(finished) + '/' + str(count),
              end='\t\t', flush=True)
