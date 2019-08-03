# -*- coding: utf-8 -*-
# 国产非特殊用途化妆品备案信息(二)-备案详情

import re
from seleniumrequests import Chrome
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

    #先调一次post请求，获取一级目录页的页数
    url = "http://125.35.6.80:8181/ftban/itownet/fwAction.do?method=getBaNewInfoPage&on=true&page=1&pageSize=15&productName=&conditionType=1&applyname=&applysn="
    browser = Chrome(chrome_options=option)
    res = browser.request("post", url)
    html = res.text
    browser.close()
    json_return = json.loads(html)
    pageCount = json_return["pageCount"]

    for i in range(1, pageCount+1): #遍历目录网页
        try :
            url_1 = "http://125.35.6.80:8181/ftban/itownet/fwAction.do?method=getBaNewInfoPage&on=true&page="+str(i)+"&pageSize=15&productName=&conditionType=1&applyname=&applysn="
            browser = Chrome(chrome_options=option)
            res = browser.request("post",url_1)
            html = res.text
            browser.close()
            json_return = json.loads(html)
            d = json_return['list'] #得到页面列表信息

            for j in range(len(d)):
                url_2 = "http://125.35.6.80:8181/ftban/itownet/hzp_ba/fw/pz.jsp?processid="+d[j]["processid"]+"&nid="+d[j]["processid"]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                s = browser.page_source
                browser.close()
                s = s.replace("&nbsp;",' ')
                s = s.replace("amp;",'')

                sql = "insert into t_gcftsythzpbaxx_baxq(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, s, parse2json(s),str(i) + '_' + str(j + 1)])
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    """
     产品名称 cpmc
    备案编号 babh
    备案日期 barq
    生产企业 scqy
    生产企业地址 scqydz
    实际生产企业 sjscqy
    成分        cf
    说明        sm
    备注        bz
    产品包装平面图  cpbzpmt
    产品包装立体图  cpbzltt

    :return: json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()

    reg_dict = dict()
    reg_dict['cpmc'] = r"<h1>(.*)</h1>"
    reg_dict['babh'] = r"<h2>备案编号\s+(.*)\s</h2>"
    reg_dict['barq'] = r"<h6>备案日期\s+(.*)</h6>.*<h3>"
    reg_dict['scqy'] = r"<h3>生产企业\s+(.*)\s</h3>"
    reg_dict['scqydz']=r"<h6>生产企业地址\s+(.*)\s</h6>"
    reg_dict['sjscqy'] = r"<h6>实.*</h6><ul.*><li>(.*)</li>\s</ul>"
    reg_dict['cf'] = r"<h6>成.*<ul.*>(.*)<br>\s+</ul>"
    reg_dict['sm'] = r"<h6>说.*<li>(.*)</li><li></li>"
    reg_dict['bz'] = r"<h6>备.*<li>(.*?)</li>"
    reg_dict['cpbzpmt'] = r'产品包装平面图.*预览.*<a href="(.*)'
    reg_dict['cpbzltt'] = r'产品包装立体图.*预览.*<a href="(.*)'

    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''

    #处理成分中的双引号问题
    result_json['cf'] = result_json['cf'].replace('\"','')

    return json.dumps(result_json, ensure_ascii=False)
if __name__ == '__main__':
    main()