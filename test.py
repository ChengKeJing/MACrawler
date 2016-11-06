import json
from virustotal import *

vt = Virustotal()
a = "http://www.baidu.com/"
b = "www.google.com"
c = "www.baidu.com\nwww.google.com\n"
d = vt.scanURL(c)
print(d)

# result = vt.rscBatchReport('e4521212ca78e142eeebe66084f4c8aae5de500822cfd75460bf33fe888d4b39-1478349930, dd014af5ed6b38d9130e3f466f850e46d21b951199d53a18ef29ee9341614eaf-1478349757,')

# test = json.dumps(result)
# arr = json.loads(test)
# print (arr[0]['positives'] == 0)