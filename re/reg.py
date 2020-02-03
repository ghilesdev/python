import re

pattern=re.compile('ello')
print(pattern.match("hello world", 1))
print(pattern.search("hello world"))

str="hello155659è(_zççç))àç"
res=re.sub("\D", "", str)
print("result of substitution is ", res)