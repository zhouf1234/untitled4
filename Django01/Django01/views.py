import pymysql
from django.shortcuts import HttpResponse,render,redirect

def login(request):
    if request.method == "POST":
        #拿到form表单提交过来的数据
        name = request.POST.get('uname')
        password = request.POST.get('upwd')
        #拿到form表单提交过来的数据去数据库中做检索，如果匹配则登录成功，否则登录失败
        if name == "zuyu1234" and password == "123456":
            return redirect("http://www.baidu.com")
        else:
            error = "用户名和密码输入有误!"
            return render(request,'sample01.html',{"error":error})
    return render(request,'sample01.html')

def class_list(request):
    #这个函数展示所有班级的列表
    #1.去数据库取数据
    conn = pymysql.connect(host="localhost",user="root",password="123456",database="s8",charset="utf8")
    #指定输出的结果类型是字典
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select id, cname from class order by id;"
    cursor.execute(sql)
    ret = cursor.fetchall()
    print(ret)
    #2.用数据去填充HTML页面
    return render(request,"class_list.html",{"class_list":ret})

def delete_class(request):
    #根据班级的ID删除
    #班级的ID从哪里来?
    print(request.GET)
    class_id = request.GET.get("class_id")
    print(class_id)
    #去数据库里删除
    conn = pymysql.connect(host="localhost",user="root",password="123456",database="s8",charset="utf8")
    #指定输出的结果类型是字典
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "delete from class where id=%s;"
    cursor.execute(sql,class_id)
    #作要提交的操作
    conn.commit()
    cursor.close()
    conn.close()
    # return HttpResponse("<h1>OK!</h1>")
    return redirect("/class_list/")

#添加班级
def add_class(request):
    if request.method == "POST":
        class_name = request.POST.get("cname")
        conn = pymysql.connect(host="localhost", user="root", password="123456", database="s8", charset="utf8")
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "insert into class (cname) VALUE (%s);"
        cursor.execute(sql, class_name)
        # 作要提交的操作
        conn.commit()
        cursor.close()
        conn.close()
        #上面去数据库里新建一个班级
        return redirect("/class_list/")
    return render(request,"add_class.html")


#新页面编辑
def edit_class(request):
    if request.method == "POST":
        class_id = request.POST.get("id")
        class_name = request.POST.get("cname")
        #去数据库里做更新
        conn = pymysql.connect(host="localhost", user="root", password="123456", database="s8", charset="utf8")
        # 指定输出的结果类型是字典
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "update class set cname=%s where id=%s;"
        cursor.execute(sql,(class_name,class_id))
        #提交修改
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/class_list/")



    #取到被编辑的班级ID
    class_id = request.GET.get('class_id')
    # 去数据库里查询当前班级的信息
    conn = pymysql.connect(host="localhost", user="root", password="123456", database="s8", charset="utf8")
    # 指定输出的结果类型是字典
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select id,cname from class where id=%s;"
    cursor.execute(sql, class_id)
    ret = cursor.fetchone()
    cursor.close()
    conn.close()
    print(ret)
    return render(request,"edit_class.html",{"class_info":ret})
