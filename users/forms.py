from django import forms
from django.contrib.auth.models import User
from post.models import Author


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User    
        fields = ('username', 'first_name', 'last_name',
                   'email', 'password')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
     
    class Meta:
        model = Author
        fields = ('first_name', "last_name", "email", "bio", "phone_number",
                  "profile_picture", "address")
          
        # __init__ metodida userni qabul qilish:
# ProfileEditForm formasi yaratilayotganda, 
# foydalanuvchining joriy first_name, last_name, 
# va email qiymatlari formaning boshlang'ich qiymatlari sifatida o'rnatiladi.

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # `user`ni olish
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        if user:
            # Foydalanuvchining mavjud ma'lumotlarini forma boshlang'ich qiymatlari sifatida o'rnating
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        instance = super().save(commit=False)
        user = instance.user  # Author modelining `user` maydonini olish

        # cleaned_data orqali mavjud qiymatlarni yangilang
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        user.email = self.cleaned_data.get('email', user.email)

        if commit:
            user.save()  # Foydalanuvchini saqlash
            instance.save()  # Author instansiyasini saqlash
        return instance