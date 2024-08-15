
from post.models import Post, PostComment, Author, Category
from django.db.models import Count
# Create your views here.


def base_page(request):
        # Postlar ro'yxatidan eng so'nggi 3 tasini olish
        three_posts = Post.objects.filter(is_approved=True).order_by('-created_post')[:3]
        top_three_posts = Post.objects.filter(is_approved=True).order_by('-view_count')[:3]
        posts = Post.objects.filter(is_approved=True)
        three_comments = PostComment.objects.order_by('-created_comment')[:3]
        # category = Category.objects.all()
        category = Category.objects.all().annotate(count=Count('post'))
        users = Author.objects.all()
        context = {
            "posts":posts,
            "three_comments":three_comments, 
            "users":users,
            "category":category,
            "three_posts":three_posts,
            'latest_post': posts[0] if len(three_posts) > 0 else None,
            'second_latest_post': posts[1] if len(three_posts) > 1 else None,
            'third_latest_post': posts[2] if len(three_posts) > 2 else None,
            "top_three_posts":top_three_posts,
            }
    
        return context