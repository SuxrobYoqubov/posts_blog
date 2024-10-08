from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from django.urls import reverse
from post.models import Post, PostComment, Category, Author
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator
from post.form import PostCommentForm, PostCreateForm, MessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class PostView(View):
    def get(self, request):
      
        posts = Post.objects.filter(is_approved=True).order_by('-created_post')
        
        # kitoblarni 2 tadan bo'lib chiqarib beradi
        page_size = request.GET.get("page_size", 5)
        paginator = Paginator(posts, page_size)
        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)
        context = {
            
            "page_obj":page_obj
      
            }
        
        return render(request, "post/list.html", context)
        
    
class PostDetailView(View):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.view_count += 1
        post.save()
        comment_count = post.postcomment_set.count()
        comments = post.postcomment_set.all()
        comment_form = PostCommentForm()
        context = {
            'post':post,
            'comment_count':comment_count,
            'comments':comments,
            "comment_form":comment_form
        }
        return render(request, 'post/detail.html', context)
    
class AddCommentView(LoginRequiredMixin, View):
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
        # kitoblarni 2 tadan bo'lib chiqarib beradi
        page_size = request.GET.get("page_size", 5)
        paginator = Paginator(posts, page_size)
        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)
        context = {
            "category_page":category_page,
            "page_obj":page_obj
        }
        
        return render(request, "post/category.html", context)
    
class PostCreateView(LoginRequiredMixin, View):
    def get(self, request):
        create_form = PostCreateForm()
        context = {
            'form':create_form
        }
        return render(request, "post/post_create.html", context)  
    
    def post(self, request):
        create_form = PostCreateForm(data=request.POST)
        if create_form.is_valid():
            post = create_form.save(commit=False)
            try:
                # Foydalanuvchi uchun Author obyektini olish
                author = Author.objects.get(user=request.user)
                post.author = author  # Author obyektini post muallifi sifatida belgilash
                post.save()
                return redirect('post:list')  # Post yaratgandan keyin qaysi sahifaga o'tishni belgilash
            except Author.DoesNotExist:
                create_form.add_error(None, "Siz uchun Author yozuvi topilmadi.")
        else:
            return render(request, 'users/post_create.html', {'form': create_form})
        
class MessageView(View):
    def get(self, request):
        message_form = MessageForm()
        context = {
            "form":message_form
        }
        return render(request, "post/message.html", context)
    
    def post(self, request):
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            message_form.save()
            return redirect('post:list')  # Post yaratgandan keyin qaysi sahifaga o'tishni belgilash
        else:
            return render(request, 'post/message.html', {'form': message_form})