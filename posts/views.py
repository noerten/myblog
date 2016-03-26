from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.models import Comment
from .models import Post
from .forms import PostForm


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # if not request.user.is_authenticated():
    #     raise Http404
    form = PostForm(request.POST or None, request.FILES or None)  # None - not to show 'required' stuff on htmlpage
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        instance.user = request.user
        messages.success(request, 'Successfully Created')
        return HttpResponseRedirect(instance.get_abs_url())

    context = {
        'form': form,
    }
    return render(request, "posts/post_form.html", context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    content_type = ContentType.objects.get_for_model(Post)
    obj_id = instance.id
    comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
    context = {
        "instance": instance,
        'comments': comments,
    }
    return render(request, "posts/post_detail.html", context)


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()  # function defined in model
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all().order_by('-id')
    query=request.GET.get('q')
    if query:
        queryset_list=queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
            ).distinct() #no duplicates
    paginator = Paginator(queryset_list, 5)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "today": today,
    }
    return render(request, "posts/post_list.html", context)


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
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


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, 'Successfully Deleted')
    return redirect('posts:list')
