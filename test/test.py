# coding: UTF-8
"""
u = u'汉'
print repr(u) # u'\u6c49'
s = u.encode('UTF-8')
print repr(s) # '\xe6\xb1\x89'
u2 = s.decode('UTF-8')
print repr(u2) # u'\u6c49'
 
# 对unicode进行解码是错误的
# s2 = u.decode('UTF-8')
# 同样，对str进行编码也是错误的
# u2 = s.encode('UTF-8')

"""
"""

f = open('test.txt')
s = f.read()
f.close()
print type(s) # <type 'str'>
# 已知是GBK编码，解码成unicode
u = s.decode('GBK')
 
f = open('test.txt', 'w')
# 编码成UTF-8编码的str
s = u.encode('UTF-8')
f.write(s)
f.close()
"""
a=222
u=u"的顺丰到付"
print ("sfsdsfsf爽肤水%s" % u.encode('UTF-8')).decode('UTF-8')
#print ("fsadfs客家话上岛咖啡%d 递四方速递 %s" % a, u).decode('UTF-8').encode('gbk')