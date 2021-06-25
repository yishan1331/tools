# -*- coding: utf-8 -*-                                                                                      
import redis
from datetime import datetime
import subprocess
import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr,parseaddr

def _readConfig():
    print "#######_readConfig########"
    dicConfig = {}
    try:
        CONFPATH = "/var/www/spdpaas/config/constants.conf"

        FILECONFIG = ConfigParser.ConfigParser()
        FILECONFIG.read(CONFPATH)

        dicConfig = {
            'celery_broker_ip': FILECONFIG.get('CeleryBroker', 'ip'),
            'celery_broker_port': FILECONFIG.get('CeleryBroker', 'port'),
            'celery_broker_password': FILECONFIG.get('CeleryBroker', 'password'),
            'celery_broker_db': FILECONFIG.get('CeleryBroker', 'db'),
            'email_host': FILECONFIG.get('Email', 'host'),
            'email_user': FILECONFIG.get('Email', 'user'),
            'email_password': FILECONFIG.get('Email', 'password'),
            'email_recipient': FILECONFIG.get('Email', 'recipient'),
            'server_name': FILECONFIG.get('Server', 'name'),
            'server_type': FILECONFIG.get('Server', 'type'),
            'server_ip': FILECONFIG.get('Server', 'ip'),
        }

        print "~~~~dicConfig~~~~~"
        print dicConfig

    except Exception as e:
        print "~~~~_readConfig error~~~~"
        print e
    finally:
        return dicConfig

dicConfig = _readConfig()

POOL = redis.ConnectionPool(host=dicConfig.get("celery_broker_ip"), port=dicConfig.get("celery_broker_port"), db=dicConfig.get("celery_broker_db"),password=dicConfig.get("celery_broker_password"))

dbRedis = redis.Redis(connection_pool=POOL)

queuelen = dbRedis.llen("L-queue1")

recipient = dicConfig.get("email_recipient")
subject = '緊急通知'
body = 'Server Name : {}<br>Server IP : {}<br>Notification : "L-queue1"已經壅塞，長度：{} '.format(
    dicConfig.get("server_name"),
    dicConfig.get("server_ip"),
    queuelen)

# 方法一：透過subprocess直接執行linux mail指令寄送
# def send_message(recipient, subject, body):
#     try:
#         process = subprocess.Popen(['mail', '-s', subject, recipient],stdin=subprocess.PIPE)
#         process.communicate(body)
#         print "  -> 已寄緊急通知信"
#     except Exception as error:
#         print "error:",error

# 方法二：透過python內建smtplib進行寄送
class EmailConfig():
    def __init__(self):
        self.host = dicConfig.get("email_host")
        self.user = dicConfig.get("email_user")
        self.password = dicConfig.get("email_password")
    
    def set_mail_msg(self,maildata):
        self.mail_msg = '<div class="emailtable" style="margin:10px">\
        <div>{}</div></div>'.format(maildata["emailContent"])
    
    def sendemail(self,maildata):
        self.maildata = maildata
        # print "===============in sendemail=================="
        # print datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[::]
        status = True
        try:
            # print "===============in sendemail 1=================="
            # print datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[::]
            SMTPserver = smtplib.SMTP(self.host, 587) # 發件人郵箱中的SMTP伺服器

            # print "===============in sendemail 2=================="
            # print datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[::]
            SMTPserver.ehlo()  # 傳送SMTP 'ehlo' 命令
            SMTPserver.starttls() #加密文件，避免私密信息被截取

            # print "===============in sendemail 3=================="
            # print datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[::]
            SMTPserver.login(self.user, self.password) # 括號中對應的是發件人郵箱賬號、郵箱密碼

            for data in self.maildata:
                self.set_mail_msg(data)
                msg = MIMEText(self.mail_msg, 'html', 'utf-8')
                msg['From']=self.user
                msg['Subject']=data["emailTitle"] # 郵件的主題，也可以說是標題

                # print "~~~~msg~~~~"
                # print msg

                msg['To']= ",".join(data["emailAddress"])
                recipients = data["emailAddress"]

                # print "~~~~recipients~~~~"
                # print recipients

                # print "===============in sendemail 8=================="
                # print datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[::]
                
                SMTPserver.sendmail(self.user,recipients,msg.as_string()) # 括號中對應的是發件人郵箱賬號、收件人郵箱賬號、傳送郵件

                # print "===============in sendemail 9=================="
                # print datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[::]

        except Exception as e: # 如果 try 中的語句沒有執行，則會執行下面的 ret=False
            # print "===============in sendemail Exception=================="
            # print datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[::]
            print "~~~~e~~~~~"
            print e
            status = False
        finally:
            if 'SMTPserver' in locals().keys():
                SMTPserver.quit() # 關閉會話
                SMTPserver.close() #關閉SMTP連接

            return status
    
    #=========================================
    #格式化email的头部信息，不然会出错，当做垃圾邮件
    #=========================================
    def _format_addr(self,s):
        name, addr = parseaddr(s)
        # 防止中文问题，进行转码处理，并格式化为str返回
        return formataddr((Header(name,charset="utf-8").encode(),addr.encode("uft-8") if isinstance(addr, unicode) else addr))

print "time:",datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[::],"| this queuelen -> ",queuelen
if queuelen > 10000:
    # send_message(recipient, subject, body)
    send = EmailConfig()
    msg_ok = "email sent successfully"
    msg_error = "email delivery failed"
    #發送成功
    if send.sendemail([{
        "emailTitle":subject,
        "emailAddress":[recipient],
        "emailContent":body
        }]):
        print "time:",datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[::],"|",msg_ok
    #發送失敗
    else:
        print "time:",datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[::],"|",msg_error