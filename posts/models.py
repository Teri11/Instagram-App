from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.dispatch import receiver
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField

# Create your models here.

class Post(models.Model):
    image = CloudinaryField('image')
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image_caption = models.TextField()

    def save_post(self):
     self.save()

    @classmethod
    def get_posts(cls):
        posts = cls.objects.all()
        return posts

    @property
    def added_comments(self):
        return self.comments.all()

    @property
    def added_like(self):
        return self.postlikes.count()

    @classmethod
    def search_users(cls,search_term):
        posts = cls.objects.filter(name__icontains = search_term).all()
        return posts

    def delete_post(self):
        self.delete()

    def __str__(self):
        return "%s post" % self.posts_name


class Profile(models.Model):
  picture = CloudinaryField('image',default='v1638348565/owuk4syvculcljuzdron.jpg')
  bio = models.TextField()
  user = models.OneToOneField(User,on_delete = models.CASCADE)

  @receiver(post_save , sender = User)
  def create_profile(instance,sender,created,**kwargs):
    if created:
      Profile.objects.create(user = instance)

  @receiver(post_save,sender = User)
  def save_profile(sender,instance,**kwargs):
    instance.profile.save()


  @classmethod
  def search_profiles(cls,search_term):
    profiles = cls.objects.filter(user__username__icontains = search_term).all()
    return profiles

  def __str__(self):
    return "%s profile" % self.user

class Comment(models.Model):
  comment = models.TextField()
  post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name='comments')
  user = models.ForeignKey(User,on_delete = models.CASCADE,related_name='comments')

  @classmethod
  def show_comments(cls,post_id):
    comments = cls.objects.filter(post_id = post_id)
    return comments

  def __str__(self):
    return "%s comment" % self.post

class Like(models.Model):
  post =models.ForeignKey(Post, on_delete = models.CASCADE,related_name='postlikes')
  liker=models.ForeignKey(User,on_delete = models.CASCADE,related_name='userlikes')

  def __str__(self):
    return "%s like" % self.post