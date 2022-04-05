from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
# Create your views here.


# post_list= ListView.as_view(model=Post) 밑의 함수와 같은 코드/ filter 코드 제외 모든 코드와 똑같이 구현 가능

def post_list(request):
    qs=Post.objects.all() #모든 object 다 가져옴
    q= request.GET.get('q','') #q가 없을 때, 공백 값 반환함
    if q:
        qs=qs.filter(message__icontains=q)
    #jstagram/templates/jstagram/post_list.html/ render -> html 태그를 만들어주는 역할
    return render(request,'jstagram/post_list.html',{ 
            'post_list':qs, #이 이름이 경로 밑에 있는 이름과 같아야함
        })

def post_detail(request,pk):
    # response=HttpResponse()s
    # response.write('Hello')
    pass

def archives_year(request, year):
    return HttpResponse(f"{year}년 archives") #html에 보여지는 text
    