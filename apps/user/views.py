from django.shortcuts import render, redirect,reverse
import re
from  itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from  itsdangerous import SignatureExpired
from django.views.generic import View
from  django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect,Http404,HttpRequest,HttpResponse
# Create your views here.
from apps.user.models import User
from django.contrib.auth import authenticate
# 显示注册用户页面


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 接受数据
        # 获取用户名称 密码 邮箱
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 数据校验
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱不合法'})
        # 校验协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        # 校验用户名
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        else:
            # 用户存在
            return render(request, 'register.html', {'errmsg': '用户名已注册'})
        # 注册用户
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        # 生成激活连接和token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'conform': user.id}
        token = serializer.dumps(info)
        token = token.decode()
        # 发邮件
        subject = '天天生鲜欢迎信息'
        message = 'hh'
        sender = settings.EMAIL_FROM
        receiver = [email]
        html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/>' \
                       '<a href="http://127.0.0.1:8000/user/active/%s">' \
                       'http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)
        send_mail(subject, message, sender, receiver, html_message=html_message)
        return redirect(reverse('goods:index'))



class ActiveView(View):

    def get(self, request,token):

        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['conform']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接已过期')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')
    def post(self,request):
        pass
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})
        user = authenticate(username='www1368', password='12345678')
        if user is not None:
            if user.is_active:
                # 加cookie session
                return redirect(reverse('goods:index'))
            else:
                return render(request, 'login.html', {'errmsg': '该账户没有激活'})
        else:
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})





