from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from shortener.forms import RegisterForm, LoginForm
from shortener.models import Users


def index(request):
    return render(request, 'base.html')


@csrf_exempt  # csrf 체크 면제
def get_user(request, user_id):
    print(user_id)
    if request.method == 'GET':
        abc = request.GET.get('abc')
        xyz = request.GET.get('xyz')
        user = Users.objects.filter(pk=user_id).first()
        return render(request, 'base.html', {'user': user, 'params': [abc, xyz]})
    elif request.method == 'POST':
        username = request.GET.get('username')
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)
        return JsonResponse(status=201, data=dict(msg='You just reached with Post Method!'), safe=False)  # 한글을 보낼 경우에 'safe=False'


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        msg = '올바르지 않은 데이터 입니다.'
        if form.is_valid():
            form.save() 
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = '회원가입 완료'
        return render(request, 'register.html', {'form': form, 'msg': msg})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


def login_view(request):
    is_ok = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            msg = '올바른 이메일과 패스워드를 입력하세요.'
            try:
                u = Users.objects.get(user__email=email)  # email=email -> user__email=email
                # Users: 우리가 1:1 매핑을 만든 모델, 여기엔 이메일이 없다
                # __: 참조키를 타고 그 다음 테이블로 넘어가서 서치를 해달라
            except Users.DoesNotExist:
                pass  # '파이써닉'하게
            else:  # 예외가 발생하지 않았을 때 실행되는 코드
                if u.user.check_password(raw_password):  # user.check_password -> user.user.check_password -> u.user.check_password
                    msg = None
                    login(request, u.user)  # user -> user.user -> u.user
                    is_ok = True
                    request.session['remember_me'] = remember_me
                    if not remember_me:
                        request.session.set_expiry(0)  # 브라우저를 닫으면 세션이 즉시 만료
    else:
        msg = None
        form = LoginForm()
    print('REMEMBER_ME: ', request.session.get('remember_me'))
    return render(request, 'login.html', {'form': form, 'msg': msg, 'is_ok': is_ok})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def list_view(request):
    page = int(request.GET.get('p', 1))
    users = Users.objects.all().order_by('-id')
    paginator = Paginator(users, 10)  # 두번째 인덱스: 한페이지당 노출될 데이터 수
    users = paginator.get_page(page)
    return render(request, 'boards.html', {'users': users})
