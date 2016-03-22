from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import pre_save  # right before model to save, gonna do smthng
from django.utils.text import slugify
import unidecode


def upload_location(instance, filename):
    return '%s/%s' % (instance.id, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field='width_field',
                              height_field='height_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    def get_abs_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})
    # class Meta:
    #     ordering = ['-added', '-updated']


def create_slug(instance, new_slug=None):
    try:
        x=(instance.title.encode('ascii'))
    except UnicodeEncodeError:
        x=unidecode.unidecode(instance.title)
    else:
        x= instance.title

    slug = slugify(x)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug =create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)