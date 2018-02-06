#coding:utf-8

import os
from tornado.web import RequestHandler
import time
import json
from alipay_sdk.alipay import AliPay
from common.log_client import gen_log
from settings import default_settings


class AlipayUrlHandler(RequestHandler):
    """
    获取支付宝支付路径
    """
    def post(self, *args, **kwargs):
        gen_log.info("alipay post")
        order_id = self.get_argument("order_id", "")
        # 创建用于进行支付宝支付的工具对象
        alipay = AliPay(
            appid=default_settings.get('app_id', ''),
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(__file__), "pem/pkcs8_private.pem"),
            alipay_public_key_path=os.path.join(os.path.dirname(__file__), "pem/alipay_public.pem"),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False  配合沙箱模式使用
        )

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(0.01),  # 将Decimal类型转换为字符串交给支付宝
            subject="云计算web个人",
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )

        # 让用户进行支付的支付宝页面网址
        url = default_settings.get("alipay_url", "") + "?" + order_string

        return self.finish({"code": 0, "message": "请求支付成功", "url": url})

class CheckAlipayHandler(RequestHandler):
    """

    """
    def get(self, *args, **kwargs):
        # 创建用于进行支付宝支付的工具对象
        gen_log.info("check alipay get:%s" %os.path.join(os.path.dirname(__file__), "pem/pkcs8_private.pem"))
        order_id = self.get_argument("order_id", "")
        alipay = AliPay(
            appid=default_settings.get("app_id", ""),
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(__file__), "pem/pkcs8_private.pem"),
            alipay_public_key_path=os.path.join(os.path.dirname(__file__), "pem/alipay_public.pem"),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA2,官方推荐，配置公钥的时候能看到
            debug=True  # 默认False  配合沙箱模式使用
        )

        while True:
            # 调用alipay工具查询支付结果
            response = alipay.api_alipay_trade_query(order_id)  # response是一个字典
            # 判断支付结果
            code = response.get("code")  # 支付宝接口调用成功或者错误的标志
            trade_status = response.get("trade_status")  # 用户支付的情况

            if code == "10000" and trade_status == "TRADE_SUCCESS":
                # 表示用户支付成功
                # 返回前端json，通知支付成功
                return self.finish({"code": 0, "message": "支付成功"})

            elif code == "40004" or (code == "10000" and trade_status == "WAIT_BUYER_PAY"):
                # 表示支付宝接口调用暂时失败，（支付宝的支付订单还未生成） 后者 等待用户支付
                # 继续查询
                print(code)
                print(trade_status)
                continue
            else:
                # 支付失败
                # 返回支付失败的通知
                return self.finish({"code": 1, "message": "支付失败"})

class AlipayHandler(RequestHandler):
    """
    支付服务
    """
    def post(self):
        self.finish(json.dumps({'state': 0, 'message': 'ok'}))

class AlipayCallbackHandler(RequestHandler):
    """
    支付宝回调
    """
    def post(self):
        self.finish(json.dumps({'state': 0, 'message': 'ok'}))
