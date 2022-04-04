from django.contrib import admin
from .models import Post, Comment, Tag
from django.utils.safestring import mark_safe
# Register your models here.

@admin.register(Post) #Wrapping
class PostAdmin(admin.ModelAdmin):
    list_display=['id','photo_tag','message','message_length','is_public','created_at','updated_at'] #필드 이름은 pk
    list_display_links=['message'] #인자, 함수도 가능
    list_filter=['created_at', 'is_public']
    search_fields=['message'] #검색창 만들기

    def message_length(self,post):
        return len(post.message)

    
    def photo_tag(self,post):
        if post.photo:
            return mark_safe(f'<img src="{post.photo.url}" style="width:72px;"/>') #이미지 주소가 나오기보다, 안전하다는 태그로 사진이 직접적으로 나옴

        else:
            return None

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

