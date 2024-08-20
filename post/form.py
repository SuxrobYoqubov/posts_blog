from django import forms
from post.models import PostComment, Post, Message

class PostCommentForm(forms.ModelForm):
    stars = forms.IntegerField(min_value=1,max_value=5)
    
    class Meta:
        model = PostComment
        fields = ('comment', )
        
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'body', 'image', )
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'phone_number', 'message', )