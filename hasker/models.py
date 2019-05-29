from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models

# https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.FileField.upload_to
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Profile(User):
    avatar = models.FileField(upload_to=user_directory_path)


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
            settings.AUTH_USER_MODEL,
            on_delete=models.SET(get_sentinel_user),
            default=None,
    )
    class Meta:
        abstract = True
        

class Question(BaseEntryModel):
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255)
    # name 'Answer' is not defined
    #best_answer = models.ForeignKey(Answer, on_delete=SET_NULL, related_name='question')

    def __str__(self):
        return self.title


class Answer(BaseEntryModel):
    to_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_best = models.BooleanField(default=False)
    votes = models.SmallIntegerField(default=0)
    
    def __str__(self):
        return "{}'s answer to {}".format(self.created_by, self.to_question)
