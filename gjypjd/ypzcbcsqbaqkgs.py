# -*- coding: utf-8 -*-
# 药品注册补充申请备案情况公示


import pickle
import re
from selenium import webdriver
from gjypjd.utils import *
import json
import time

def main():
    option=None
    mysql_db = DataBase()
    #配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')

    for i in range(1, 15010):  # 遍历15009个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=63&State=1&bcId=152904798868514040213090136034&State=1&curstart='+str(i)+'&State=1&tableName=TABLE63&State=1&viewtitleName=COLUMN710&State=1&viewsubTitleName=COLUMN707,COLUMN697&State=1&tableView=%25E8%258D%25AF%25E5%2593%2581%25E6%25B3%25A8%25E5%2586%258C%25E8%25A1%25A5%25E5%2585%2585%25E7%2594%25B3%25E8%25AF%25B7%25E5%25A4%2587%25E6%25A1%2588%25E6%2583%2585%25E5%2586%25B5%25E5%2585%25AC%25E7%25A4%25BA&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=63&tableName=TABLE63&tableView=药品注册补充申请备案情况公示&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ypzcbcsqbaqkgs(c_bh, dt_insertTime, c_url, b_content,c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
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
    备案号bah
    药品通用名称yptymc
    英文名称/拉丁名称ywmc_ldmc
    药品分类ypfl
    剂型jx
    规格gg
    包装规格bzgg
    批准文号pzwh
    药品标准ypnr
    备案内容banr
    药品生产企业ypscqy
    备案机关bajg
    备案日期barq
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['slh'] = r"受理号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bah'] = r"备案号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yptymc'] = r"药品通用名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ywmc_ldmc'] = r"英文名称/拉丁名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypfl'] = r"药品分类</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jx'] = r"剂型</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['gg'] = r"规格</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bzgg'] = r"包装规格</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pzwh'] = r"批准文号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypbz'] = r"药品标准</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['banr'] = r"备案内容</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypscqy'] = r"药品生产企业</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bajg'] = r"备案机关</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['barq'] = r"备案日期</td>\s*<td.*>(.*)</td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)

if __name__ == '__main__':
    main()