from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geoip2 import GeoIP2
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from ratelimit.decorators import ratelimit

from shortener.forms import UrlCreateForm
from shortener.models import ShortenedUrls, Statistic
from shortener.utils import url_count_changer


# @ratelimit: 요청 속도를 제한, 사용자가 애플리케이션에 과도한 요청을 보내는 것을 방지 = 어뷰징(abusing) 방지
# 어뷰징: 애플리케이션에 과도한 요청을 보내는 등 서비스를 악용하는 행위 (서버 리소스 낭비 -> 서비스 성능 저하)
# key: 요청을 식별하는 기준, ip 주소 또는 사용자의 식별자 등이 사용
# rate: 허용된 요청 속도를 나타내는 문자열
# 3/m: 1분에 3번
# 10/s: 1초에 10번
@ratelimit(key='ip', rate='3/m') 
def url_redirect(request, prefix, url):  # request는 이 함수에서 쓰이지 않음
    # print(prefix, url)
    was_limited = getattr(request, 'limited', False)
    
    if was_limited:
        return redirect('index')

    get_url = get_object_or_404(ShortenedUrls, prefix=prefix, shortened_url=url)
    is_permanent = False  # 302: 임시 리다이렉트 (검색엔진에 안잡힘)
    target = get_url.target_url
    print('get_url.creator.organization:', get_url.creator.organization)
    if get_url.creator.organization:
        is_permanent = True  # 301: 검색엔진에 잡히는 리다이렉트
    if not target.startswith('https://') and not target.startswith('http://'):
        target = 'https://' + get_url.target_url

    custom_params = request.GET.dict() if request.GET.dict() else None
    history = Statistic()
    history.record(request, get_url, custom_params)

    # print(is_permanent)
    return redirect(target, permanent=is_permanent)


# @login_required
def url_list(request):
    # GeoIP2 사용 예제
    # country = GeoIP2().country('google.co.kr')
    # print(country)

    # 통계 사용 예제
    # a = (
    #     Statistic.objects.filter(shortened_url_id=3)
    #     .values('custom_params__email_id')
    #     .annotate(t=Count('custom_params__email_id'))
    # )
    # print(a)

    get_list = ShortenedUrls.objects.order_by('-created_at').all()
    return render(request, 'url_list.html', {'list': get_list})


@login_required
def url_create(request):
    msg = None
    if request.method == 'POST':
        form = UrlCreateForm(request.POST)
        if form.is_valid():
            msg = f'{form.cleaned_data.get("nick_name")} 생성 완료!'
            messages.add_message(request, messages.INFO, msg)
            form.save(request)
            return redirect('url_list')
        else:
            form = UrlCreateForm()
    else:
        form = UrlCreateForm()
    return render(request, 'url_create.html', {'form': form})


@login_required
def url_change(request, action, url_id):
    if request.method == 'POST':
        url_data = ShortenedUrls.objects.filter(id=url_id)
        if url_data.exists():
            if url_data.first().creator_id != request.user.id:
                msg = '자신이 소유하지 않은 URL 입니다.'
            else:
                if action == 'delete':
                    msg = f'{url_data.first().nick_name} 삭제 완료!'
                    try:
                        url_data.delete()
                    except Exception as e:
                        print('url_change Error:', e)
                    else:
                        url_count_changer(request, False)
                    messages.add_message(request, messages.INFO, msg)
                elif action == 'update':
                    msg = f'{url_data.first().nick_name} 수정 완료!'
                    form = UrlCreateForm(request.POST)
                    form.update_form(request, url_id)
                    messages.add_message(request, messages.INFO, msg)
        else:
            mag = '해당 URL 정보를 찾을 수 없습니다.'
    elif request.method == 'GET' and action == 'update':
        url_data = ShortenedUrls.objects.filter(pk=url_id).first()
        form = UrlCreateForm(instance=url_data)
        return render(request, 'url_create.html', {'form': form, 'is_update': True})
    return redirect('url_list')