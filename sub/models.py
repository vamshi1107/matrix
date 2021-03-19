from django.db import models

# Create your models here.
class post(models.Model):
        user=models.CharField(max_length=100)
        caption=models.CharField(max_length=300)
        content=models.CharField(max_length=2000)
        type=models.CharField(max_length=20)

        def __str__(self):
               return self.user

class member(models.Model):
        name=models.CharField(max_length=100)
        username=models.CharField(max_length=100)
        password=models.CharField(max_length=30)
        email=models.CharField(max_length=200)

        def __str__(self):
                return self.name

class relation(models.Model):
        user1=models.CharField(max_length=100)
        user2=models.CharField(max_length=100)

        def __str__(self):
                return self.user1+"  "+self.user2

class request(models.Model):
        From=models.CharField(max_length=100)
        To=models.CharField(max_length=100)

        def __str__(self):
                return self.From +" "+self.To

class displaypic(models.Model):
    user=models.CharField(max_length=100)
    content = models.CharField(max_length=1500)

    def __str__(self):
        return self.user

class comment(models.Model):
    user=models.CharField(max_length=100)
    content = models.CharField(max_length=1500)
    postid=models.CharField(max_length=5000)
    def __str__(self):
        return self.postid


