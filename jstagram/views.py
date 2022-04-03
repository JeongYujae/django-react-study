from email import message
from django.shortcuts import render
from .models import Post
# Create your views here.

def post_list(request):
    qs=Post.objects.all() #모든 object 다 가져옴
    q= request.GET.get('q','') #q가 없을 때, 공백 값 반환함
    if q:
        qs=qs.filter(message__icontains=q)
    #jstagram/templates/jstagram/post_list.html/ render -> html 태그를 만들어주는 역할
    return render(request,'jstagram/post_list.html',{ 
            'post_list':qs, #이 이름이 경로 밑에 있는 이름과 같아야함
        })

    
    