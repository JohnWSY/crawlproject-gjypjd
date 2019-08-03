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
        url_1='http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList&on=true&page=' + str(
                                  i) + '&pageSize=15&productName=&conditionType=1&applyname=&applysn'
        res1 = browser.request('post', url_1)
        # print(res.text)
        res1= json.loads(res1.content)['list']
        # print(res1)
        browser.close()
        for j in range(len(res1)):
            browser = Chrome(chrome_options=option)
            url_2='http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById&id='+res1[j]['ID']
            res2 = browser.request('post', url_2)
            res3 =json.loads(res2.content)
            # print(res3)
            browser.close()
            sql = "insert into t_hzpscxkzhzqy_xkxq(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
            mysql_db.exetcute_sql(sql, [url_2, res2.content, parse(res3),
                                        str(i) + '_' + str(j + 1)])

def parse(dic):
    """
    企业名称qymc
    许可证编号xkzbh
    许可项目xkxm
    企业住所qyzs
    生产地址scdz
    社会信用代码shxydm
    法定代表人fddbr
    企业负责人qyfzr
    质量负责人zlfzr
    发证机关fzjg
    签发人qfr
    日常监督管理机构rcjdgljg
    日常监督管理人员rcjdglry
    有效期至yxqz
    发证日期fzrq
    状态zt
    投诉举报电话tsjbdh

    """

    reg_dict = dict()
    reg_dict['qymc'] = dic['epsName']
    reg_dict['xkzbh'] = dic['productSn']
    reg_dict['xkxm'] = dic['certStr']
    reg_dict['qyzs'] = dic['epsAddress']
    reg_dict['scdz'] = dic['epsProductAddress']
    reg_dict['shxydm'] = dic['businessLicenseNumber']
    reg_dict['fddbr'] = dic['legalPerson']
    reg_dict['qyfzr'] = dic['businessPerson']
    reg_dict['zlfzr'] = dic['qualityPerson']
    reg_dict['fzjg'] = dic['qfManagerName']
    reg_dict['qfr'] = dic['xkName']
    reg_dict['rcjdgljg'] = dic['rcManagerDepartName']
    reg_dict['rcjdglry'] = dic['rcManagerUser']
    reg_dict['yxqz'] = dic['xkDate']
    reg_dict['fzrq'] = dic['xkDateStr']
    reg_dict['zt'] = '正常'
    reg_dict['jbdh'] = '12331'

    return json.dumps(reg_dict, ensure_ascii=False)


if __name__ == '__main__':
    main()