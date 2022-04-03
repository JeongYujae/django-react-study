from distutils.command.upload import upload
from tabnanny import verbose
from turtle import title, update
from django.db import models

# Create your models here.

# models.py를 수정한 후에는 python manage.py makemigrations jstagram,
#python manage.py migrate jstagram 해줘야 서버에 반영됨


class Post(models.Model):
    message=models.TextField()
    photo=models.ImageField(blank=True, upload_to='jstagram/post/%Y/%m/%d') #db에 photo를 만듦/ upload_to에 문자열, 함수 가능
    is_public=models.BooleanField(default=False, verbose_name='공개 여부')
    created_at=models.DateTimeField(auto_now_add=True) #자동으로 입력되는 부분 auton_now
    updated_at=models.DateTimeField(auto_now=True)

    #문자열 표현이 필요할 때
    def __str__(self):
        # return f" Custom Post object ({self.id})"
        return self.message
    

    class Meta:
        ordering=['-id']