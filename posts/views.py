from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

from .forms import PostForm, CommentForm, ProfileEditForm
from .models import Post, Group, User, Comment, Follow


@cache_page(20)
def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page, "paginator": paginator})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = Post(text=form.cleaned_data['text'], group=form.cleaned_data['group'], author=request.user)
            new_post.save()
            return redirect('/')
        return render(request, 'new_post.html', {'form': form})
    form = PostForm()
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    post_list = profile.posts.order_by('-pub_date').all()
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    follow = Follow.objects.filter(user=request.user, author=profile).exists()
    return render(request, 'profile.html', {"profile": profile, "page": page, "paginator": paginator, 'follow': follow})


@login_required
def profile_edit(request, username):
    if request.user.username != username:
        return redirect('profile', username)
    form = ProfileEditForm(request.POST or None, instance=request.user)
    if form.is_valid():
        request.user.first_name = form.cleaned_data['first_name']
        request.user.last_name = form.cleaned_data['last_name']
        request.user.email = form.cleaned_data['email']
        request.user.save()
        return redirect('profile', username)
    return render(request, 'profile_edit.html', {'form': form})


def post_view(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    form = CommentForm()
    return render(request, 'post.html', {'post': post, 'profile': profile, 'form': form})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect("post", username=username, post_id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            post.save()
            return redirect("post", username=username, post_id=post_id)
    return render(request, 'new_post.html', {'form': form, 'edit': True, 'post': post})


@login_required
def post_delete(request, username, post_id):
    if request.user.username != username:
        return redirect('post', username=username, post_id=post_id)
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@login_required
def add_comment(request, username, post_id):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = get_object_or_404(Post, pk=post_id)
        new_comment = Comment(text=form.cleaned_data['text'], post=post, author=request.user)
        new_comment.save()
    return redirect('post', username=username, post_id=post_id)


@login_required
def comment_delete(request, username, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        comment.delete()
    return redirect('post', username=username, post_id=post_id)


@login_required
def follow_index(request):
    followings = User.objects.get(pk=request.user.id).follower.all().values_list('author')
    posts = Post.objects.filter(author__in=followings).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    following = request.user.follower.filter(author=author).exists()
    if not following and author.id != request.user.id:
        new_following = Follow(user=request.user, author=author)
        new_following.save()
    return redirect('profile', username=username)

@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    following = request.user.follower.filter(author=author)
    if following.exists():
        following.delete()
    return redirect('profile', username=username)



