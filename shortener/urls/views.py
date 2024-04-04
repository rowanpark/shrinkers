from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from shortener.forms import UrlCreateForm
from shortener.models import ShortenedUrls
from shortener.utils import url_count_changer


def url_redirect(request, prefix, url):  # request는 이 함수에서 쓰이지 않음
    print(prefix, url)
    get_url = get_object_or_404(ShortenedUrls, prefix=prefix, shortened_url=url)
    is_permanent = False  # 302: 임시 리다이렉트 (검색엔진에 안잡힘)
    target = get_url.target_url
    if get_url.creator.organization:
        is_permanent = True  # 301: 검색엔진에 잡히는 리다이렉트
    if not target.startswith('https://') and not target.startswith('http://'):
        target = 'https://' + get_url.target_url
    return redirect(target, permanent=is_permanent)


@login_required
def url_list(request):
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
                        print(e)
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
        url_date = ShortenedUrls.objects.filter(pk=url_id).first()
        form = UrlCreateForm(instance=url_data)
        return render(request, 'url_create.html', {'form': form, 'is_update': True})
    return redirect('url_list')