# -*- coding: utf-8 -*-
# GSP认证
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

    for i in range(1, 22030):  # 遍历22029个一级目录网页]
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=24&State=1&bcId=152911910751861035063432446242&State=1&curstart='+str(i)+'&State=1&tableName=TABLE24&State=1&viewtitleName=COLUMN159&State=1&viewsubTitleName=COLUMN158&State=1&tableView=GSP%25E8%25AE%25A4%25E8%25AF%2581&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=24&tableName=TABLE24&tableView=GSP认证&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_gsprz(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source,parse2json(browser.page_source),str(i)+'_'+str(j+1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    '''
    省市 ss
    证书编号zsbh
    企业名称 qymc
    经营地址 jydz
    认证范围 rzfw
    发证日期 fzrq
    证书有效期 zsyxq
    备注 bz
    发证机构 fzjg
    '''
    reg_dict=dict()
    result_json=dict()
    reg_dict['ss']=  r'省市</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['zsbh'] = r'证书编号</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['qymc']=r'企业名称</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['jydz']=r'经营地址</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['rzfw'] = r'认证范围</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['fzrq'] = r'发证日期</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['fzrq'] = r'证书有效期</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['bz'] = r'备注</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['fzjg'] = r'发证机构</td>\s*<td.*>(.*)</td></tr>'
    for i,v in reg_dict.items():
        reg_search=re.search(v,html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)



if __name__ == '__main__':
    main()