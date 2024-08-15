from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from django.urls import reverse
from post.models import Post, PostComment, Author, Category
from django.db.models import Count
from django.contrib import messages
from post.form import PostCommentForm
# Create your views here.

class PostView(View):
    def get(self, request):
      
        posts = Post.objects.filter(is_approved=True).order_by('-created_post')
        
        context = {
            "posts":posts,
            
      
            }
        
        return render(request, "post/list.html", context)
        
    
class PostDetailView(View):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        comment_count = post.postcomment_set.count()
        comments = PostComment.objects.filter(post=post)
        comment_form = PostCommentForm()
        context = {
            'post':post,
            'comment_count':comment_count,
            'comments':comments,
            "comment_form":comment_form
        }
        return render(request, 'post/detail.html', context)
    
class AddCommentView(View):
    def post(self, request, id):
        post = Post.objects.get(id=id)
        comment_form = PostCommentForm(data=request.POST)

        if comment_form.is_valid():
            PostComment.objects.create(
                post=post,
                user = request.user,
                comment = comment_form.cleaned_data['comment'],
                stars = comment_form.cleaned_data['stars'],


            )
            messages.success(request, "You have succesfully save your comment.")
            return redirect(reverse("post:detail", kwargs={"id":post.id}))
        else:
            messages.success(request, "Comment qo'sholmadi")

        return render(request, "post/detail.html", {"post":post, 'comment_form':comment_form})

    
class PostCategoryView(View):
    def get(self, request, id):
        category_page = get_object_or_404(Category, id=id)
        posts = Post.objects.filter(category=category_page, is_approved=True).order_by('-created_post')
        
        context = {
            "category_page":category_page,
            "posts":posts
        }
        
        return render(request, "post/category.html", context)
        