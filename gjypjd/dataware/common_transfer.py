# Author:Frank

from gjypjd.utils import *
import pymysql
import psycopg2


def main(source_table, target_table, columns_num):
    gp_db = DataBase('../conf/target_db.ini')
    mysql_db = DataBase('../conf/common.ini')

    source_table = source_table
    source_sql = 'select c_json from {}'.format(source_table)

    target_table = target_table
    columns_num = columns_num
    placeholders = []
    for i in range(columns_num):
        placeholders.append("%s")
    placeholders = str(tuple(placeholders)).replace("'", "")
    target_table = 'insert into {} values {}'.format(target_table, placeholders)

    for data in mysql_db.select_sql_all(source_sql):
        data_dict = eval(data[0])
        params = list()
        for k, v in data_dict.items():
            params.append(v)
        gp_db.exetcute_sql(target_table, params)
    pass


if __name__ == '__main__':
    source_table = 't_gcyp'
    target_table = 'syn_network.t_net_chinesedrug'
    columns_num = 14
    main(source_table, target_table, columns_num)
