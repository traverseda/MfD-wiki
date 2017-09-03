from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
import mistune # bbcode
import reversion

User = settings.AUTH_USER_MODEL

import taggit
reversion.register(taggit.models.Tag)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    long_name = models.TextField(max_length=500, default="",blank=True)
    bio = models.TextField(max_length=500, default="",blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

renderer = mistune.Renderer(escape=True)
markdown = mistune.Markdown(renderer=renderer)


@reversion.register(exclude=('renderedText',),follow=('tags',))
class Wiki(models.Model):
    name = models.CharField(max_length=400, unique=True)
    bodyText = models.TextField(default="This page doesn't have any content yet.",blank=True)
    renderedText = models.TextField(default="",blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified =  models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
   
    def save(self, *args, **kwargs):
#        self.renderedText = bbcode.render_html(self.bodyText)
        self.renderedText = markdown(self.bodyText)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Vote(models.Model):
    plan = models.ForeignKey(Wiki, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    class Meta:
        unique_together = ("plan", "user")
