# -*- coding: utf-8 -*-
# 进口器械（历史数据）
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

    for i in range(1, 834):  # 遍历833个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=95&State=1&bcId=152904451661174780844452282676&State=1&curstart='+str(i)+'&State=1&tableName=TABLE95&State=1&viewtitleName=COLUMN1209&State=1&viewsubTitleName=COLUMN1203,COLUMN1202&State=1&tableView=%25E8%25BF%259B%25E5%258F%25A3%25E5%2599%25A8%25E6%25A2%25B0%25EF%25BC%2588%25E5%258E%2586%25E5%258F%25B2%25E6%2595%25B0%25E6%258D%25AE%25EF%25BC%2589&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=95&tableName=TABLE95&tableView=进口器械（历史数据）&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_jkqx_lssj(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
    """
    注册号zch
    生产厂商名称（中文）sccsmc_zw_
    生产厂商名称（英文）sccsmc_yw_
    生产厂地址（中文） sccdz_zw_
    生产场所sccs
    生产国或地区（中文）scghdq_zw_
    产品名称（中文）cpmc_zw_
    产品名称（英文）cpmc_yw_
    规格型号 ggxh
    产品标准cpbz
    产品性能结构及组成cpxnjgjzc
    产品适用范围 cpsyfw
    注册代理 zcdl
    售后服务机构 shfwjg
    批准日期pzrq
    有效期截止日 yxjzr
    变更日期 bgrq
    附件 fj
    备注bz
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['zch'] = r"注册号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sccsmc_zw_'] = r"生产厂商名称（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sccsmc_yw_'] = r"生产厂商名称（英文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sccdz_zw_'] = r"生产厂地址（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sccs'] = r"生产场所</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scghdq_zw_'] = r"生产国或地区（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpmc_zw_'] = r"产品名称（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpmc_yw_'] = r"产品名称（英文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ggxh'] = r"规格型号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpbz'] = r"产品标准</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpxnjgjzc'] = r"产品性能结构及组成</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpsyfw'] = r"产品适用范围</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zcdl'] = r"注册代理</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['shfwjg'] = r"售后服务机构</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pzrq'] = r"批准日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxjzr'] = r"有效期截止日</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bgrq'] = r"变更日期</td>\s*<td.*>(.*)</td></tr>"
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