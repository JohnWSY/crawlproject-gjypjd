# -*- coding: utf-8 -*-
# 药品出口销售证明


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
    for i in range(1, 17):  # 遍历16个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=143&State=1&bcId=155842726469384720845975356256&State=1&curstart='+str(i)+'&State=1&tableName=TABLE143&State=1&viewtitleName=COLUMN1934&State=1&viewsubTitleName=COLUMN1935,COLUMN1938&State=1&tableView=%25E8%258D%25AF%25E5%2593%2581%25E5%2587%25BA%25E5%258F%25A3%25E9%2594%2580%25E5%2594%25AE%25E8%25AF%2581%25E6%2598%258E&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=143&tableName=TABLE143&tableView=药品出口销售证明&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ypckxszm(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    """
    证明编号zsbh
    Certificate No
    证明类别zmlb
    Certificate Classification
    产品名称cpmc
    Name of Product
    剂型jx
    Dosages Form of the Product
    规格gg
    Strength
    商品名spm
    Trade Name
    产品批准文号cppzwh
    Number of product license（DMF number）
    批准（备案）时间pzbasj
    Date of Issue
    该药品规格是否获得许可在中国市场上使用gypggsfhdxkzzgscssy
    Is this product strength licensed to be placed on the market for use in China
    药品生产企业或者药品上市许可持有人名称ypscqyhzypssxkcyrmc
    Name of Manufacturer or Product-license Holder
    社会信用代码(组织机构代码)shxydm_zzjgdm
    Social Credit Code
    药品生产企业或者药品上市许可持有人地址ypscqyhzypssxkcyrdz
    Address of Manufacturer or Product-license Holder
    如果药品上市许可持有人不是生产者，药品实际生产者名称是rgypssxkcyrbsscz_ypsjsczmcs
    If the license holder is not the manufacturer, the name of the manufacturer producing the dosage form is
    如果药品上市许可持有人不是生产者，药品实际生产者地址是rgypssxkcyrbsscz_ypsjsczdzs
    If the license holder is not the manufacturer, the address of the manufacturer producing the dosage form is
    是否中国药品生产质量管理规范的要求sfzgypsczlglgfdyq

    Do the facilities and operations conform to the requirements of Chinese GMP
    证明事项Certificate Item
    证明当局名称zmdjmc
    Name of Certifying Authority
    证明当局地址zmdjdz
    Address of Certifying Authority
    证明当局电话Telephone number of Certifying Authority
    证明当局传真Fax of Certifying Authority
    证明出具时间zmcjsj
    Certificate IssueDate
    证明有效期至zmyxqz
    This certificate remain valid until
    状态zt
    Status of Certificate
    有关说明ygsm
    注z
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['zsbh'] = r"证明编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Certificate No'] = r"Certificate No</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zmlb'] = r"证明类别</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Certificate Classification'] = r"Certificate Classification</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpmc'] = r"产品名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Name of Product'] = r"Name of Product</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jx'] = r"剂型</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Dosages Form of the Product'] = r"Dosages Form of the Product</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['gg'] = r"规格</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Strength'] = r"Strength</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['spm'] = r"商品名</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Trade Name'] = r"Trade Name</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cppzwh'] = r"产品批准文号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Number of product license（DMF number）'] = r"Number of product license（DMF number）</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pzbasj'] = r"批准（备案）时间</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Date of Issue'] = r"Date of Issue</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['gypggsfhdxkzzgscssy'] = r"该药品规格是否获得许可在中国市场上使用</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Is this product strength licensed to be placed on the market for use in China'] = r"Is this product strength licensed to be placed<br> on the market for use in China</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypscqyhzypssxkcyrmc'] = r"药品生产企业或者药品上市许可持有人名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Name of Manufacturer or Product-license Holder'] = r"Name of Manufacturer or Product-license Holder<br></td>\s*<td.*>(.*)</td></tr>"
    reg_dict['shxydm_zzjgdm'] = r"社会信用代码\(组织机构代码\)</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Social Credit Code'] = r"Social Credit Code</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypscqyhzypssxkcyrdz'] = r"药品生产企业或者药品上市许可持有人地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Address of Manufacturer or Product-license Holder'] = r"Address of Manufacturer or Product-license Holder</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['rgypssxkcyrbsscz_ypsjsczmcs'] = r"如果药品上市许可持有人不是生产者，药品实际生产者名称是</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['If the license holder is not the manufacturer, the name of the manufacturer producing the dosage form is'] = r"If the license holder is not the manufacturer, <br>the name of the manufacturer producing the dosage form is</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['rgypssxkcyrbsscz_ypsjsczdzs'] = r"如果药品上市许可持有人不是生产者\，药品实际生产者地址是</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['If the license holder is not the manufacturer, the address of the manufacturer producing the dosage form is'] = r"If the license holder is not the manufacturer, <br>the address of the manufacturer producing the dosage form is</td>\s*<td.*>(.*)</td></tr>"
    
    reg_dict['sfzgypsczlglgfdyq'] = r"是否中国药品生产质量管理规范的要求</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Do the facilities and operations conform to the requirements of Chinese GMP'] = r"Do the facilities and operations conform <br>to the requirements of Chinese GMP</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Certificate Item'] = r"证明事项Certificate Item</td>\s*<td.*?>(.*)</td></tr>"
    reg_dict['zmdjmc'] = r"证明当局名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Name of Certifying Authority'] = r"Name of Certifying Authority</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zmdjdz'] = r"证明当局地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Address of Certifying Authority'] = r"Address of Certifying Authority</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Telephone number of Certifying Authority'] = r"证明当局电话Telephone number of Certifying Authority</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Fax of Certifying Authority'] = r"证明当局传真Fax of Certifying Authority</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zmcjsj'] = r"证明出具时间</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Certificate IssueDate'] = r"Certificate IssueDate</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zmyxqz'] = r"证明有效期至</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['This certificate remain valid until'] = r"This certificate remain valid until</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zt'] = r"状态</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['Status of Certificate'] = r"Status of Certificate</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ygsm'] = r"有关说明</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['z'] = r"注</td>\s*<td.*><span.*>(.*)</span></td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()