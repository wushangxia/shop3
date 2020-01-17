import requests
import json

class YunPian(object):
    def __init__(self,api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"
    def send_sms(self,code,mobile):
        parmas = {
            "apikey":self.api_key,
            "mobile":mobile,
            "text":"测试验证码{code}".format(code=code)
        }
        response = requests.post(self.single_send_url,data=parmas)
        re_dict = json.loads(response.text)
        return re_dict
if __name__=="__main__":
    yun_pian = YunPian("2e87d1xxxxxx7d4bxxxx1608f7c6da23exxxxx2")
    yun_pian.send_sms('2018',"手机号码")