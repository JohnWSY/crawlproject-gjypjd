# -*- coding: utf-8 -*-
# 麻醉药品和精神药品品种目录
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

    for i in range(1, 27):  # 遍历27个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=102&State=1&bcId=152911939788030557312353847510&State=1&curstart='+str(i)+'&State=1&tableName=TABLE102&State=1&viewtitleName=COLUMN1349&State=1&viewsubTitleName=COLUMN1353,COLUMN1350&State=1&tableView=%25E9%25BA%25BB%25E9%2586%2589%25E8%258D%25AF%25E5%2593%2581%25E5%2592%258C%25E7%25B2%25BE%25E7%25A5%259E%25E8%258D%25AF%25E5%2593%2581%25E5%2593%2581%25E7%25A7%258D%25E7%259B%25AE%25E5%25BD%2595&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=102&tableName=TABLE102&tableView=麻醉药品和精神药品品种目录&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_mzyphjsyppzml(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source,parse2json(browser.page_source),str(i)+'_'+str(j+1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
    '''
    中文名zwm
    英文名ywm
    CAS号cash
    备注bz
    药品类别yplb
    目录版本mlbb
    注z

    '''
    reg_dict=dict()
    result_json=dict()
    reg_dict['zwm']=r'中文名</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['ywm'] = r'英文名</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['cash']=r'CAS号</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['bz']=r'备注</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['yplb'] = r'药品类别</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['mlbb'] = r'目录版本</td>\s*<td.*>(.*\s*.*)</td></tr>'
    reg_dict['z'] = r'注</td>\s*<td.*><span\s.*><p><b>(.*)</p></span></td></tr>'

    for i,v in reg_dict.items():
        reg_search=re.search(v,html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()