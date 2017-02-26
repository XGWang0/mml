


a = "aaa=123&tty=sdkfkj&qwe=dklfljsdf"

import re

print(dict([i.split("=") for i in a.split("&")]))
list1 = re.split("&", a)

print(dict([i.split("=") for i in list1]))

format = "{0[0]:^8} {0[1]:^8} {0[2]:^8}"

w = ["111", '222', '333']
c = list(map(lambda i: str(i), [1, 'src1', None]))
print(format.format(c))
#print(format.format(str(c[0]), str(c[1]), str(c[2])))
#print([(key, value) for (key, value) in list1])
#print(dict((key, value) for (key, value) in list1))