import json
import requests
import random
import re
import chardet
import os
import time
 
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109 \
  import DescribeDomainRecordsRequest, UpdateDomainRecordRequest

user_agent_list = [
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
  'Opera/8.0 (Windows NT 5.1; U; en)',
  'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
  'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
  'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
  'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
  'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
  'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
  'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
  'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
  'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
  'Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
  'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
  'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
  'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
  'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
  'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
  'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0',
  'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
  'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
  'UCWEB7.0.2.37/28/999',
  'NOKIA5700/ UCWEB7.0.2.37/28/999',
  'Openwave/ UCWEB7.0.2.37/28/999',
  'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999',
]

# 此类的作用是获取本地外网ip
class IP(object):
  def __init__(self):
    global user_agent_list
    self.user_agent_list = user_agent_list
    # 网上找了几个获取ip的接口，为了防止过多的访问接口被封，每次调用随机选择
    self.api_list = [
      'http://ip.chinaz.com/getip.aspx',
      'http://www.net.cn/static/customercare/yourip.asp',
      'https://ip.cn/',
      'http://www.ip168.com/json.do?view=myipaddress',
      'http://pv.sohu.com/cityjson',
      'http://pv.sohu.com/cityjson',
      'http://ip.taobao.com/service/getIpInfo.php?ip=myip',
      'http://2018.ip138.com/ic.asp',
    ]
 
  def ip_query(self):
    # 一直循环，直到成功获取到本地外网ip
    while True:
      url = random.sample(self.api_list, 1)[0]
      headers = random.sample(self.user_agent_list, 1)[0]
      try:
        res = requests.get(url, headers={'User-Agent':headers}, timeout=5)
        encoding = chardet.detect(res.content)['encoding']
        html = res.content.decode(encoding)
        out = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',html)
        if out != []:
          return out[0] 
      except Exception as e:
        continue
 
#此类是修改阿里云的解析ip
class Aliyunddns(object):
  def __init__(self):
    self.local_ip = IP()
    # 修改以下内容为你自己的，！！！！！！！！！！！！！！
    self.client = AcsClient("修改为你的AccessKey ID","修改为你的Access Key Secret")
    self.domain = '修改为你的顶级域名，注意是顶级域名'
 
  #检测本地网络环境，是否是联网状态
  def IsConnectNet(self):
    try:
      requests.get('http://www.baidu.com',timeout=5)
      return True
    except requests.exceptions.ConnectionError as e:
      return False
 
  # 检测本地外网ip是否和解析的ip一致
  def CheckLocalip(self):
    if not self.IsConnectNet():
      print('no net')
      return None
 
    #这里为了防止频繁的访问阿里云api，会把ip存入本地的ip.txt文件中
    #每次都和本地文件中的ip地址进行对比，不一致再去访问阿里云api进行修改
    netip = self.local_ip.ip_query()
    return netip
 
  #开始更新
  def Update(self,ip,record):
    udr = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    udr.set_accept_format('json')
    udr.set_RecordId(record['RecordId'])
    udr.set_RR(record['RR'])
    udr.set_Type(record['Type'])
    udr.set_Value(ip)
    response = self.client.do_action_with_exception(udr)
    UpdateDomainRecordJson = json.loads(response.decode('utf-8'))
    print(UpdateDomainRecordJson)
 
  #获取阿里云域名解析信息
  def GetDomainRecords(self):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_DomainName(self.domain)
    DomainRecords.set_accept_format('json')
    response = self.client.do_action_with_exception(DomainRecords)
    record_dict = json.loads(response.decode('utf-8'))
    for record in record_dict['DomainRecords']['Record']:
      if not record['RR'] in ['@','www']:
        continue
      netip = self.local_ip.ip_query()
 
      if record['Value'] != netip:
        print('netip:',netip)
        print('aliip:',record['Value'])
        self.Update(netip, record)
 
if __name__ == '__main__':
  ali = Aliyunddns()
  while True:
    local_ip = ali.CheckLocalip()
    # 这里设置检测的时间间隔，单位秒
    time.sleep(60)