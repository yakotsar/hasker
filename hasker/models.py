from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


class Tag(models.Model):
    tag = models.SlugField(unique=True)

    def __str__(self):
        return self.tag


# https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.SET
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class BaseEntryModel(models.Model):
    created = models.DateTimeField(default=timezone.now)
    body = models.TextField()
    author = models.ForeignKey(
            get_user_model(),
            on_delete=models.SET(get_sentinel_user),
            default=None,
    )
    class Meta:
        abstract = True
        

class Question(BaseEntryModel):
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255)
    best_answer = models.ForeignKey('Answer', on_delete=models.SET_NULL, null=True)

    # wtf 'name 'Answer' is not defined'
    #best_answer = models.ForeignKey(Answer, on_delete=SET_NULL, related_name='question')

    def __str__(self):
        return self.title


class Answer(BaseEntryModel):
    to_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_best = models.BooleanField(default=False)
    votes = models.SmallIntegerField(default=0)
    
    def __str__(self):
        return "{}'s answer to {}".format(self.author, self.to_question)
