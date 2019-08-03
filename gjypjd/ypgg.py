# -*- coding: utf-8 -*-
# 药品广告

import pickle
import re
from selenium import webdriver
from gjypjd.utils import *
import json
import time

def main():
    option = None
    mysql_db = DataBase()
    # 配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')

    for i in range(1, 6000):  # 遍历3个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=39&State=1&bcId=152904590261619367373367535375&State=1&curstart=' + str(
                i) + '&State=1&tableName=TABLE39&State=1&viewtitleName=COLUMN413&State=1&viewsubTitleName=COLUMN410,COLUMN415,COLUMN414&State=1&tableView=%25E8%258D%25AF%25E5%2593%2581%25E5%25B9%25BF%25E5%2591%258A&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=39&tableName=TABLE39&tableView=药品广告&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ypgg(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])

                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)


def parse2json(html):
    """
    药品广告批准文号ypggpzwh
    单位名称dwmc
    地址dz
    邮政编码yzbm
    通用名称tymp
    商品名称spmc
    商标名称sbmc
    处方分类cffl
    广告类别gglb
    时长sc
    广告有效期ggyxq
    广告发布内容ggfbnr
    批准文号pzwh
    备注bz
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['ypggpzwh'] = r"药品广告批准文号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dwmc'] = r"单位名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dz'] = r"地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yzbm'] = r"邮政编码</td>\s*<td.*>(.*\s*.*)</td></tr>"
    reg_dict['tymp'] = r"通用名称</td>\s*<td.*>(.*\s*.*)</td></tr>"
    reg_dict['spmc'] = r"商品名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cffl'] = r"处方分类</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['gglb'] = r"广告类别</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sc'] = r"时长</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ggyxq'] = r"广告有效期</td>\s*<td.*>(.*\s*.*)</td></tr>"
    reg_dict['ggfbnr'] = r"广告发布内容</td>\s*<td><a href=\"(.*)\" target.*>.*</a></td></tr>"
    reg_dict['pzwh'] = r"批准文号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bz'] = r"备注</td>\s*<td.*>(.*)</td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    result_json['ggfbnr'] = 'http://app1.sfda.gov.cn' + result_json['ggfbnr']
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()
