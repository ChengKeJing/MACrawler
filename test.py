import json
from virustotal import *

vt = Virustotal()
a = "http://www.baidu.com/"
b = "www.google.com"
c = "www.baidu.com\nwww.google.com\n"
e = 'http://law.nus.edu.sg/pdfs/cbfl/events/morriss_rifcge.pdf\n'
f = "www.tttttttt.com"
# g = vt.scanURL(f)
# print(g)
resource_list = []
resource_list.append("bf6373382b1de0e5c205ce47b38b9ade57df1b9de4a8ed10823a7ad50176d1db-1478424155")
resource_list.append(', '  + "b3d43aa2f34675a6c0eac6f219597bf5b515e919b14f74fe765007aa2404515d-1478424155")
res_str = ''.join(resource_list)
print(res_str)
d = vt.urlReport("bf6373382b1de0e5c205ce47b38b9ade57df1b9de4a8ed10823a7ad50176d1db-1478424155\nb3d43aa2f34675a6c0eac6f219597bf5b515e919b14f74fe765007aa2404515d-1478424155")
print(d[0])

# result = vt.rscBatchReport('e4521212ca78e142eeebe66084f4c8aae5de500822cfd75460bf33fe888d4b39-1478349930, dd014af5ed6b38d9130e3f466f850e46d21b951199d53a18ef29ee9341614eaf-1478349757,')

# test = json.dumps(result)
# arr = json.loads(test)
# print (arr[0]['positives'] == 0)