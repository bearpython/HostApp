from django.db import models

# Create your models here.

# class Foo(models.Model):
#     name = models.CharField(max_length=32)


class Business(models.Model):
    #id
    caption = models.CharField(max_length=32)
    #在已经创建好的表，并且添加数据之后在创建一个字段，这时候在执行命令时候会提示原有数据的这个新增字段要写什么值
    # 第二种解决方式是在code字段这里写一个default='sa'或者写上null=True
    code = models.CharField(max_length=32)
    #fk = models.ForeignKey(to='Foo',to_field='id',null=True)


class Host(models.Model):
    nid = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=32,db_index=True,verbose_name="主机名")
    # ip = models.IPAddressField() #这种写法是django1.10版本以下的
    ip = models.GenericIPAddressField(db_index=True)  #db_index=True 创建索引
    #GenericIPAddressField可以带参数protocol='ipv4'或者'both' ,both是ipv4和ipv6都支持
    port = models.IntegerField()
    b = models.ForeignKey(to='Business',to_field='id')


class Application(models.Model):
    name = models.CharField(max_length=32)
    #下边这行是自动创建关系方式
    r = models.ManyToManyField('Host')


#自定义关系创建方式
# class HostToApp(models.Model):
#     hobj = models.ForeignKey(to='Host',to_field='nid')
#     aobj = models.ForeignKey(to='Application',to_field='id')
