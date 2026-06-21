from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Post
from .forms import PostForm

# View all posts
def home(request):
    context = {'posts': Post.objects.all().order_by('-created_at')}
    return render(request, 'blog/home.html', context)

# View a single post (Public)
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

# Create a new post
@login_required
def create_post(request):
    if request.method == 'POST':
        # request.FILES must be here
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

# Edit a post
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user != post.author:
        return redirect('home')
        
    if request.method == 'POST':
        # request.FILES must be here
        print("DETECTED FILES:", request.FILES)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
        
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

# Delete a post
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
            return redirect('home')
        return render(request, 'blog/delete_confirm.html', {'post': post})
    else:
        return redirect('home')

# Register a new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})