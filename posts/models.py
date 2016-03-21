from django.db import models
from django.core.urlresolvers import reverse

def upload_location(instance, filename):
    return '%s/%s' %(instance.id, filename)
class Post(models.Model):
    title = models.CharField(max_length=140)
    image = models.ImageField(upload_to=upload_location,
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
        return reverse('posts:detail', kwargs={'id': self.id})
    # class Meta:
    #     ordering = ['-added', '-updated']