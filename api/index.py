'''
Date: 2021-08-22 15:18:09
LastEditors: Steve Li
LastEditTime: 2021-08-25 10:15:11
FilePath: \vercelwecom\api\index.py
'''
from requests import *
from re import *
from json import dumps
from os import environ
from http.server import BaseHTTPRequestHandler
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin',"*")
        self.send_header('Content-type','application/json')
        self.end_headers();
        # try:
        cpid = environ['corpid'];
        cpsc = environ['corpsecret'];
        resp = get("https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+cpid+"&corpsecret="+cpsc).json()
        actk = resp["access_token"];
        code = resp["errcode"];
        if code != 0:
            self.wfile.write(dumps({
                "code":code,
                "msg": resp["errmsg"]
            }))
            return;
        msg = compile(r'msg=([^?&=]*)').findall(self.path);
        print(msg);
        if len(msg)==0 or msg[0]=='':
            self.wfile.write(dumps({
                "code": 0,
                "msg": "未传入请求参数！"
            }).encode())
            return;
        resp = post("https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+actk,data=dumps({
                "touser": "@all",
                "msgtype": "markdown",
                "agentid": environ["agentid"],
                "markdown": {
                    "content": msg[0]
                },
                "enable_duplicate_check": 0,
                "duplicate_check_interval": 1800
            })).json()
        code = resp["errcode"];
        if code != 0:
                self.wfile.write(dumps({
                    "code":code,
                    "msg": resp["errmsg"]
                }).encode())
                return;
        else:
            self.wfile.write(dumps({
                    "code":200,
                    "msg":"Success"
                }).encode())
        # except Exception as e:
        #     self.wfile.write(dumps({
        #         "code": 500,
        #         "error": e
        #     }));
        # finally:
        #     return;
    def do_POST(self):
        self.do_GET(self);
        return;
