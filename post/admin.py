from django.contrib import admin
from post.models import Author, Category,Post,PostComment


class AuthorAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    list_filter = ['title', 'body']
    

class PostCommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)

