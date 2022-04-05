from .models import Post,Profile,Like
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect, get_object_or_404
from django.http import Http404,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import Registration,UpdateUser,UpdateProfile,MakeCommentForm,postForm
from django.contrib.auth.decorators import login_required


def register(request):
  if request.method == 'POST':
    form = Registration(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')

      messages.success(request,f'Account for {username} created,you can now login')
      return redirect('login')
  else:
    form = Registration()

  return render(request,'registration/registration_form.html',{"form":form})

@login_required
def profile(request):
  add_comment = MakeCommentForm()
  current_user = request.user
  posts = Post.objects.all()
  users = User.objects.all()
  user_posts = Post.objects.filter(user_id = current_user.id).all()
  
  return render(request,'profile/profile.html',{"posts":posts,'users':users,'add_comment':add_comment,'user_posts':user_posts,"current_user":current_user})

@login_required
def add_post(request):
  if request.method == 'POST':
    post_form = postForm(request.POST,request.FILES) 
    if post_form.is_valid():
      post = post_form.save(commit = False)
      post.user = request.user
      post.save()
      return redirect('profile')

  else:
    post_form = postForm()
  return render(request,'add_post.html',{"post_form":post_form})

def post_details(request,post_id):
  current_user = request.user
  try:
    post = get_object_or_404(Post, pk = post_id)
  except ObjectDoesNotExist:
    raise Http404()
  return render(request, 'details.html', {'post':post,'current_user':current_user})


@login_required
def search_users(request):
  if 'search_user' in request.GET and request.GET["search_user"]:
    search_term = request.GET.get('search_user')
    users = Profile.search_profiles(search_term)
    posts = Post.search_users(search_term)
    return render(request,'search.html',{"users":users,"posts":posts})
  else:
    return render(request,'search.html')

@login_required
def posts_profile(request,pk):
  add_comment = MakeCommentForm()
  user = User.objects.get(pk = pk)
  posts = Post.objects.filter(user = user)
  current_user = request.user
  
  return render(request,'profile/posts_profile.html',{"user":user,'add_comment':add_comment,
"posts":posts,"current_user":current_user})

@login_required
def update_profile(request):
  if request.method == 'POST':
    user_form = UpdateUser(request.POST,instance=request.user)
    profile_form = UpdateProfile(request.POST,request.FILES,instance=request.user.profile)
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('profile')
  else:
    user_form = UpdateUser(instance=request.user)
    profile_form = UpdateProfile(instance=request.user.profile) 
  params = {
    'user_form':user_form,
    'profile_form':profile_form
  }
  return render(request,'profile/update_user.html',params)

@login_required
def comment(request,post_id):
  comment_form = MakeCommentForm()
  post = Post.objects.filter(pk = post_id).first()
  if request.method == 'POST':
    comment_form = MakeCommentForm(request.POST)
    if comment_form.is_valid():
      comment = comment_form.save(commit = False)
      comment.user = request.user
      comment.post = post
      comment.save() 
  return redirect('profile')

def likes(request, post_id):
    current_user = request.user
    post=Post.objects.get(id=post_id)
    new_like,created= Like.objects.get_or_create(liker=current_user, post=post)
    new_like.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def delete(request,post_id):
  current_user = request.user
  post = Post.objects.get(pk=post_id)
  if post:
    post.delete_post()
  return redirect('profile')

