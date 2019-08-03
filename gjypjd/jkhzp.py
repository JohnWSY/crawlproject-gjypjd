# -*- coding: utf-8 -*-
# 进口化妆品
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

    for i in range(1, 14167):  # 遍历14166个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=69&State=1&bcId=152904517090916554369932355535&State=1&curstart='+str(i)+'&State=1&tableName=TABLE69&State=1&viewtitleName=COLUMN801&State=1&viewsubTitleName=COLUMN811,COLUMN805&State=1&tableView=%25E8%25BF%259B%25E5%258F%25A3%25E5%258C%2596%25E5%25A6%2586%25E5%2593%2581&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=69&tableName=TABLE69&tableView=进口化妆品&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_jkhzp(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])

                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    """
    产品名称（中文）	cpmc_zw
    批件状态	pjzt
    产品名称（英文）	cpmc
    产品类别	cplb
    生产国（地区）	scg_dq
    生产企业（中文）	scqy_zw
    生产企业（英文）	scqy_yw
    生产企业地址	scqydz
    在华申报责任单位  zhsbzrdw
    在华责任单位地址  zhzrdwdz
    批准文号	pzwh
    批准日期	pzrq
    批件有效期	pjyxq
    备注  bz
    产品名称备注  cpbz
    产品技术要求	cpjsyq
    注  z
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['cpmc_zw'] = r"产品名称（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pjzt'] = r"批件状态</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpmc'] = r"产品名称（英文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cplb'] = r"产品类别</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scg_dq'] = r"生产国（地区）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scqy_zw'] = r"生产企业（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scqy_yw'] = r"生产企业（英文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scqydz'] = r"生产企业地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zhsbzrdw'] = r"在华申报责任单位</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zhzrdwdz'] = r"在华责任单位地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pzwh'] = r"批准文号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pzrq'] = r"批准日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pjyxq'] = r"批件有效期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bz'] = r"备注</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpbz'] = r"产品名称备注</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpjsyq'] = r"产品技术要求</td>\s*<td.*><a .*href=\"(.*)\">查看详细内容</a></td></tr>"
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