# -*- coding: utf-8 -*-
# 国产器械（历史数据）


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
        option.add_argument('--no-sandbox')

    for i in range(1, 2724):  # 遍历2723个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=94&State=1&bcId=152904424297012685387397452852&State=1&curstart=' + str(
                i) + '&State=1&tableName=TABLE94&State=1&viewtitleName=COLUMN1188&State=1&viewsubTitleName=COLUMN1189,COLUMN1187&State=1&tableView=%25E5%259B%25BD%25E4%25BA%25A7%25E5%2599%25A8%25E6%25A2%25B0%25EF%25BC%2588%25E5%258E%2586%25E5%258F%25B2%25E6%2595%25B0%25E6%258D%25AE%25EF%25BC%2589&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=94&tableName=TABLE94&tableView=国产器械（历史数据）&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_gcqx_lssj(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    '''
        注册号 zch
        产品名称cpmc
        生产单位scdw
        地址dz
        产品标准cpbz
        产品性能结构及组成cpxnjgjzc
        产品适用范围cpsyfw
        规格型号ggxh
        批准日期pzrq
        有效期yxq
        变更日期bgrq
        生产场所sccs
        邮编yb
        附件fj
        备注bz
     :return:json
    '''
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()

    reg_dict['zch'] = r"注册号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpmc'] = r"产品名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scdw'] = r"生产单位</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dz'] = r"地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpbz'] = r"产品标准</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpxnjgjzc'] = r"产品性能结构及组成</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpsyfw'] = r"产品适用范围</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ggxh'] = r"规格型号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pzrq'] = r"批准日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxq'] = r"有效期</td>\s*<td.*>(.*)</td></tr>"

    reg_dict['bgrq'] = r"变更日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sccs'] = r"生产场所</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yb'] = r"邮编</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fj'] = r"附件</td>\s*<td>(.*)</></td></tr>"
    reg_dict['bz'] = r"备注</td>\s*<td.*>(.*)</td></tr>"
    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()
