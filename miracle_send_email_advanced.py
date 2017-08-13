#encodig=utf-8
# _*_ coding:utf-8 _*_

import os  
import smtplib  
import mimetypes  
import xlrd 
import string
import pymysql
from email.MIMEMultipart import MIMEMultipart  
from email.MIMEBase import MIMEBase  
from email.MIMEText import MIMEText  
from email.MIMEAudio import MIMEAudio  
from email.MIMEImage import MIMEImage  
from email import encoders
from email.utils import parseaddr, formataddr
from email.header import Header
from email.Encoders import encode_base64
from email.utils import COMMASPACE


#######################################################################
# #使用该脚本之前请填入以下参数：

count=0             #本期简报的期数
account_number=18   #这次发送简报最开始使用第几个邮箱(我是18)(从1开始)
donated=0           #这次发送简报是有捐赠版(1)还是无捐赠版(0)
tired=0       #计算何时应该更换下一个工作邮箱进行操作，若今天还
# #没有使用该当邮箱，请让其为零，反之，填入使用次数整除50的结果
#######################################################################
account_number=account_number-1
def connect_db():
    # config of the database
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '0000',
        'db': 'work_brief',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    # Connect to the database
    connection = pymysql.connect(**config)
    #print "db ok"
    return connection

connection=connect_db();
try:
    with connection.cursor() as cursor:
        # 执行sql语句，进行查询
        sql1 = 'SELECT subject, content, file_path, file_path_donated FROM message where id=%s'
        cursor.execute(sql1, count)
        # 获取查询结果
        result = cursor.fetchone()
        subject=(result["subject"]).encode(encoding='gb2312',errors='ignore')    #邮件主题.encode("gb2312")
        if(donated==0):
            file_path=(result["file_path"]).encode(encoding='gb2312',errors='ignore')    #附件.encode("gb2312")  .encode(encoding='UTF-8',errors='strict')
        else:
            file_path=(result["file_path_donated"]).encode(encoding='gb2312',errors='ignore')
        #print file_path
        content=(result["content"]).encode(encoding='gb2312',errors='ignore')    #邮件正文内容，用utf-8无bom格式编码.encode("gb2312")
        
        sql2 = 'SELECT email FROM test'    #记住把test改成mydutypart！！！！！！！！！！！！
        cursor.execute(sql2)
        # 获取查询结果
        result2 = cursor.fetchall()
        #num=0
        emails=[]
        for item in result2:
            emails.append(item['email'])
            #num=num+1
        
        sql3 = 'SELECT account, code FROM work_account'
        cursor.execute(sql3)
        # 获取查询结果
        result3 = cursor.fetchall()
        account_using=result3[account_number]
        gmailUser = account_using['account']
        #print gmailUser
        gmailPassword =account_using['code']
    # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
    connection.commit()
 
finally:
    connection.close();
    

#path = u"E:\测试邮箱列表.xls".encode("gb2312") #发送邮件列表
#file_path = u"E:\Newsletter_20150916_147.pdf".encode("gb2312") #附件
#email_name = u'E-mail Address' #发送邮件列表中邮箱信息列头

    
    
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'gb2312').encode(), \
        addr.encode('gb2312') if isinstance(addr, unicode) else addr))
 
def sendMail(gmailUser, gmailPassword, subject, text, other, *attachmentFilePaths):   
    recipient = []  
    
    # 设置根容器属性
    msg = MIMEMultipart()  
    msg['From'] = _format_addr(u'Newsletter Dian <%s>' % gmailUser) 
    msg['To'] = COMMASPACE.join(recipient)
    msg['Bcc'] = COMMASPACE.join(other)
    msg['Subject'] = Header(subject, 'gb2312').encode()  
    msg.attach(MIMEText(content, 'plain', 'gb2312'))  
   
    for attachmentFilePath in attachmentFilePaths:  
        msg.attach(getAttachment(attachmentFilePath))  

    mailServer = smtplib.SMTP('smtp.gmail.com', 25)  #QQ邮箱需要改为smtp.qq.com
    mailServer.ehlo()  
    mailServer.starttls()  
    mailServer.ehlo()  
    mailServer.login(gmailUser, gmailPassword)  
    mailServer.sendmail(gmailUser, recipient+other, msg.as_string())  
    mailServer.close()  
   
    print "Sent  email  to  ", other 
   
def getAttachment(attachmentFilePath):  
    contentType, encoding = mimetypes.guess_type(attachmentFilePath)  
   
    if contentType is None or encoding is not None:  
        contentType = 'application/octet-stream' 
   
    mainType, subType = contentType.split('/', 1)  
    file = open(attachmentFilePath, 'rb')  
   
    if mainType == 'text':  
        attachment = MIMEText(file.read())  
    elif mainType == 'message':  
        attachment = email.message_from_file(file)  
    elif mainType == 'image':  
        attachment = MIMEImage(file.read(),_subType=subType)  
    elif mainType == 'audio':  
        attachment = MIMEAudio(file.read(),_subType=subType)  
    else:  
        attachment = MIMEBase(mainType, subType)  
    attachment.set_payload(file.read())  
    encode_base64(attachment)    
   
    file.close()  

    ## 设置附件头    
    attachment.add_header('Content-Disposition', 'attachment',   filename=os.path.basename(attachmentFilePath))  
    return attachment  


def OneUsrSendMail():
    global tired
    #global account_number
    allsent=0
    rested=len(emails)
    while(rested!=0):
        if(rested>=50):
            sendMail(gmailUser, gmailPassword, subject, content, emails[allsent:(allsent+50)], file_path)
            allsent=allsent+50
            print ("这50封邮件由该工作邮箱发出：%s ，目前已经发送了%d 封邮件，马上发送余下部分，请稍等...\n" % (gmailUser.encode('UTF-8'),allsent)).decode('UTF-8')
            rested=rested-50
        else:
            sendMail(gmailUser, gmailPassword, subject, content, emails[allsent:], file_path)
            allsent=len(emails)
            print ("这 %d 封邮件由该工作邮箱发出：%s ，已经发送了全部的 %d 封邮件，谢谢使用:)" % ((allsent%50),gmailUser.encode('UTF-8'),allsent)).decode('UTF-8')
            rested=0
        if(tired>=8):
            resetMail()
        else:
            tired=tired+1

            
def resetMail():
    global account_using
    global account_number
    account_number=account_number+1
    account_using=result3[account_number]
    global gmailUser
    gmailUser=account_using['account']
    global gmailPassword
    gmailPassword =account_using['code']    
    global tired
    tired=0
#sendMail(gmailUser, gmailPassword, subject, content, emails, file_path)
#print result3
OneUsrSendMail() #账号，密码
