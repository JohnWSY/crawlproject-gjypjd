# -*- coding: utf-8 -*-
from seleniumrequests import Chrome
import json
from selenium import webdriver
from gjypjd.utils import  *

def main():
    option = None
    mysql_db = DataBase()
    # 配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')

    for i in range(1, 330):
        browser = Chrome(chrome_options=option)
        url='http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList&on=true&page=' + str(
                                  i) + '&pageSize=15&productName=&conditionType=1&applyname=&applysn'
        res = browser.request('post', url)
        # print(res.text)
        res1 = json.loads(res.content)['list']
        # print(res1)
        browser.close()
        for j in range(len(res1)):
            sql = "insert into t_hzpscxkhzqy_lbsj(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
            mysql_db.exetcute_sql(sql, [url, res.content, parse(res1[j]),
                                        str(i) + '_' + str(j + 1)])

def parse(dic):
    """
    企业名称qymc
    许可证编号xkzbh
    发证机关fzjg
    有效期至yxqz
    发证日期fzrq
    """

    reg_dict = dict()
    reg_dict['qymc'] = dic['EPS_NAME']
    reg_dict['xkzbh'] = dic['PRODUCT_SN']
    reg_dict['fzjg'] = dic['QF_MANAGER_NAME']
    reg_dict['yxqz'] = dic['XK_DATE']
    reg_dict['fzrq'] = dic['XC_DATE']

    return json.dumps(reg_dict, ensure_ascii=False)


if __name__ == '__main__':
    main()