from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
from . import forms
from .forms import LoginUserForm, RegisterUserForm
from .models import Post, Comment


def index(request: HttpRequest):
    posts = Post.objects.all()
    for post in posts:
        post.likes_count = post.number_of_likes()
        post.isLiked = post.isLiked(request.user)
    ctx = {
        'posts': posts,
        'user': request.user
    }
    return render(request, 'index.html', ctx)


def PostPage(request: HttpRequest, pk: int):
    post = Post.objects.get(id=pk)
    post.likes_count = post.number_of_likes()
    post.isLiked = post.isLiked(request.user)
    comments = post.comments.all()
    for comment in comments:
        comment.likes_count = comment.number_of_likes()
        comment.isLiked = comment.isLiked(request.user)
    ctx = {
        'post': post,
        'comments': comments,
        'user': request.user
    }
    return render(request, 'post.html', ctx)


def likePost(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    post_id = request.POST.get('id')
    post = Post.objects.get(pk=post_id)
    post.like(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def likeComment(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    post_id = request.POST.get('id')
    comment = Comment.objects.get(pk=post_id)
    comment.like(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def loginPage(request: HttpRequest):
    form = LoginUserForm()
    error = None
    if request.method == "POST" and request.user.is_anonymous:
        user = authenticate(username=request.POST.get('name'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error = "error"

    ctx = {
        'form': form,
        'error': error
    }
    return render(request, 'login.html', ctx)


def registerPage(request: HttpRequest):
    form = RegisterUserForm()
    error = None
    if request.method == "POST" and request.user.is_anonymous:
        try:
            user = User.objects.get(username=request.POST.get('name'))
        except User.DoesNotExist:
            user = None
        if user is not None:
            error = "пользователь с таким именем уже существует"
        else:
            user = User.objects.create_user(username=request.POST.get('name'), password=request.POST.get('password'))
            login(request, user)
            return redirect('/')

    ctx = {
        'form': form,
        'error': error
    }
    return render(request, 'register.html', ctx)


@login_required
def addComment(request: HttpRequest, pk: int):
    text: str = request.POST.get('content')
    text = text.strip()
    if text != "":
        post = Post.objects.get(pk=pk)
        comment = Comment.objects.create(content=text, post=post, creator=request.user)
    return redirect(request.META.get("HTTP_REFERER", '/'))


@login_required
def newPost(request: HttpRequest):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        content = request.POST.get('content').strip()
        if name == "" or content == "":
            return render(request, 'createPost.html')
        Post.objects.create(content=content, creator=request.user, name=name)

        return redirect('/')
    return render(request, 'createPost.html')
