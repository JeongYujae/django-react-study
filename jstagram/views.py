from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView
from .models import Post
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PostForm
from django.contrib import messages
# Create your views here.


#한페이지에 10개씩 나오게 만드는 코드
# post_list= login_required(ListView.as_view(model=Post, paginate_by=10)) #밑의 함수와 같은 코드/ filter 코드 제외 모든 코드와 똑같이 구현 가능

@login_required
def post_list(request):
    qs=Post.objects.all() #모든 object 다 가져옴
    q= request.GET.get('q','') #q가 없을 때, 공백 값 반환함
    if q:
        qs=qs.filter(message__icontains=q)
    #jstagram/templates/jstagram/post_list.html/ render -> html 태그를 만들어주는 역할

    messages.info(request,'test') #등록만 한 코드 -> 소비하는 코드 작성해줘야함

    return render(request,'jstagram/post_list.html',{ 
            'post_list':qs, })
            #이 이름이 경로 밑에 있는 이름과 같아야함


#로그인 달린 기능 만들기/ 위와 코드 같지만 더 자주 쓰이는 코드

@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    model=Post
    paginate_by=10

post_list=PostListView.as_view()

        

# def post_detail(request,pk: int):
#     # try:
#     #     post=Post.objects.get(pk=pk)#앞 pk는 변수, 뒤 pk는 입력된 인자/ DoesNotExist 예외 발생 가능
#     # except Post.DoesNotExist:
#     #     raise Http404
#     post=get_object_or_404(Post,pk=pk) #위의 동작 줄여주는 기능

#     return render(request, 'jstagram/post_detail.html',{
#         'post': post, #templates에 html 파일을 만들어주자
#     })

post_detail= DetailView.as_view(
        model=Post,
        queryset=Post.objects.filter(is_public=True)) #import 해서 쓰기/ 위와 동일한 코드
        #공개된 포스팅만 공개되는 코드

class PostDetailView(DetailView):
    model=Post

    #로그인이 안된 유저는 public 공개된 post만 볼 수 있게
    def get_queryset(self):
        qs=super().get_queryset()
        if not self.request.user.is_authenticated:
            qs=qs.filter(is_public=True)
        return qs


@login_required
def post_new(request):
    if request.method=='POST':
        form=PostForm(request.POST, request.FILES)
        if form.is_valid(): 
            post=form.save(commit=False)
            post.author=request.user #현재 로그인된 유저 정보
            post.save() #save 하려면 무조건 login된 상황이어야만 함
            messages.success(request, '작성 완료!')

            return redirect(post)
    else:
        form=PostForm() 

    return render(request, 'jstagram/post_form.html',{
        'form':form,
        'post':None,
    })

#폼 기반 뷰로 봤을 떄 같은 코드

# class PostCreateView(LoginRequiredMixin, CreateView):
#     model= Post
#     form_class= PostForm
#     def form_valid(self, form):
#         self.object=form.save(commit=False)
#         self.object.author=self.request.user
#          messages.success(request, '작성 완료!')
#         return super().from_valid(form)



@login_required
def post_edit(request, pk):
    post=get_object_or_404(Post, pk=pk)

    if post.author !=request.user:
        messages.error(request, '작성만 수정 가능')
        
    

    if request.method=='POST':
        form=PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post=form.save()
            messages.success(request, '수정 완료!')
            return redirect(post)
    else:
        form=PostForm(instance=post) 

    return render(request, 'jstagram/post_form.html',{
        'form':form,
        'post':post,
    })

#폼 기반 뷰로 봤을 떄 같은 코드
# class PostUpdateView(UpdateView):
#     model=Post
#     form_class= PostForm

#     def form_valid(self, form):
#         messages.success(self.reqeust, '수정 완료!')
#         return super().form_valid(form)


@login_required
def post_delete(request, pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, '포스팅 삭제완료!')
        return redirect('jstagram:post_list')
    return render(request, 'jstagram/post_confirm_delete.html',{
        'post':post,
    })

#폼 기반 뷰로 봤을 떄 같은 코드

# class PostDeleteView(loginRequiredMixin, DeleteView):
#     model=Post
#     success_url=reverse_lazy('jstagram:post_list')



# def archives_year(request, year):s
#     return HttpResponse(f"{year}년 archives") #html에 보여지는 text

#archives view를 통해 위의 함수 대체 가능. -> urls에 있는 path도 같이 손봐줘야 하는 구조

post_archive=ArchiveIndexView.as_view(model=Post, date_field='created_at')

post_archive_year=YearArchiveView.as_view(model=Post, date_field='created_at', make_object_list=True)