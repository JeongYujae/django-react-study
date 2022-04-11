from unicodedata import name
from django.urls import path, register_converter
# from django.urls import re_path #1,2 모두 같은 방식이지만 2가지 다 알아둘것/ 정규표현식 ver.

from . import views
 
app_name='jstagram' #url reverse에서 namespace 역할을 하게 됨


#정규표현식으로 4자리수 바꾸기 class

class YearConverter:
    regex=r"20\d{2}"

    def to_python(self, value):
        return int(value) #문자형인 입력값을 int형으로
    
    def to_url(self, value):
        return "%04d" % value

class MonthConverter(YearConverter): #Year Converter를 상속받기
    regex=r"d{1,2}"

class DayConverter(YearConverter): #Year Converter를 상속받기
    regex=r"[0123]\d"

register_converter(YearConverter, 'year')
register_converter(MonthConverter, 'month')
register_converter(DayConverter, 'day')




urlpatterns=[
    path('',views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'), #int형이 오면 pk로 바꿔서post_deatail 함수 호출
    # path('archives/<year:year>/', views.archives_year),
    #                #컨버터 이름, 인자
    # re_path(r'archives/(?P<year>\d+)/', views.archives_year),

    path('archive/',views.post_archive, name='post_archive'),
    path('archive/<year:year>/', views.post_archive_year, name='post_year_archive')

    
]