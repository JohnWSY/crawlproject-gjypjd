# -*- coding: utf-8 -*-
#药品经营企业

import time

import pickle
import re
from selenium import webdriver
from gjypjd.utils import *
import json


def main():
    option=None
    mysql_db = DataBase()
    #配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')

    for i in range(1, 33405):  # 遍历33404个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=41&State=1&bcId=152911863995882985662523838679&State=1&curstart='+str(i)+'&State=1&tableName=TABLE41&State=1&viewtitleName=COLUMN438&State=1&viewsubTitleName=COLUMN437&State=1&tableView=%25E8%258D%25AF%25E5%2593%2581%25E7%25BB%258F%25E8%2590%25A5%25E4%25BC%2581%25E4%25B8%259A&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=41&tableName=TABLE41&tableView=药品经营企业&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ypjyqy(c_bh, dt_insertTime, c_url, b_content,c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)


def parse2json(html):
    """
    许可证编号xkzbh
    企业名称qymc
    注册地址zcdz
    仓库地址ckdz
    法人代表frdb
    企业负责人qyfzr
    质量负责人zlfzr
    经营方式jyfs
    经营范围jyfw
    发证日期farq
    证书有效期zsyxq
    发证机构fzjg
    许可证状态xkzzt
    相关数据库查询xgsjkcx
    注z
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['xkzbh'] = r"许可证编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['qymc'] = r"企业名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zcdz'] = r"注册地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ckdz'] = r"仓库地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['frdb'] = r"法人代表</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['qyfzr'] = r"企业负责人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zlfzr'] = r"质量负责人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jyfs'] = r"经营方式</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jyfw'] = r"经营范围</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fzrq'] = r"发证日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zsyxq'] = r"证书有效期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fzjg'] = r"发证机构</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['xkzzt'] = r"许可证状态</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['xgsjkcx'] = r"相关数据库查询</td>\s*<td>\s*<a.*>(.*)</a><br>\s*</td></tr>"
    reg_dict['z'] = r"注</td>\s*<td.*><span.*>(.*)</span></td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)

if __name__ == '__main__':
    main()