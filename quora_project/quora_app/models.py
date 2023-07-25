from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='liked_answers',blank=True)
    dislikes = models.ManyToManyField(User,related_name='disliked_answers',blank=True)

    def likes_count(self):
        return self.likes.count()

    def dislikes_count(self):
        return self.dislikes.count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)


class QuestionCategory(models.Model):
    category = models.CharField(default="", max_length=100)

    def __str__(self):
        return self.category
        
    class Meta:
        verbose_name = 'Question Category'
        verbose_name_plural = 'Question Categories'