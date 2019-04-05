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

def student_list(request):
    # 1. 去数据库里查询所有学生的信息
    # 去数据库里查询当前班级的信息
    conn = pymysql.connect(host="localhost", user="root", password="123456", database="s8", charset="utf8")
    # 指定输出的结果类型是字典
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select student.id, sname, cname from student LEFT JOIN class on student.cid = class.id;"
    cursor.execute(sql)
    student_list = cursor.fetchall()
    return render(request,"student_list.html",{"student_list":student_list})


def delete_student(request):
    if request.method == "GET":
        student_id = request.GET.get('student_id')
        conn = pymysql.connect(host="localhost", user="root", password="123456", database="s8", charset="utf8")
        # 指定输出的结果类型是字典
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "delete from student where id=%s;"
        cursor.execute(sql, student_id)
        # 作要提交的操作
        conn.commit()
        cursor.close()
        conn.close()
    return redirect("/student_list/")


def add_student(request):
    if request.method == "POST":
        #表示页面填写完新学生的相关信息,并点击按钮
        #从post过来的数据里面取得新的学生的姓名和班级名称
        student_name = request.POST.get('sname')
        class_id = request.POST.get('cid')
        conn = pymysql.connect(host="localhost", user="root", password="123456", database="s8", charset="utf8")
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "insert into student (sname,cid) values(%s,%s);"
        cursor.execute(sql,[student_name,class_id])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/student_list/")
    else:
        conn = pymysql.connect(host="localhost", user="root", password="123456", database="s8", charset="utf8")
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "select id,cname from class;"
        cursor.execute(sql)
        class_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render(request,"add_student.html",{"class_list":class_list})

from tools import db_helper
def edit_student(request):
    if request.method == "POST":
        student_id = request.POST.get("id")
        new_student_name = request.POST.get("sname")
        new_student_class = request.POST.get("cid")
        sql = "update student set sname=%s,cid=%s where id=%s;"
        db_helper.modify(sql,[new_student_name,new_student_class,student_id])
        #去数据库更新
        # conn = pymysql.connect(host="localhost", user="root", password="123456", database="s8", charset="utf8")
        # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # sql = "update student set sname=%s,cid=%s where id=%s;"
        # cursor.execute(sql,[new_student_name,new_student_class,student_id])
        # conn.commit()
        # cursor.close()
        # conn.close()
        return redirect("/student_list/")
    else:
        #从URL里取到当前编辑学生的ID值
        student_id = request.GET.get('student_id')
        sql = "select id,sname,cid from student where id=%s;"
        ret = db_helper.get_one(sql,student_id )
        sql2 = "select id,cname from class;"
        class_list = db_helper.get_list(sql2)
        #去数据库里面取当前的学生的id，sname和cid
        # conn = pymysql.connect(host="localhost", user="root", password="123456", database="s8", charset="utf8")
        # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # sql = "select id,sname,cid from student where id=%s;"
        # cursor.execute(sql,student_id )
        # ret = cursor.fetchone()
        # sql2 = "select id,cname from class;"
        # cursor.execute(sql2)
        # class_list = cursor.fetchall()
        # cursor.close()
        # conn.close()
        return render(request,"edit_student.html",{"student":ret,"class_list":class_list})


