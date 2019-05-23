from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Tag(models.Model):
    tag = models.SlugField(unique=True)

    def __str__(self):
        return self.tag


class BaseModel(models.Model):
    created = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, blank=True)
    
    class Meta:
        abstract = True


class Question(BaseModel):
    title = models.CharField(max_length=255)
    body = models.TextField()
    best_answer = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class Answer(BaseModel):
    body = models.TextField()
    to_question = models.ForeignKey('Question', related_name='answers')
    created_by = models.ForeignKey(User, on_delete=SET_NULL, related_name='answers')
    
    def __str__(self):
        return "{}'s answer to {}".format(self.created_by, self.to_question)
