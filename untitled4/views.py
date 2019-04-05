# 和urls是写函数的对应关系
# 初始三件套必写：render渲染，redirect跳转到一个网页，HttpResponse跳转的内容
from django.shortcuts import HttpResponse,render,redirect
import pymysql
from tools import db_helper
from django.shortcuts import reverse
#调用mysql模块

def login(request):
    # return redirect('https://www.baidu.com/')
    # return HttpResponse('一个httpresponse返回的内容')
    # return render(request,'sample01.html')

    if request.method == 'POST':  # 拿到该html中form表单提交过来的数据
        name = request.POST.get('uname')  # get，把后台数据拉到这里面来
        password = request.POST.get('upwd')
        # print(name)
        # print(password)

        # 拿到form表单提交过来的数据去数据库检索，匹配则成功，反之报错
        if name == 'zuyu1234' and password == '123456':
            return redirect('https://www.baidu.com/')
            # return HttpResponse('<h1>登录成功</h1>')
        else:
            error = '用户名或密码错误！请重新输入！'
            # 登录失败就返回该html页面，即当前登录页面
            return render(request, 'sample01.html', {'error': error})  # 对应该html的error的style
    return render(request, 'sample01.html')

#mysql导入班级
def class_list(request):
    # 通过这个函数体现所有班级列表
    # 获取内容，去mysql数据库取内容,跟数据库关联
    conn = pymysql.connect(host='localhost', user='root', password='123456', database='s8', charset='utf8')
    # cursor()数据库光标,cursor=pymysql.cursors.DictCursor指定输出类型是字典
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # select id,cname from class加上order by id使之按照由小到大顺序排序
    sql = "select id,cname from class order by id;"
    cursor.execute(sql)
    ret = cursor.fetchall()
    print(ret)
    cursor.close()
    conn.close()
    # 用数据去填充html网页
    # request：封装数据
    return render(request, 'class_list.html', {'class_list': ret})

#删除班级:GET方法
def delete_class(request):
    #根据班级id删除，get的方法来找key即id，同时在class_list这个html对删除按键也做了修改来关联id
    #GET是默认的找数据的方法，不用像post要写if
    print(request.GET)
    class_id = request.GET.get('class_id')
    print(class_id)
    #去数据库里做删除，连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='123456', database='s8', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #数据库语句，如果id，就删除
    sql = "delete from class where id=%s;"
    #和数据库的class_id做关联
    cursor.execute(sql,class_id)
    #做要提交的操作,写closed把光标和连接关闭
    conn.commit()
    cursor.close()
    conn.close()
    #return HttpResponse('<h1>ok</h1>')
    #删除操作完成后自动跳转回这个html
    return redirect('/class_list/')

#添加班级：POST方法传信息到数据库
def add_class(request):
    #添加班级，POST方法
    if request.method == 'POST':
        class_name = request.POST.get('cname')
        conn = pymysql.connect(host='localhost', user='root', password='123456', database='s8', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 数据库语句，写班级名直接提交就添加进去了
        sql = "insert into class (cname) VALUE (%s);"
        # 和class_name做关联
        cursor.execute(sql, class_name)
        # 做要提交的操作,写closed把光标和连接关闭
        conn.commit()
        cursor.close()
        conn.close()
        #返回上面的数据库新建一个班级
        return redirect('/class_list/')
    return render(request,'add_class.html')

#班级名编辑：POST方法
def edit_class(request):
    #2:将修改好的传进去
    if request.method == 'POST':
        class_id =request.POST.get('id')
        class_name = request.POST.get('cname')
        conn = pymysql.connect(host='localhost', user='root', password='123456', database='s8', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 数据库语句，如果id，就添加
        sql = "update class set cname=%s where id=%s;"
        # 和数据库的class_id做关联
        cursor.execute(sql, (class_name,class_id))
        # 做要提交修改的操作,写closed把光标和连接关闭
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/class_list/')
    #1:取到要编辑的班级的id，取数据
    class_id = request.GET.get('class_id')
    #去数据库里做编辑，连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='123456', database='s8', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 数据库语句，如果id，就删除
    sql = "select id,cname from class where id=%s;"
    # 和数据库的class_id做关联
    cursor.execute(sql, class_id)
    ret = cursor.fetchone()
    # 做要提交的操作,写closed把光标和连接关闭
    cursor.close()
    conn.close()
    print(ret)
    return render(request,"edit_class.html",{"class_info":ret})

#mysql导入学生信息
def student_list(request):
    #去mysql数据库找学生信息
    conn = pymysql.connect(host='localhost', user='root', password='123456', database='s8', charset='utf8')
    # cursor()数据库光标,cursor=pymysql.cursors.DictCursor指定输出类型是字典
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 多表联查,mysql的student的cid和class的班级id相关联，得到班级信息
    #select student.id,sname,cname from student left join class c on student.cid = c.id;这条语句在console里写的，可验证
    #left join 是做链接用的，语句意思为把class表的class.id加到student的cid
    sql = "select student.id,sname,cname from student LEFT JOIN class on student.cid = class.id;"
    cursor.execute(sql)
    student_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request,'student_list.html',{'student_list':student_list})

#删除学生列表:更改和删除都用GET取数据的方法
def delete_student(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        conn = pymysql.connect(host='localhost', user='root', password='123456', database='s8', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "delete from student where id=%s;"
        # 和数据库的student_id做关联
        cursor.execute(sql, student_id)
        # 做要提交的操作,写closed把光标和连接关闭
        conn.commit()
        cursor.close()
        conn.close()
    return redirect('/student_list/')

#添加学生信息：POST方法
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


#学生名编辑，此次调用模块tools里面的文件db_helper的函数modify
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

#给老师表单写的函数，处理重复key，即一个老师多班级处理
def magic(data_o):
    tmp={}
    for i in data_o:
        if i["id"] not in tmp:
            tmp[i["id"]] = {"id":i["id"],"tname":i["tname"],"cname":[i["cname"]]}
        else:
            tmp[i["id"]]["cname"].append(i["cname"])
    data = list(tmp.values())
    print(data)
    return data

#展示老师列表
def teacher_list(request):
    #导入数据,order by id使mysql按照id由小到大顺序排序，老师的sql语句是三表联查，学生的sql语句是双表联查
    sql = "select teacher.id,tname,cname from teacher left join class_2_teacher on teacher.id = class_2_teacher.tid left join class on class_2_teacher.cid = class.id order by id;"
    #此次调用模块tools里面的文件db_helper的函数get_list查询多个数据
    teacher_list_o=db_helper.get_list(sql)
    #把查询到的数据用上方的函数做格式转换，方便页面渲染，最后得到的结果：
    #[{'id': 1, 'tname': '孙老师', 'cname': ['全栈3班', '全栈4班']}, {'id': 2, 'tname': '刘老师', 'cname': ['全栈五班']},
     #{'id': 3, 'tname': '韩老师', 'cname': ['全栈五班', '全栈一班']}, {'id': 4, 'tname': '皮老师', 'cname': ['全栈六班']},
     #{'id': 5, 'tname': '王老师', 'cname': ['全栈二班']}, {'id': 6, 'tname': 'andy', 'cname': ['全栈六班']},
     #{'id': 7, 'tname': 'pipi', 'cname': ['全栈七班', '全栈4班']}]
    teacher_list = magic(teacher_list_o)
    return render(request,"teacher_list.html",{"teacher_list":teacher_list})

#删除老师列表
def delete_teacher(request):
    #要删除，就要先知道删除哪一个老师，get取数据通过teacher.id
    teacher_id = request.GET.get("teacher_id")
    #删除的数据库sql语句
    sql = "delete from teacher where id=%s;"
    #去执行,此次调用模块tools里面的文件db_helper的函数modify单条语句
    db_helper.modify(sql,teacher_id)
    return redirect("/teacher_list/")

#添加老师的方法
def add_teacher(request,name=teacher_list):
    if request.method == "POST":
        tname=request.POST.get("tname")
        #使用getlist:可以取到多个cid，get只能取一个
        cid_list=request.POST.getlist("cid")
        #print(tname,cid_list)
        #去数据库里面输入信息
        sql1 = "insert into teacher (tname) values(%s);"
        new_teacher_id=db_helper.create(sql1,tname)
        #去更新class_2_teacher数据库
        sql2 = "insert into class_2_teacher(cid,tid) values(%s,%s);"
        #多次连接，多次提交的方式：
        #for cid in cid_list:
            #db_helper.create(sql2,[cid,new_teacher_id])

       #多次提交，一次连接的方式：db_helper.pl_modify(sql2,data)的方法和for cid in cid_list:的方法结果一致，但是运行速度更快，更简洁
        #将数据类型转换成支持批量操作的格式
        #executemany支持的格式如下：
        #[(cid,new_teacher_id),(cid,new_teacher_id)......]
        #cid_list[9.10,11]new_teacher_id=5---->(9,5)、(10,5)、(11,5)

        data = [(i,new_teacher_id) for i in cid_list]
        #db_helper.pl_modify(sql2,data)

        #使用面向对象的方式1：
        #db = db_helper.DBhelper()
        #db.pl_modify(sql2,data)
        #db.close()

        # 使用面向对象的方式2：
        with db_helper.DBHelper() as db:
            db.pl_modify(sql2,data)
        #以上几种方法都可添加
        #return redirect("/teacher_list/")
        return redirect(reverse(" ",args=name))



    sql = "select id,cname from class;"
    class_list=db_helper.get_list(sql)
    return render(request,"add_teacher.html",{"class_list":class_list})

#给edit_teacher写的函数
def magic2(arg):
    ret = {}
    for j in arg:
        # z赋值一个变量，方便重复写j[id]
        this_id = j["id"]
        if this_id not in ret:
            ret[this_id] = {"id": this_id, "tname": j["tname"], "cid": [j["cid"], ]}
        else:
            ret[this_id]["cid"].append(j["cid"])
    return list(ret.values())[0]

#老师信息编辑
def edit_teacher(request):
    if request.method == "POST":
        # 从表单里post过来的数据里面取得新的信息
        teacher_id = request.POST.get("id")
        #老师的新姓名
        teacher_name = request.POST.get("tname")
        #获取编辑后老师的授课班级
        cid_list = request.POST.getlist("cid")
        #以上操作完成了数据的获取工作，接下来就是更新老师的信息，去mysql数据库更新
        sql = "update teacher set tname=%s where id=%s;"
        with db_helper.DBHelper()as db:
            db.modify(sql,[teacher_name,teacher_id])
        #更新老师的授课班级----直接删除原来的，增加更新后的

        #先删除
        sql_del = "delete from class_2_teacher where tid=%s;"
        #再添加
        sql_add = "insert into class_2_teacher(tid,cid) values(%s,%s);"
        pl_data = [(teacher_id,i) for i in cid_list]
        #把老师信息和授课班级信息拼接起来，以便支持批量操作
        with db_helper.DBHelper() as db:
            db.modify(sql_del,[teacher_id])
            db.pl_modify(sql_add, pl_data)
        #至此更新完毕
        return redirect("/teacher_list/")

    teacher_id = request.GET.get('teacher_id')
    #此条语句显示了所有班级名称
    sql = "select id,cname from class;"
    #此条语句查询了老师和授课班级的信息（id，cid，tname）,三表联查语句，mysql的console里试写试试
    sql2="select teacher.id,tname,cid from teacher left join class_2_teacher on teacher.id =class_2_teacher.tid where tid = %s;"
    with db_helper.DBHelper() as db:
        class_list = db.get_list(sql)
        teacher_info_o = db.get_list(sql2,[teacher_id])
        teacher_info = magic2(teacher_info_o)
    return render(request, "edit_teacher.html", {"class_list": class_list,"teacher":teacher_info})

#老师表单的页面搜索框:此次只是模拟，一般是用Ajax，或者js编写
def search_teacher(request):
    #拿到搜索词
    search_str = request.POST.get("search_str")
    #去数据库查询;like使之模糊查询，即打出首字，即可查出所有首字为它的信息，where改为tname是因为按老师名字查询
    sql = "select teacher.id,tname,cname from teacher left join class_2_teacher on teacher.id =class_2_teacher.tid left join class on class_2_teacher.cid=class.id where tname like %s;"
    #"{}%".format(search_str),:占位符的一种
    #teacher_list_o是查询结果，teacher_list是返回结果
    with db_helper.DBHelper() as db:
        teacher_list_o=db.get_list(sql,["{}%".format(search_str),])
        teacher_list=magic(teacher_list_o)
    return render(request, "teacher_list.html", {"teacher_list": teacher_list})


def zdenglu(request):
    # 拿到该html中form表单提交过来的数据
    if request.method == 'POST':
        # get，把后台数据拉到这里面来
        name = request.POST.get('uname')
        password = request.POST.get('upwd')

        # 拿到form表单提交过来的数据去数据库检索，匹配则成功，反之报错
        if name == 'llcc12345' and password == '12345':
            return HttpResponse('<h2>登录成功</h2>')
        else:
            error = '用户名或密码错误！请重新输入！'
            # 登录失败就返回该html页面，即当前登录页面
            return render(request, 'zdenglu.html', {'error': error})
    return render(request, 'zdenglu.html')