from django import forms
from post.models import PostComment

class PostCommentForm(forms.ModelForm):
    stars = forms.IntegerField(min_value=1,max_value=5)
    
    class Meta:
        model = PostComment
        fields = ('comment', )