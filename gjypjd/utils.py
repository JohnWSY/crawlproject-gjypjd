# Author:Frank
import configparser
import pymysql
import psycopg2
import logging
from DBUtils.PooledDB import PooledDB


class DataBase:

    def __init__(self, conf=None):
        if conf is None:
            conf = './conf/common.ini'

        db_conf = get_db_conf(conf)
        self._driver = db_conf[0]
        self._ip = db_conf[1]
        self._port = db_conf[2]
        self._user = db_conf[3]
        self._password = db_conf[4]
        self._name = db_conf[5]
        self._encoding = db_conf[6]

        self._create_pool()

    def _create_pool(self):
        if self._driver == 'pymysql':
            self._pool = PooledDB(creator=pymysql, mincached=3, maxcached=1, maxconnections=3, blocking=True,
                                  host=self._ip, port=self._port, db=self._name, user=self._user,
                                  passwd=self._password, charset=self._encoding)
        if self._driver == 'psycopg2':
            self._pool = PooledDB(creator=psycopg2, mincached=10, maxcached=5, maxconnections=20, blocking=True,
                                  host=self._ip, port=self._port, database=self._name, user=self._user,
                                  password=self._password)

    def _get_connection(self):
        return self._pool.connection()

    def exetcute_sql(self, sql, params):
        """
        执行带有参数的sql
        :param sql:
        :param params:
        :return:
        """
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                logger().info('success execute {}'.format(params[0]))
                conn.commit()
        except Exception as e:
            logger().error(e)
            logger().error('error execute {}'.format(params[0]))
            conn.rollback()
        finally:
            conn.close()

    def select_sql_first(self, sql, params=None):
        """
        执行带有参数的sql,获取第一条数据
        :param sql:
        :param params:
        :return:
        """
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                data = cursor.fetchone()
                return data
        except:
            logger().error('error execute {}'.format(sql))
            return None
        finally:
            conn.close()

    def select_sql_all(self, sql, params=None):
        """
        执行带有参数的sql,获取所有数据
        :param sql:
        :param params:
        :return:
        """
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                data = cursor.fetchall()
                return data
        except:
            logger().error('error execute {}'.format(sql))
            return None
        finally:
            conn.close()

    def if_exists(self, url, tableName):
        """
        检查URL是否存在  如果存在就不进行爬取
        :param url:
        :return:
        """
        sql = 'select count(*) from {} where c_url = \'{}\''.format(tableName, url)
        result = self.select_sql_first(sql)
        if result[0] == 1:
            return True
        return False


def logger():
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger('gjypjd')
    return logger


def if_headless():
    cf = configparser.ConfigParser()
    cf.read('./conf/common.ini')

    headless = cf.get('webdriver', 'headless')
    if headless.lower() == 'true':
        return True
    return False


def get_db_conf(conf):
    """
    获取数据库配置信息
    :return:
    """
    cf = configparser.ConfigParser()
    # cf.read('./conf/common.ini')
    cf.read(conf)

    db_driver = cf.get('db', 'db_driver')
    db_ip = cf.get('db', 'db_ip')
    db_port = cf.getint('db', 'db_port')
    db_user = cf.get('db', 'db_user')
    db_password = cf.get('db', 'db_password')
    db_name = cf.get('db', 'db_name')
    db_encoding = cf.get('db', 'db_encoding')
    return [db_driver, db_ip, db_port, db_user, db_password, db_name, db_encoding]


if __name__ == '__main__':
    pass
