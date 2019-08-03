# -*- coding: utf-8 -*-
# 全国药品抽检



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

    for i in range(1, 457):  # 遍历456个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=121&State=1&bcId=152894035121716369704750131820&State=1&curstart=' + str(
        i) + '&State=1&tableName=TABLE121&State=1&viewtitleName=COLUMN1615&State=1&viewsubTitleName=COLUMN1618,COLUMN1616&State=1&tableView=%25E5%2585%25A8%25E5%259B%25BD%25E8%258D%25AF%25E5%2593%2581%25E6%258A%25BD%25E6%25A3%2580&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=121&tableName=TABLE121&tableView=全国药品抽检&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_qgypcj(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source,parse2json(browser.page_source),str(i)+'_'+str(j+1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
    '''

    药品品名     yppm
    标示生产企业名称(来源、产地)bsscqymc
    药品规格	 ypgg
    生产批号     scph
    检品来源     jply
    检验依据     jyyj
    检验结果	 jyjg
    不合格项目   bhgxm
    检验机构名称 jyjgmc
    抽检类别	 cjlb
    通告（公告）号 tg_gg_h
    备注 bz

    '''
    reg_dict = dict()
    result_json = dict()
    reg_dict['yppm'] = r'药品品名</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['bsscqymc_lycd_'] = r'标示生产企业名称\(来源\、产地\)</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['ypgg'] = r'药品规格</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['scph'] = r'生产批号</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['jply'] = r'检品来源</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['jyyj'] = r'检验依据</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['jyjg'] = r'检验结果</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['bhgxm'] = r'不合格项目</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['jyjgmc'] = r'检验机构名称</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['cjlb'] = r'抽检类别</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['tg_gg_h'] = r'通告（公告）号</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['bz'] = r'备注</td>\s*<td.*>(.*)</td></tr>'
    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)
if __name__ == '__main__':
    main()