'''
DDNS 主程序 使用阿里云的SDK发起请求
Created By Martin Huang on 2018/5/20
修改记录：
2018/5/20 => 第一版本
2018/5/26 => 增加异常处理、Requst使用单例模式，略有优化
2018/5/29 => 增加网络连通性检测，只有联通时才进行操作，否则等待
2018/6/10 => 使用配置文件存储配置，避免代码内部修改(需要注意Python模块相互引用问题)
2018/9/24 => 修改失败提示信息
'''
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.acs_exception.exceptions import ClientException
from Utils import Utils
import time
import argparse
import get_ip

def DDNS(ip_addr, use_v6):
  client = Utils.getAcsClient()
  recordId, server_ip = Utils.getRecordId(\
    Utils.getConfigJson().get('Second-level-domain'))
  if use_v6:
    type = 'AAAA'
  else:
    type = 'A'
  print({'type': type, 'ip':ip_addr})

  if server_ip == ip_addr:
    print("ip same")
    return True

  request = Utils.getCommonRequest()
  request.set_domain('alidns.aliyuncs.com')
  request.set_version('2015-01-09')
  request.set_action_name('UpdateDomainRecord')
  request.add_query_param('RecordId', recordId)
  request.add_query_param('RR', Utils.getConfigJson().get('Second-level-domain'))
  request.add_query_param('Type', type)
  request.add_query_param('Value', ip)
  response = client.do_action_with_exception(request)
  return response

def GetIntervalTime():
  return 120

g_last_ip = ''
def RunDDns():
  getip_manager = get_ip.Aliyunddns()

  while True:
    global g_last_ip
    ip = getip_manager.CheckLocalip()
    if ip != g_last_ip:
      try:
        DDNS(ip, False)
      except (ServerException,ClientException) as reason:
        print("failed:" + reason.get_error_msg())
      except Exception as err:
        print("failed, unknow:" + str(err))
      g_last_ip = ip
    time.sleep(GetIntervalTime())

if __name__ == "__main__":
  RunDDns()