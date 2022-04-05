from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Comment,Post
from django.contrib.auth.models import User

class postForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['image','name','image_caption']

class MakeCommentForm(forms.ModelForm):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.fields['comment'].widget=forms.TextInput()
    self.fields['comment'].widget.attrs['placeholder']='Make a comment...'
  class Meta:
    model = Comment
    fields = ('comment',)

class UpdateUser(forms.ModelForm):
  email = forms.EmailField()
  class Meta:
    model = User
    fields = ['username','email']
    
class Registration(UserCreationForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username','email','password1','password2']

class UpdateProfile(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['picture','bio']



