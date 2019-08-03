# -*- coding: utf-8 -*-
# 进口药品
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

    for i in range(1, 271):  # 遍历270个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=36&State=1&bcId=152904858822343032639340277073&State=1&curstart='+str(i)+'&State=1&tableName=TABLE36&State=1&viewtitleName=COLUMN361&State=1&viewsubTitleName=COLUMN354,COLUMN823,COLUMN356,COLUMN355&State=1&tableView=%25E8%25BF%259B%25E5%258F%25A3%25E8%258D%25AF%25E5%2593%2581&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=36&tableName=TABLE36&tableView=进口药品&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_jkyp(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    """
    注册证号 zczh
    原注册证号 yzczh
    注册证号备注 zczhbz
    分包装批准文号 fbzpzwh
    公司名称（中文） gsmc_zw_
    公司名称（英文） gsmc_yw_
    地址（中文）dz_zw_
    地址（英文）dz_yw_
    国家/地区（中文）gjdq_zw_
    国家/地区（英文）gjdq_yw_
    产品名称（中文）cpmc_zw_
    产品名称（英文）cpmc_yw_
    商品名（中文）spm_zw_
    商品名（英文）spm_yw_
    剂型（中文）jx_zw_
    规格（中文）gg_zw_
    包装规格（中文）bzgg_zw_
    生产厂商（中文）sccs_zw_
    生产厂商（英文）sccs_yw_
    厂商地址（中文）csdz_zw_
    厂商地址（英文）csdz_yw_
    厂商国家/地区（中文）csgjdq_zw_
    厂商国家/地区（英文）csgjdq_yw_
    发证日期 fzrq
    有效期截止日 yxjzr
    分包装企业名称 fbzqymc
    分包装企业地址 fbzqydz
    分包装文号批准日期 fbzwhpzrq
    分包装文号有效期截止日 fbzwhyxqjzr
    产品类别 cplb
    药品本位码 ypbwm
    药品本位码备注 ypbwmbz

    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['zczh'] = r"注册证号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yzczh'] = r"原注册证号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zczhbz'] = r"注册证号备注</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fbzpzwh'] = r"分包装批准文号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['gsmc_zw_'] = r"公司名称（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['gsmc_yw_'] = r"公司名称（英文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dz_zw_'] = r"地址（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dz_yw_'] = r"地址（英文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['gjdq_zw_'] = r"国家/地区（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['gjdq_yw_'] = r"国家/地区（英文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpmc_zw_'] = r"产品名称（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpmc_yw_'] = r"产品名称（英文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['spm_zw_'] = r"商品名（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['spm_yw_'] = r"商品名（英文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jx_zw_'] = r"剂型（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['gg_zw_'] = r"规格（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bzgg_zw_'] = r"包装规格（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sccs_zw_'] = r"生产厂商（中文）</td>\s*<td.*>(.*)</></td></tr>"
    reg_dict['sccs_yw_'] = r"生产厂商（英文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['csdz_zw_'] = r"厂商地址（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['csdz_yw_'] = r"厂商地址（英文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['csgjdq_zw_'] = r"厂商国家/地区（中文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['csgjdq_yw_'] = r"厂商国家/地区（英文）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fzrq'] = r"发证日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict[' yxjzr'] = r"有效期截止日</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fbzqymc'] = r"分包装企业名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fbzqydz'] = r"分包装企业地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fbzwhpzrq'] = r"分包装文号批准日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fbzwhyxqjzr'] = r"分包装文号有效期截止日</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cplb'] = r"产品类别</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypbwm'] = r"药品本位码</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypbwmbz'] = r"药品本位码备注</td>\s*<td.*>(.*)</td></tr>"
    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)
if __name__ == '__main__':
    main()