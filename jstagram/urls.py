from django.urls import path, register_converter
# from django.urls import re_path #1,2 모두 같은 방식이지만 2가지 다 알아둘것/ 정규표현식 ver.

from . import views


#정규표현식으로 4자리수 바꾸기 class

class YearConverter:
    regex=r"20\d{2}"

    def to_python(self, value):
        return int(value) #문자형인 입력값을 int형으로
    
    def to_url(self, value):
        return "%04d" % value

register_converter(YearConverter, 'year')


urlpatterns=[
    path('',views.post_list),
    path('<int:pk>/', views.post_detail), #int형이 오면 pk로 바꿔서post_deatail 함수 호출
    path('archives/<year:year>/', views.archives_year),
                   #컨버터 이름, 인자
    # re_path(r'archives/(?P<year>\d+)/', views.archives_year),
    
]