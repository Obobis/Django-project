import uuid
from datetime import timezone
from venv import logger

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from future.backports.datetime import datetime

from .forms import ReplyForm, PostForm, ReplyFormLogin, EditPostForm
from .models import Post, Reply
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from taggit.models import Tag

def post_list(request, tag_slug=None):
    object_list = Post.objects.filter(status = 'published')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # если номер страницы не целое число, показываем первую страницу
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # если страница выходит за пределы, показываем последнюю

    return render(request, 'posts/post/list.html', {
        'page': page,
        'posts': posts,
        'tag': tag
    })




def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
                             status = 'published',
                             publish__year = year,
                             publish__month = month,
                             publish__day = day)
    #reply_list
    replies = post.replies.filter(active = True)
    if request.method == 'POST':
        if request.user.is_authenticated:  # Авторизованный пользователь
            reply_form = ReplyFormLogin(data=request.POST)
            if reply_form.is_valid():
                new_reply = reply_form.save(commit=False)
                new_reply.name = request.user.username
                new_reply.email = request.user.email
                new_reply.post = post
                new_reply.save()
        else:  # Гость
            reply_form = ReplyForm(data=request.POST)
            if reply_form.is_valid():
                new_reply = reply_form.save(commit=False)
                new_reply.post = post
                new_reply.save()
    else:
        if request.user.is_authenticated:
            reply_form = ReplyFormLogin()
        else:
            reply_form = ReplyForm()
    return render(request, 'posts/post/details.html', {'post':post,
                                                                           'replies':replies,
                                                                           'reply_form': reply_form})
#create
@login_required
def post_create(request):
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.status = 'published'
            new_post.slug = slugify(new_post.title)
            new_post.save()
            post_form.save_m2m()

            return redirect(new_post.get_absolute_url())

    else:
        post_form = PostForm
    return render(request, 'posts/post/create.html', {'post_form':post_form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post_form = PostForm(instance=post)
        if post_form.is_valid():
            edit_post = post_form.save(commit=False)
            edit_post.slug = slugify(edit_post.title)
            edit_post.save()
            post_form.save_m2m()
            return redirect(edit_post.get_absolute_url())
    else:
        post_form = PostForm(instance=post)
    return render(request, 'posts/post/edit.html', {'post_form': post_form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user, )
    if request.method == 'POST':
        post.delete()
        return render(request, 'posts/post/delete.html')
    return redirect(request. post.get_absolute_url)

@login_required
def reply_delete(request, pk):
    reply = get_object_or_404(Reply, pk=pk, name=request.user.username)
    if request.method == 'POST':
        reply.delete()
        return render(request, f'posts/post/reply_delete.html')
    return redirect(request.reply.post.get_absolute_url)



class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post/detail.html'
    context_object_name = 'post'

class PostListView(ListView):
    queryset = Post.objects.filter(status = 'published')
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'posts/post/list.html'
