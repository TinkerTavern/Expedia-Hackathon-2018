from django.db import models
from django.utils import timezone


"""Review class for the database table Review.
Contains attributes, reviewText, location, author, upvotes and datePosted"""
class Review(models.Model):
    reviewText = models.TextField()
    location = models.CharField(max_length=50)
    author = models.CharField('Author',max_length=50)
    upvotes = models.IntegerField(default=0)
    datePosted = models.DateField(default=timezone.now)
