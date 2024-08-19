from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from users.forms import UserCreateForm, ProfileEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from post.models import Post, PostComment, Category, Author
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        return render(request, 'users/register.html', {'form': create_form})

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            user = create_form.save()
            login(request, user)
            return redirect('post:list')
        else:
            return render(request, 'users/register.html', {'form': create_form})

class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'users/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            if user is not None:            
                login(request, user)
                return redirect('post:list')
            else:
                return redirect('post:login')
        else:
            return render(request, 'users/login.html', {'login_form': login_form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("post:list")
    
class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        is_admin = user.is_staff
        author_profile, created = Author.objects.get_or_create(user=user)
        
        if author_profile:
            posts = Post.objects.filter(author=author_profile)
            posts_true = Post.objects.filter(author=author_profile, is_approved=True)
            post_count = posts.count()
            post_count_true = posts_true.count()
        else:
            post_count = 0
        context = {
            "user_profile":author_profile,
            "is_admin":is_admin,
            "post_count":post_count,
            "post_count_true":post_count_true,
            "posts_true":posts_true
        }
        return render(request, 'users/profile.html', context) 

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        # Kirgan foydalanuvchiga tegishli Author obyektini olish
        author = get_object_or_404(Author, user=request.user)
        # Formani yaratishda `user`ni ham berish
        profile_edit_form = ProfileEditForm(instance=author, user=request.user)
        context = {
            "form": profile_edit_form,
        }
        return render(request, 'users/profile_edit.html', context)

    def post(self, request):
        # Kirgan foydalanuvchiga tegishli Author obyektini olish
        author = get_object_or_404(Author, user=request.user)
        # Formani yaratishda `user`ni ham berish
        profile_update_form = ProfileEditForm(
            instance=author,
            data=request.POST,
            files=request.FILES,
            user=request.user
        )
        if profile_update_form.is_valid():
            profile_update_form.save()
            return redirect("users:profile")
        return render(request, "users/profile_edit.html", {"form": profile_update_form})
    

class ProfilePostsView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        user = request.user
        author_profile=Author.objects.get(user=user)
        
        if author_profile:
            posts_true = Post.objects.filter(author=author_profile, is_approved=True)
        else:
            return redirect('post:list')
        context = {
            "posts_true":posts_true
        }
        return render(request, 'post/user_posts.html', context)         