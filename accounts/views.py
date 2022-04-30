from urllib import response
from django.contrib.auth import get_user_model, login as auth_login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, UpdateView, CreateView
from accounts.forms import ProfileForm
from accounts.models import Profile
from django.conf import settings


# Create your views here.


User=get_user_model()

#class 기반 뷰로도 구현 가능

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name='accounts/profile.html'


profile=ProfileView.as_view()

# class ProfileUpdateView(UpdateView):
#     model= Profile
#     form_class=ProfileForm


# profile_edit=ProfileUpdateView.as_view()


@login_required
def profile_edit(request):
    try:
        profile=request.user.profile
    except Profile.DoesNotExist:
        profile=None

    if request.method=='POST':
        form=ProfileForm(request.POST, request.FILES, instance=profile) #instance를 지정해야 주소 칸에 기존 주소가 나온다
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect('profile')
    else: 
        form=ProfileForm()
    return render(request,'accounts/profile_form.html',{
        'form':form
    })

class SignupView(CreateView):
    model=User
    form_class=UserCreationForm
    success_url=settings.LOGIN_REDIRECT_URL
    template_name='accounts/signup_form.html'

    def form_valid(self, form):
        response=super().form_valid(form)
        user=self.object
        auth_login(self.request, user)
        return response

signup=SignupView.as_view()

#이 코드에서 logic 추가하고 싶으면 class 기반 뷰로 다뤄줘야함
# signup=CreateView.as_view(
#     model=User,
#     form_class=UserCreationForm,
#     success_url=settings.LOGIN_URL,
#     template_name='accounts/signup_form.html',

# )


