from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Post
from .forms import PostForm


@login_required
def post_list(request):
    list_of_objects = Post.published.all().exclude(author=request.user)
    paginator = Paginator(list_of_objects, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'posts/list.html', {'page': page, 'posts': posts, 'section': 'posts'})


@login_required
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'posts/detail.html', {'post': post})


@login_required
def post_create(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Post created')
            return redirect(new_post.get_absolute_url())
    else:
        form = PostForm(data=request.GET)
    return render(request, 'posts/create.html', {'section': 'posts', 'form': form})


@login_required
def users_post_list(request):
    list_of_objects = Post.published.all().filter(author=request.user)
    paginator = Paginator(list_of_objects, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'posts/list.html', {'page': page, 'posts': posts, 'section': 'my posts'})


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                if request.user != post.author:
                    post.users_like.add(request.user)
            else:
                if request.user != post.author:
                    post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})
