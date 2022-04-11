from unicodedata import name
from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.

# models.py를 수정한 후에는 python manage.py makemigrations jstagram,
#python manage.py migrate jstagram 해줘야 서버에 반영됨


class Post(models.Model):
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message=models.TextField()
    photo=models.ImageField(blank=True, upload_to='jstagram/post/%Y/%m/%d') #db에 photo를 만듦/ upload_to에 문자열, 함수 가능
    is_public=models.BooleanField(default=False, verbose_name='공개 여부')
    created_at=models.DateTimeField(auto_now_add=True) #자동으로 입력되는 부분 auton_now
    updated_at=models.DateTimeField(auto_now=True)

    #문자열 표현이 필요할 때
    def __str__(self):
        # return f" Custom Post object ({self.id})"
        return self.message
    
    def get_absolute_url(self):
        return reverse('jstagram:post_detail', args=[self.pk])

        
    

    class Meta:
        ordering=['-id']


class Comment(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE, limit_choices_to={'is_public': True}) #ForeignKey(대상모델, record 삭제 시 다른 모델의 record도 삭제함) 공식 문서, pdf 참조할 것
    #db에 post_id 필드생성
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

class Tag(models.Model):
    name=models.CharField(max_length=50, unique=True)
    post_set=models.ManyToManyField(Post)

    def __str__(self):
        return self.name