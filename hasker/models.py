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
    best_answer = models.ForeignKey('Answer', default=None, on_delete=models.SET_NULL, null=True)
    answers_count = models.SmallIntegerField(default=0)

    def tag_summary(self):
        return ' '.join(t.tag for t in self.tags.all())

    def count_answers(self):
        self.answers_count = Answer.objects.filter(to_question=self).count()
        self.save()

    def __str__(self):
        return self.title


class Answer(BaseEntryModel):
    to_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_best = models.BooleanField(default=False)
    votes = models.SmallIntegerField(default=0)
    
    def __str__(self):
        ch_lim=15
        short_answer = self.body if len(self.body)<ch_lim else self.body[:ch_lim] +'...'
        return short_answer

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.to_question.count_answers()
        
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.to_question.count_answers()
