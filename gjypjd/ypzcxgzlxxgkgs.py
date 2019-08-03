# -*- coding: utf-8 -*-
# 药品注册相关专利信息公开公示
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

    for i in range(1, 130):  # 遍历129个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=65&State=1&bcId=152904820477685999443922990230&State=1&curstart='+str(i)+'&State=1&tableName=TABLE65&State=1&viewtitleName=COLUMN741&State=1&viewsubTitleName=COLUMN740,COLUMN743,COLUMN742&State=1&tableView=%25E8%258D%25AF%25E5%2593%2581%25E6%25B3%25A8%25E5%2586%258C%25E7%259B%25B8%25E5%2585%25B3%25E4%25B8%2593%25E5%2588%25A9%25E4%25BF%25A1%25E6%2581%25AF%25E5%2585%25AC%25E5%25BC%2580%25E5%2585%25AC%25E7%25A4%25BA&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=65&tableName=TABLE65&tableView=药品注册相关专利信息公开公示&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ypzcxgzlxxgkgs(c_bh, dt_insertTime, c_url, b_content,c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    """
    受理号slh
    药品名称ypmc
    申请人sqr
    专利zl
    专利名称zlmc
    邮编yb
    专利到期日或专利授权/公开日期zldqrhzlsq_gkrq
    外国专利wgzl
    外国专利人wgzlr
    申请人联系地址sqrlxdz
    专利人zlr
    注z
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['slh'] = r"受理号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypmc'] = r"药品名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sqr'] = r"申请人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zl'] = r"专利</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zlmc'] = r"专利名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yb'] = r"邮编</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zldqrhzlsq_gkrq'] = r"专利到期日或专利授权/公开日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['wgzl'] = r"外国专利</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['wgzlr'] = r"外国专利人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sqrlxdz'] = r"申请人联系地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zlr'] = r"<td.*>专利人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['z'] = r"注</td>\s*<td.*><span.*>(.*\s*.*)</span></td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)

if __name__ == '__main__':
    main()