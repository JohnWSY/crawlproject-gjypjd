# -*- coding: utf-8 -*-

# 化妆品生产许可获证企业（历史数据）
import pickle
import re
from selenium import webdriver
from gjypjd.utils import *
import json
import time

def main():
    option=None
    mysql_db=DataBase()
    #配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')

    for i in range(1, 260):  # 遍历259个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=93&State=1&bcId=152904546381762233020239194602&State=1&curstart='+str(i)+'&State=1&tableName=TABLE93&State=1&viewtitleName=COLUMN1178&State=1&viewsubTitleName=COLUMN1179,COLUMN1177&State=1&tableView=%25E5%258C%2596%25E5%25A6%2586%25E5%2593%2581%25E7%2594%259F%25E4%25BA%25A7%25E8%25AE%25B8%25E5%258F%25AF%25E8%258E%25B7%25E8%25AF%2581%25E4%25BC%2581%25E4%25B8%259A%25EF%25BC%2588%25E5%258E%2586%25E5%258F%25B2%25E6%2595%25B0%25E6%258D%25AE%25EF%25BC%2589&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=93&tableName=TABLE93&tableView=化妆品生产许可获证企业（历史数据）&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_hzpscxkhzqy_lssj(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),str(i)+'_'+str(j)])

                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
    """
    省份sf
    证书编号zsbh
    企业名称qymc
    产品名称cpmc
    住所zs
    生产地址scdz
    明细mx
    发证日期fzrq
    有效期yxq
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['sf'] = r"省份</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zsbh'] = r"证书编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['qymc'] = r"企业名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpmc'] = r"产品名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zs'] = r"住所</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scdz'] = r"生产地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['mx'] = r"明细</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fzrq'] = r"发证日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxq'] = r"有效期</td>\s*<td.*>(.*)</td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()