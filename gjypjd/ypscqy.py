# -*- coding: utf-8 -*-
# 药品生产企业



import pickle
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

    for i in range(1, 527):  # 遍历526个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=34&State=1&bcId=152911762991938722993241728138&State=1&curstart='+str(i)+'&State=1&tableName=TABLE34&State=1&viewtitleName=COLUMN322&State=1&viewsubTitleName=COLUMN321&State=1&tableView=%25E8%258D%25AF%25E5%2593%2581%25E7%2594%259F%25E4%25BA%25A7%25E4%25BC%2581%25E4%25B8%259A&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=34&tableName=TABLE34&tableView=药品生产企业&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ypscqy(c_bh, dt_insertTime, c_url, b_content,c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)


def parse2json(html):
    """
    编号bh
    社会信用代码/组织机构代码shxydm_zzjgdm
    分类码flm
    省份sf
    企业名称qymc
    法定代表人fdzrr
    企业负责人qyzrr
    质量负责人zlfzr
    注册地址zcdz
    生产地址scdz
    生产范围scfw
    发证日期fzrq
    有效期至yxqz
    发证机关fzjg
    签发人qfr
    日常监管机构rcjgjg
    日常监管人员rcjgry
    监督举报电话jdjbdh
    备注bz
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['bh'] = r"编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['shxydm_zzjgdm'] = r"社会信用代码/组织机构代码</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['flm'] = r"分类码</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sf'] = r"省份</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['qymc'] = r"企业名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fdzrr'] = r"法定代表人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['qyzrr'] = r"企业负责人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zlfzr'] = r"质量负责人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zcdz'] = r"注册地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scdz'] = r"生产地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fzrq'] = r"发证日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxqz'] = r"有效期至</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fzjg'] = r"发证机关</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['qfr'] = r"签发人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['rcjgjg'] = r"日常监管机构</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['rcjgry'] = r"日常监管人员</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jdjbdh'] = r"监督举报电话</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bz'] = r"备注</td>\s*<td.*>(.*)</td></tr>"



    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()