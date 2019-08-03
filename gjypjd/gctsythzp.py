# -*- coding: utf-8 -*-

# 国产特殊用途化妆品

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
    #  option.add_argument('--no-sandbox')

    for i in range(1, 2686):  # 遍历2685个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=68&State=1&bcId=152904508268669766289794835880&State=1&curstart=' + str(
                i) + '&State=1&tableName=TABLE68&State=1&viewtitleName=COLUMN787&State=1&viewsubTitleName=COLUMN793,COLUMN789&State=1&tableView=%25E5%259B%25BD%25E4%25BA%25A7%25E7%2589%25B9%25E6%25AE%258A%25E7%2594%25A8%25E9%2580%2594%25E5%258C%2596%25E5%25A6%2586%25E5%2593%2581&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=68&tableName=TABLE68&tableView=国产特殊用途化妆品&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_gctsythzp(c_bh, dt_insertTime, c_url, b_content, c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    """
    产品名称	cpmc
    产品类别	cplb
    生产企业	svqy
    生产企业地址	scqydz
    批准文号	pzwh
    批件状态	pjzt
    批准日期	pzrq
    批件有效期	pjyxq
    卫生许可证号 wsxkzh
    产品名称备注	cpmcbz
    备注  bz
    产品技术要求	cpjsyq
    注  z
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['cpmc'] = r"产品名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cplb'] = r"产品类别</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['svqy'] = r"生产企业</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scqydz'] = r"生产企业地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pzwh'] = r"批准文号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pjzt'] = r"批件状态</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pzrq'] = r"批准日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pjyxq'] = r"批件有效期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['wsxkzh'] = r"卫生许可证号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpmcbz'] = r"产品名称备注</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bz'] = r"备注</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpjsyq'] = r"产品技术要求</td>\s*<td.*><a.*>(.*)</a></td></tr>"
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
