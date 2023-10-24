from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from shortener.models import Users

# Create your views here.

def index(request):
    user = Users.objects.filter(username='rowanpark').first()
    # user = Users.objects.get(username='rowanpark')
    email = user.email if user else 'Anonymous User!'
    print(email)

    # print(request.user.is_authenticated)  # 로그인 유무
    # if request.user.is_authenticated is False:
    #     email = 'Anonymous User!'
    #     print(email)

    return render(request, 'base.html', {'welcome_msg': f'Hello {email}', 'hello': 'hello!'})

# def redirect_test(request):
#     print('Go Redirect')
#     return redirect('index_name')

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