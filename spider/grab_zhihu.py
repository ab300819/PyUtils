import os, re, time, json
import http.cookiejar
import requests
import html
from pyquery import PyQuery as pq
from spider import ui

'''
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            佛祖保佑       永无BUG
'''

'''
普通验证码
/captcha.gif?r=1482662794237&type=login

文字点击验证码
/captcha.gif?r=1482662996504&type=login&lang=cn

验证码name = 'captcha'

手机登陆
http://www.zhihu.com/login/phone_num

邮箱登陆
https://www.zhihu.com/login/email
'''


class GrabZhiHu:
    def __init__(self):
        self.main_url = 'https://www.zhihu.com'
        self.login_url = 'https://www.zhihu.com/login/email'
        self.user_agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.cookie_file = '../resources/zhihu_cookie'
        self.session = requests.Session()
        self.session.cookies = http.cookiejar.LWPCookieJar(filename=self.cookie_file)

    def check_login(self):
        try:
            # 加载Cookies文件
            self.session.cookies.load(ignore_discard=True)
            print("使用cookie登陆!")

        except:
            print("未找到或cookie已过期!")
            self.login()

    def login(self):

        # 获取_xsrf
        result = self.session.get(self.main_url, headers=self.user_agent)
        html = pq(result.content)
        xsrf = pq(html("input[name='_xsrf']")[0])
        _xsrf = xsrf.attr.value

        # 获取验证码图片
        gif_url = "http://www.zhihu.com/captcha.gif?r=" + str(int(time.time() * 1000)) + "&type=login"
        gif_image = self.session.get(gif_url, headers=self.user_agent)

        # 保存图片
        with open('../resources/zhihu_code.gif', 'wb') as f:
            f.write(gif_image.content)

        # 获取登陆信息
        login_info = ui.get_login_info('../resources/zhihu_code.gif')
        login_data = {
            "captcha": login_info['code'],
            "password": login_info['password'],
            "_xsrf": _xsrf,
            "email": login_info['username']
        }

        # 登录
        response = self.session.post(self.login_url, data=login_data, headers=self.user_agent)
        print(response.content.decode("unicode-escape"))

        # 保存cookie
        self.session.cookies.save()

    def test(self, url):
        self.check_login()
        if url:
            result = self.session.get(url, headers=self.user_agent, allow_redirects=False)
        else:
            result = self.session.get(self.main_url, headers=self.user_agent, allow_redirects=False)
        print(html.unescape(result.content.decode("utf-8")))

    # 抓取专栏文章的url
    def analyze_article_ur(self):
        pass

    # 分析文章界面抓取文章内容
    def get_article(self):
        pass

    # 保存内容
    def save_content(self, article_info):
        pass

    # 传入收藏夹主页，分析每个问题及其答案
    def analyse_collection_url(self):
        pass

    # 传入单个问题url，抓取收藏夹问题和答案
    def get_collection_question_answer(self):
        pass

    # 抓取目标问题及答案
    def get_question_answer(self):
        pass

if __name__ == '__main__':
    test = GrabZhiHu()
    url = 'https://www.zhihu.com/collection/41051858'
    test.test(url)