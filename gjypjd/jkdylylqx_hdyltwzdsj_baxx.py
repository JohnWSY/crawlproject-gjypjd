# -*- coding: utf-8 -*-
# 进口第一类医疗器械（含第一类体外诊断试剂）备案信息

import re
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

    for i in range(1, 588):  # 遍历587个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=104&State=1&bcId=152904498781962056127955207188&State=1&curstart=' + str(
                i) + '&State=1&tableName=TABLE104&State=1&viewtitleName=COLUMN1384&State=1&viewsubTitleName=COLUMN1376,COLUMN1371&State=1&tableView=%25E8%25BF%259B%25E5%258F%25A3%25E7%25AC%25AC%25E4%25B8%2580%25E7%25B1%25BB%25E5%258C%25BB%25E7%2596%2597%25E5%2599%25A8%25E6%25A2%25B0%25EF%25BC%2588%25E5%2590%25AB%25E7%25AC%25AC%25E4%25B8%2580%25E7%25B1%25BB%25E4%25BD%2593%25E5%25A4%2596%25E8%25AF%258A%25E6%2596%25AD%25E8%25AF%2595%25E5%2589%2582%25EF%25BC%2589%25E5%25A4%2587%25E6%25A1%2588%25E4%25BF%25A1%25E6%2581%25AF&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=104&tableName=TABLE104&tableView=进口第一类医疗器械（含第一类体外诊断试剂）备案信息&Id=\d+', s,
                           re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_jkdylylqx_hdyltwzdsj_baxx(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)


def parse2json(html):
    '''
    备案号 bah
    产品类别 cplb
    备案人名称 barmc
    备案人组织机构代码 barzzjgdm
    备案人注册地址 barzcdz
    生产地址 scdz
    代理人 dlr
    代理人注册地址 dlrzcdz
    产品名称或产品分类名称 cpmchcpflmc
    型号/规格或包装规格xhgghbzgg
    产品有效期 cpyxq
    产品描述或主要组成成份 cpmshzyzccf
    预期用途 yqyt
    备注 bz
    备案单位badw
    备案日期barq
    变更情况bgqk
    备案状态bazt

    '''
    reg_dict = dict()
    result_json = dict()

    reg_dict['bah'] = r'备案号</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['cplb'] = r'产品类别</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['barmc'] = r'备案人名称</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['barzzjgdm'] = r'备案人组织机构代码</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['barzcdz'] = r'备案人注册地址</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['scdz'] = r'生产地址</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['dlr'] = r'代理人</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['dlrzcdz'] = r'代理人注册地址</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['cpmchcpflmc'] = r'产品名称或产品分类名称</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['xhgghbzgg'] = r'规格或包装规格</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['cpyxq'] = r'产品有效期</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['cpmshzyzccf'] = r'产品描述或主要组成成份</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['yqyt'] = r'预期用途</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['bz'] = r'备注</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['badw'] = r'备案单位</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['barq'] = r'备案日期</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['bgqk'] = r'变更情况</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['bazt'] = r'备案状态</td>\s*<td.*>(.*)</td></tr>'
    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()
