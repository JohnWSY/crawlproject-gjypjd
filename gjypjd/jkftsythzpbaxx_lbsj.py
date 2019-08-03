# -*- coding: utf-8 -*-
# 进口非特殊用途化妆品备案信息（一）-列表数据

from seleniumrequests import Chrome
import json
from selenium import webdriver
from gjypjd.utils import  *
import  re

def main():
    option = None
    mysql_db = DataBase()
    # 配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')


    browser = Chrome(chrome_options=option)
    url_1 = 'http://cpnp.nmpa.gov.cn/province/webquery/wq.do?method=query&querytype=productname&pfid=&content=&dataPage=0&perPage=15&allRows=8084&order='
    response = browser.request('post', url_1)
    response1 = json.loads(response.content)['pageBean']
    page=response1['allPage']
    browser.close()


    for i in range(0, page):
        browser = Chrome(chrome_options=option)
        url_1 = 'http://cpnp.nmpa.gov.cn/province/webquery/wq.do?method=query&querytype=productname&pfid=&content=&dataPage=' + str(
            i) + '&allPage=539&perPage=15&allRows=8084&order='
        res = browser.request('post', url_1)
        res1 = json.loads(res.content)['list']
        browser.close()
        for j in range(len(res1)):
            sql = "insert into t_jkftsythzpbaxx_lbsj(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
            mysql_db.exetcute_sql(sql, [url_1, res.content, parse(res1[j]),
                                        str(i+1) + '_' + str(j + 1)])

def parse(dic):
    """
    产品名称cpmc
    备案凭证号bapzh
    生产企业scqy
    境内责任人jnzrr
    备案日期barq

    """

    reg_dict = dict()
    reg_dict['cpmc'] = dic['productname']
    reg_dict['bapzh'] = dic['passno']
    reg_dict['scqy'] = dic['enterprise']
    reg_dict['jnzrr'] = dic['internalunitname']
    reg_dict['barq'] = dic['updatepassdate']

    return json.dumps(reg_dict, ensure_ascii=False)


if __name__ == '__main__':
    main()