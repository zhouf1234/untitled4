list1 = [
    {'id': 5, 'tname': '金老板', 'cid': 11},
    {'id': 5, 'tname': '金老板', 'cid': 10},
    {'id': 5, 'tname': '金老板', 'cid': 12}
]

#把上述列表变成下面的字典形式
list2 = {"id": 5, "tname": "金老板", "cid": [11, 10, 12]}

#第一种方法
#list3={}
#for i in list1:
     #print(i)
    #if i["id"] not in list3:
        #list3[i["id"]]=i
        #list3[i["id"]]["tname"]=i["tname"]
        #list3[i["id"]]["cid"]=[i["cid"],]
    #else:
        #list3[i["id"]]["cid"].append(i["cid"])
 #ret = (list(list3.values())[0])
#print(ret)
#print(type(ret))
#print(list3[5])
#print(type(list3))
#print()

#第二种方法
dic = {}
for j in list1:
    #z赋值一个变量，方便重复写j[id]
    this_id = j["id"]
    if this_id not in dic:
        dic[this_id] = {"id":this_id,"tname":j["tname"],"cid":[j["cid"],]}
    else:
        dic[this_id]["cid"].append(j["cid"])
print(dic)
print(list(dic.values())[0])
