
# запись в куки количества посещений главной страницы в одном сеансе (после закрытия браузера, cnt обнуляется)
def get_visit_in_cookies(request):
    if 'cnt' in request.COOKIES:
        cnt = int(request.COOKIES.get('cnt')) + 1
    else:
        cnt = request.COOKIES.setdefault('cnt', 1)

    return cnt