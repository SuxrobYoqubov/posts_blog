from django.contrib import admin
from post.models import Author, Category,Post,PostComment, Message


class AuthorAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    list_display = ['title',"is_approved", 'author']
    list_filter = ['title', 'body']
    

class PostCommentAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    list_display = ['name',"phone_number", 'message']

admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Message, MessageAdmin)

