# -*- coding: utf-8 -*-

# 国产器械


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

    for i in range(1, 10590):  # 遍历10589个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=26&State=1&bcId=152904417281669781044048234789&State=1&curstart='+str(i)+'&State=1&tableName=TABLE26&State=1&viewtitleName=COLUMN184&State=1&viewsubTitleName=COLUMN181,COLUMN180&State=1&tableView=%25E5%259B%25BD%25E4%25BA%25A7%25E5%2599%25A8%25E6%25A2%25B0&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=26&tableName=TABLE26&tableView=国产器械&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_gcqx(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),str(i)+'_'+str(j+1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
    """
    注册证编号 zczbh
    注册人名称 zcrmc
    注册人住所 zcrzs
    生产地址   scdz
    代理人名称  dlrmc
    代理人住所  dlrzs
    产品名称  cpmc
    型号、规格 xhgg
    结构及组成 jgjzc
    适用范围 syfw
    其他内容 qtnr
    备注     bz
    批准日期  pzrq
    有效期至  yxqz
    附件      fj
    产品标准  cpbz
    变更日期  bgrq
    邮编      yb
    主要组成成分（体外诊断试剂） zyzcbf_twzdsj_
    预期用途（体外诊断试剂）     yqyt_twzdsj_
    产品储存条件及有效期（体外诊断试剂）cpcctjjyxq_twzdsj_
    审批部门   spbm
    变更情况   bgqk

     :return:json
     """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['zczbh'] = r"注册证编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zcrmc'] = r"注册人名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zcrzs'] = r"注册人住所</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scdz'] = r"生产地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dlrmc'] = r"代理人名称</td>\s*<td.*>(.*)</td></tr>"

    reg_dict['dlrzs'] = r"代理人住所</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpmc'] =    r"产品名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['xhgg'] =     r"规格</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jgjzc']=r"结构及组成</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['syfw'] = r"适用范围</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['qtnr'] = r"其他内容</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bz'] =       r"备注</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pzrq'] = r"批准日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxqz'] = r"有效期至</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fj '] =      r"附件</td>\s*<td>(.*)</></td></tr>"


    reg_dict['cpbz'] = r"产品标准</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bgzq'] = r"变更日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yb'] =       r"邮编</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zyzcbf_twzdsj_'] = r"主要组成成分\（体外诊断试剂\）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yqyt_twzdsj_'] = r"预期用途\（体外诊断试剂\）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpcctjjyxq_twzdsj_'] = r"产品储存条件及有效期\（体外诊断试剂\）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['spbm'] = r"审批部门</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bgqk'] = r"变更情况</td>\s*<td.*>(.*)</td></tr>"
    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()
    while(1):
        print('Finashed!')