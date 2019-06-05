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
    text = models.TextField()
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
    best_answer = models.ForeignKey('Answer', default=None, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def votes_count(self):
        return sum(answer.votes for answer in self.answers.all())

    def answers_count(self):
        return self.answers.all().count()


class Answer(BaseEntryModel):
    to_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_best = models.BooleanField(default=False)
    votes = models.SmallIntegerField(default=0)
    
    def __str__(self):
        ch_lim=15
        short_answer = self.text if len(self.text)<ch_lim else self.text[:ch_lim] +'...'
        return short_answer
