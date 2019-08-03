# -*- coding: utf-8 -*-
# OTC化学药品说明书范本
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

    for i in range(1, 81):  # 遍历80个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=1&State=1&bcId=154117771028162150796642210632&State=1&curstart='+str(i)+'&State=1&tableName=TABLE1&State=1&viewtitleName=COLUMN1&State=1&tableView=OTC%25E5%258C%2596%25E5%25AD%25A6%25E8%258D%25AF%25E5%2593%2581%25E8%25AF%25B4%25E6%2598%258E%25E4%25B9%25A6%25E8%258C%2583%25E6%259C%25AC&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=1&tableName=TABLE1&tableView=OTC化学药品说明书范本&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_otchxypsmsfb(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source,parse2json(browser.page_source),str(i)+'_'+str(j+1)])

                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()

        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
    '''
    说明书标题 smsbt
    注 z
    正文 zw
    '''
    reg_dict=dict()
    result_json=dict()
    reg_dict['smsbt']=r'说明书标题</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['z']= r'注</td>\s*<td.*>(.*)<br></td></tr>'
    reg_dict['z_'] = r'注</td>\s*<td.*>(.*)\s*<br>\s*<br></td></tr>'
    reg_dict['zw'] = r'正文</td>\s*<td.*>(.*)<br></td></tr>'
    reg_dict['z_w'] = r'正文</td>\s*<td.*?>((\s*<br>.*)*)</td></tr>'
    for i,v in reg_dict.items():
        reg_search=re.search(v,html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    if result_json['z'] == '':
        result_json['z']=result_json['z_']
        del result_json['z_']
    else:
        del result_json['z_']

    if result_json['zw'] == '':
        result_json['zw'] = result_json['z_w']
        del result_json['z_w']
    else:
        del result_json['z_w']

    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()