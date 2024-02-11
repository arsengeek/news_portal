from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Author(models.Model):
    """
        This class is realizate User-Select - rating and name    
    """
    
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    rating = models.IntegerField(default=0)
    
    def update_rating(self):
        full_rating = 0
        full_coments_rating = 0
        full_post_rating = 0
    
        post = Post.objects.filter(author=self)
        for pos in post:
            full_rating += pos.raiting_post
            
        comments = Comment.objects.filter(user_comment=self.user)
        for com in comments:
            full_coments_rating += com.rating_comment
            
        posts_comment = Comment.objects.filter(post_comment__author=self)
        for pos_com in posts_comment:
            full_post_rating += pos_com.rating_comment
            
        print(full_rating)
        print(full_coments_rating)
        print(full_post_rating)    
        
        
        self.rating = full_coments_rating + full_post_rating + full_rating * 3
        self.save()
            
            
class Catigory(models.Model):
    """
        subjects for news/post, this class is stores sub
    """
    category = models.CharField(max_length=50, unique=True)
    
    def __str__(self) -> str:
        return self.category
    
    
class Post(models.Model):
    """
        This model should contain articles and news that are created by users. Each object can have one or more categories
    """
    
    title = models.CharField(max_length=50)
    text_post = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content_post = models.ForeignKey(to='Catigory',related_name='post_category', on_delete=models.CASCADE)
    time_post = models.DateTimeField(auto_now_add=True)
    raiting_post = models.IntegerField(default=0)
    
    #preview text
    def preview(self):
        text_preview = self.text_post[:124]
        
        if len(self.text_post) > 124:
            text_preview += '...'

        return text_preview
    
        #this method  rating post on the one point
    def like(self):
        self.raiting_post += 1
        self.save()
    
    #this method reduces rating post on the one point
    def dislike(self):  
        self.raiting_post -= 1
        self.save()
        
    def best_post(self):
        post_ratings = list(Post.objects.filter(author=self).order_by('-raiting_post').values_list('title', Post.preview()))
    
        print(post_ratings[0])
        
        
    def __str__(self):
        return self.title
        
class PostCatigory(models.Model):
    """
        Connecting to models Post and Catigory
    """
    conect_catigory = models.ForeignKey(Catigory,on_delete=models.CASCADE)
    conect_post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    """
        Comment in post, user can writes text under post
    """
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField(max_length=100)
    data_time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)
    
    #this method  rating comment on the one point
    def like(self):
        self.rating_comment += 1
        self.save()
        
    #this method reduces rating comment on the one point
    def dislike(self):
        self.rating_comment -=1
        self.save()
        
        
class Best_rating_user(models.Model):
    
    def print_best_users(self):
        user_ratings = list(Author.objects.all().order_by('-rating').values_list('user__username', 'rating'))
    
        print(user_ratings[0])
    
