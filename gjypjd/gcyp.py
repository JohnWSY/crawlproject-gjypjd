# -*- coding: utf-8 -*-
# 2-1 国产药品
import re
from selenium import webdriver
from gjypjd.utils import *
import json
import time


def main():
    mysql_db = DataBase()
    option = None
    # 配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')

    for i in range(1, 11022):  # 遍历11021个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=25&State=1&bcId=152904713761213296322795806604&State=1&curstart=' + str(
                i) + '&State=1&tableName=TABLE25&State=1&viewtitleName=COLUMN167&State=1&viewsubTitleName=COLUMN821,COLUMN170,COLUMN166&State=1&tableView=%25E5%259B%25BD%25E4%25BA%25A7%25E8%258D%25AF%25E5%2593%2581&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=25&tableName=TABLE25&tableView=国产药品&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                # 如果URL重复不进行爬取
                # if mysql_db.if_exists(url_2, 't_gcyp'):
                #     logger().info("{} is exists".format(url_2))
                #     continue
                # logger().info("{} is not exists".format(url_2))
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_gcyp(c_bh, dt_insertTime, c_url, b_content, c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),str(i)+'_'+str(j+1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)


def parse2json(html):
    """
    批准文号  pzwh
    产品名称  cpmc
    英文名称  ywmc
    商品名   spm
    剂型     jx
    规格     gg
    上市许可持有人  ssxkcyr
    生产单位   scdw
    生产地址   scdz
    产品类别   cplb
    批准日期   pzrq
    原批准文号   ypzwh
    药品本位码   ypbwm
    药品本位码备注  ypbwmbz
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['pzwh'] = r"批准文号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpmc'] = r"产品名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ywmc'] = r"英文名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['spm'] = r"商品名</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jx'] = r"剂型</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['gg'] = r"规格</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ssxkcyr'] = r"上市许可持有人<td.*>(.*)</td></tr>"
    reg_dict['scdw'] = r"生产单位</td>\s*<td.*><a.*>(.*)</a></td></tr>"
    reg_dict['scdz'] = r"生产地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cplb'] = r"产品类别</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pzrq'] = r"批准日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypzwh'] = r"原批准文号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypbwm'] = r"药品本位码</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypbwmbz'] = r"药品本位码备注</td>\s*<td.*>(.*)</td></tr>"

    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)

if __name__ == '__main__':
    main()
