from django.shortcuts import render,HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import os
from app01 import models
from django.views import View

# Create your views here.

def business_add(request):
    # models.Business.objects.create(caption='测试部')
    # models.Business.objects.create(caption='研发部')
    # models.Business.objects.create(caption='运维部')
    # models.Business.objects.create(caption='市场部')
    # models.Business.objects.create(caption='运营部')
    # models.Business.objects.create(caption='产品部')
    return redirect("/app01/business")

def business(request):
    v1 = models.Business.objects.all()
    # QuerySet类型
    #[obj(id,caption,code),obj(id,caption,code),obj(id,caption,code)....]

    v2 = models.Business.objects.all().values('id','caption')
    #这样就是只取这两个字段数据，也是QuerySet类型，但是v2取出来的数据就不是对象了而是变成了对应的字典
    # [{'id':1,'caption':'运维部'},{'id':1,'caption':'运维部'}]

    v3 = models.Business.objects.all().values_list('id','caption')
    #QuerySet类型
    #数据格式改变[(1,运维部),(2，研发部)....]

    return render(request,'business.html',{"v1":v1,"v2":v2,"v3":v3})


def host(request):
    if request.method == "GET":
        v1 = models.Host.objects.filter(nid__gt=0)
        v2 = models.Host.objects.filter(nid__gt=0).values('nid','hostname','b_id','b__caption')
        v3 = models.Host.objects.filter(nid__gt=0).values_list('nid','hostname','b_id','b__caption')
        b_list = models.Business.objects.all()
        return render(request,'host.html',{"v1":v1,"v2":v2,"v3":v3,"b_list":b_list})
    elif request.method == "POST":
        h = request.POST.get("hostname")
        ip = request.POST.get("ip")
        port = request.POST.get("port")
        b_id = request.POST.get("b_id")
        models.Host.objects.create(hostname=h,
                                   ip=ip,
                                   port=port,
                                   # b=models.Business.objects.get(id=b),  #这里的b就是一个对象，后边赋值的时候也必须是对象才行，需要查询两次数据库比较麻烦
                                   b_id=b_id)
        #这里return如果是render(reuqest,"host.html")这样的话等于是把页面从新渲染了，这时候页面上是没有数据的
        return redirect("/app01/host")

class host_del(View):
    def dispatch(self, request, *args, **kwargs):
        result = super(host_del,self).dispatch(request, *args, **kwargs)
        return result

    def post(self, request, *args, **kwargs):
        ret = {"status": True, 'error': None, 'data': None}
        try:
            mes_error = ""
            hid = request.POST.get("hid")
            models.Host.objects.filter(nid=hid).delete()
        except Exception as e:
            ret["status"] = False
            ret["error"] = "请求错误"
        #return redirect("/app01/host")
        return HttpResponse(json.dumps(ret))

import json
def test_ajax(request):
    ret = {"status":True,'error':None,'data':None}
    try:
        mes_error = ""
        #print(request.method,request.GET.get('user'),request.GET.get('pwd'),sep='\t')
        #import time
        #time.sleep(5)
        h = request.POST.get("hostname")
        ip = request.POST.get("ip")
        port = request.POST.get("port")
        b_id = request.POST.get("b_id")
        #print(h,ip,port,b_id)
        if h and len(h) > 5:
            models.Host.objects.create(hostname=h,
                                       ip=ip,
                                       port=port,
                                       b_id=b_id)
            #return HttpResponse('OK')
        else:
            #return HttpResponse('太短了')
            ret["status"] = False
            ret["error"] = "太短了"
    except Exception as e :
        ret["status"] = False
        ret["error"] = "请求错误"
    return HttpResponse(json.dumps(ret))



def edit_ajax(request):
    ret = {"status":True,'error':None,'data':None}
    try:
        mes_error = ""
        nid = request.POST.get('nid')
        h = request.POST.get("hostname")
        ip = request.POST.get("ip")
        port = request.POST.get("port")
        b_id = request.POST.get("b_id")
        #print(h,ip,port,b_id)
        if h and len(h) > 5:
            models.Host.objects.filter(nid=nid).update(
                hostname=h,
                ip=ip,
                port=port,
                b_id=b_id
            )
        else:
            ret["status"] = False
            ret["error"] = "太短了"
    except Exception as e :
        ret["status"] = False
        ret["error"] = "请求错误"
    return HttpResponse(json.dumps(ret))


def app(request):
    if request.method == "GET":
        app_list = models.Application.objects.all()
        host_list = models.Host.objects.all()
        #for row in app_list:
            #print(row.name,row.r.all())
        return render(request,"app.html",{"app_list":app_list,"host_list":host_list})
    elif request.method == "POST":
        #下面这段是以form表单方式提交过来的数据
        app_name = request.POST.get('app_name')
        host_list = request.POST.getlist('host_list')
        print(app_name,host_list)
        obj = models.Application.objects.create(name=app_name)
        obj.r.add(*host_list)
        return redirect("/app01/app")

def ajax_add_app(request):
    ret = {'status':True,'error':None,'data':None}
    try:
        # print(request.POST.get('app_name'))
        # print(request.POST.getlist('host_list'))
        app_name = request.POST.get('app_name')
        host_list = request.POST.getlist('host_list')
        if app_name:
            obj = models.Application.objects.create(name=app_name)
            obj.r.add(*host_list)
            # print(app_name)
        else:
            ret["status"] = False
            ret["error"] = "应用名称不能为空"
    except Exception as e :
        ret["status"] = False
        ret["error"] = "请求错误"
    return HttpResponse(json.dumps(ret))

def ajax_edit_app(request):
    ret = {'status':True,'error':None,'data':None}
    try:
        # print(request.POST.get('app_name'))
        # print(request.POST.getlist('host_list'))
        aid = request.POST.get('aid')
        app_name = request.POST.get('app_name')
        host_list = request.POST.getlist('host_list')
        #print(aid,app_name,host_list)
        if app_name:
            models.Application.objects.filter(id=aid).update(name=app_name)
            obj = models.Application.objects.get(id=aid)
            obj.r.set(host_list)
        else:
            ret["status"] = False
            ret["error"] = "应用名称不能为空"
    except Exception as e :
        ret["status"] = False
        ret["error"] = "请求错误"
    return HttpResponse(json.dumps(ret))

def ajax_del_host_app(request):
    ret = {'status':True,'error':None,'data':None}
    try:
        aid = request.POST.get('aid')
        hid = request.POST.get('hid')
        print(aid,hid)
        if aid:
            obj = models.Application.objects.get(id=aid)
            obj.r.remove(hid)
        else:
            ret["status"] = False
            ret["error"] = "应用名称不能为空"
    except Exception as e :
        ret["status"] = False
        ret["error"] = "请求错误"
    return HttpResponse(json.dumps(ret))