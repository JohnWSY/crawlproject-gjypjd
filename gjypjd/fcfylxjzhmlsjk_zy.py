# -*- coding: utf-8 -*-
# 非处方药遴选及转换目录数据库-中药


import re
from selenium import webdriver
from gjypjd.utils import *
import json
import time


def main():
    mysql_db = DataBase()
    option=None
    #配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')

    for i in range(1, 262):  # 遍历261个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=130&State=1&bcId=154339165535424686654038867162&State=1&curstart='+str(i)+'&State=1&tableName=TABLE130&State=1&viewtitleName=COLUMN1754&State=1&tableView=%25E9%259D%259E%25E5%25A4%2584%25E6%2596%25B9%25E8%258D%25AF%25E9%2581%25B4%25E9%2580%2589%25E5%258F%258A%25E8%25BD%25AC%25E6%258D%25A2%25E7%259B%25AE%25E5%25BD%2595%25E6%2595%25B0%25E6%258D%25AE%25E5%25BA%2593-%25E4%25B8%25AD%25E8%258D%25AF&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=130&tableName=TABLE130&tableView=非处方药遴选及转换目录数据库-中药&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_fcfylxjzhmlsjk_zy(c_bh, dt_insertTime, c_url, b_content,c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),str(i)+'_'+str(j+1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()

        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
        """
         非处方药遴选及转换目录数据库-化学药品
         药品名称（公告名称） ypmc_ggmc_
         现用通用名  xytym
         规格  gg
         甲/乙分类   jyfl
         是/否双跨    sfsk
         公告发布时间 ggfbrq
         发布文件链接 fbwjlj
         是/否转出   sfzc
         转出文件链接 zcwjlj
         中/化 zh
         :return:json
         """
        # 初始化，避免取不到的情况下为空值
        result_json = dict()
        # 批准文号
        reg_dict = dict()
        reg_dict['ypmc_ggmc_'] = r"药品名称\（公告名称\）</td>\s*<td.*>(.*)</td></tr>"
        reg_dict['xytym'] = r"现用通用名</td>\s*<td.*>(.*)</td></tr>"
        reg_dict['gg'] =    r"规格</td>\s*<td.*>(.*)</td></tr>"
        reg_dict['jyfl'] = r"甲/乙分类</td>\s*<td.*>(.*)</td></tr>"
        reg_dict['sfsk'] = r"是/否双跨</td>\s*<td.*>(.*)</td></tr>"

        reg_dict['ggfbsj'] = r"公告发布时间</td>\s*<td.*>(.*)</td></tr>"
        reg_dict['fbwjlj'] = r"发布文件链接</td>\s*<td><a.*>(.*)</a></td></tr>"
        reg_dict['sfzc'] = r"是/否转出</td>\s*<td.*>(.*)</td></tr>"
        reg_dict['zcwjlj'] = r"转出文件链接</td>\s*<td>(.*)</></td></tr>"
        reg_dict['zh'] = r"中/化</td>\s*<td.*>(.*)</td></tr>"


        for i, v in reg_dict.items():
            reg_search = re.search(v,html)
            if reg_search is not None:
                result_json[i] = reg_search.group(1)
            else:
                result_json[i] = ''
        return json.dumps(result_json, ensure_ascii=False)

if __name__ == '__main__':
    main()
    while(1):
        print('Finashed!')