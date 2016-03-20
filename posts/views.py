from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm


def post_create(request):
    form = PostForm(request.POST or None)  # None - not to show 'required' stuff on htmlpage
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Created')
        return HttpResponseRedirect(instance.get_abs_url())
    else:
        messages.error(request, 'Error')

    context = {
        'form': form,
    }
    return render(request, "posts/post_form.html", context)


def post_detail(request, id):
    instance = get_object_or_404(Post, id=id)
    context = {
        "instance": instance
    }
    return render(request, "posts/post_detail.html", context)


def post_list(request):
    queryset = Post.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "posts/index.html", context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Saved')
        return HttpResponseRedirect(instance.get_abs_url())
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, "posts/post_form.html", context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Successfully Deleted')
    return redirect('posts:list')
