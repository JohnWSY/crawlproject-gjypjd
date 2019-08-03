# -*- coding: utf-8 -*-
# 进口非特殊用途化妆品备案信息-备案详情
from seleniumrequests import Chrome
import json
from selenium import webdriver
import re
from gjypjd.utils import *


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
    page = response1['allPage']
    browser.close()


    for i in range(0, page):
        browser = Chrome(chrome_options=option)
        url_1='http://cpnp.nmpa.gov.cn/province/webquery/wq.do?method=query&querytype=productname&pfid=&content=&dataPage='+str(i)+'&allPage=539&perPage=15&allRows=8084&order='
        res1 = browser.request('post', url_1)
        res1= json.loads(res1.content)['list']
        browser.close()
        for j in range(len(res1)):
            browser = Chrome(chrome_options=option)
            url_2='http://cpnp.nmpa.gov.cn/province/webquery/wq.do?'
            params = {'method': 'show','id':res1[j]['id']}
            headers={
                    'Accept':'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.9',
                    'Connection':'keep-alive',
                    'Content-Length': '31',
                    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                    'Cookie':'_gscu_515232071=60234697wnhvr115; _gscbrs_515232071=1; JSESSIONID=DA4CEE8CEE0F521678039F251D0A32AD',
                    'Host':'cpnp.nmpa.gov.cn',
                    'Origin':'http://cpnp.nmpa.gov.cn',
                    'Referer':'http://cpnp.nmpa.gov.cn/province/webquery/show.jsp?id=50BF34D2A36759BA',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
                    'X-Requested-With':'XMLHttpRequest'
                    }
            res2 = browser.request('post', url_2, data=params, headers=headers)
            browser.close()
            sql = "insert into t_jkftsythzpbaxx_baxq(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
            mysql_db.exetcute_sql(sql, [url_2, res2.text, parse(json.loads(res2.text)),
                                        str(i+1) + '_' + str(j+1)])

def parse(dic):
    """
    产品名称cpmc
    产品英文名称cpywm
    备案编号babh
    备案日期barq
    生产企业名称（中文）scqymc_zw
    生产企业名称（英文）scqymc_yw
    生产企业地址scqydz
    境内负责人名称jnfzrmc
    境内负责人地址jnfzrdz
    生产国（地区）scg_dq
    进口省份jksf
    成分cf
    备注bz
    备案资料核查bazlsc
    历史ls
    技术要求jsyq
    产品设计包装平面图cpsjbzpmt
    产品中文标签cpzwbq
    产品上市包装立体图cpssbzltt
    """
    s = re.findall('id=([0-9|A-Z]{16})', dic['preview'])
    reg_dict = dict()
    reg_dict['cpmc'] = dic['productname']
    reg_dict['cpywm'] = dic['productnameen']
    reg_dict['babh'] = dic['passno']
    reg_dict['barq'] = dic['passdate']
    reg_dict['scqymc_zw'] = dic['enterprise']
    reg_dict['scqymc_yw'] = dic['enterpriseen']
    reg_dict['scqydz'] = dic['enterpriseaddressen']
    reg_dict['jnfzrmc'] = dic['internalunitname']
    reg_dict['jnfzrdz'] = dic['internalunitaddr']
    reg_dict['scg_dq'] = dic['Country']
    reg_dict['jksf'] = dic['jksf']
    reg_dict['cf'] = dic['cf']
    reg_dict['bz'] = dic['memo']
    reg_dict['bazlsc'] = dic['CheckupResult']
    reg_dict['ls'] = dic['hisList']
    reg_dict['jsyq'] = 'http://cpnp.nmpa.gov.cn/province/webquery/wq.do?method=jsyq&id='+s[0]
    reg_dict['cpsjbzpmt'] = 'http://cpnp.nmpa.gov.cn/province/webquery/preview.jsp?id='+s[1]
    reg_dict['cpzwbq'] = 'http://cpnp.nmpa.gov.cn/province/webquery/preview.jsp?id='+s[2]
    reg_dict['cpssbzltt'] = 'http://cpnp.nmpa.gov.cn/province/webquery/preview.jsp?id='+s[3]

    return json.dumps(reg_dict, ensure_ascii=False)


if __name__ == '__main__':
    main()