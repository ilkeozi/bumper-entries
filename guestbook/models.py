from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)  
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),  
        ]


class Entry(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, db_index=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")

    def __str__(self):
        return f"{self.subject} - {self.user.name}"

    class Meta:
        indexes = [
            models.Index(fields=['created_date']),  
            models.Index(fields=['user', 'created_date']),  
        ]
