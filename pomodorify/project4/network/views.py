from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import User, Post, Follow, Like, Todo
from django.views.decorators.http import require_POST


def index(request):
    all_posts = Post.objects.all().order_by("id").reverse()
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)
    all_likes = Like.objects.all()
    whoYouLiked = []
    try:
        for like in all_likes:
            if like.user.id == request.user.id:
                whoYouLiked.append(like.post.id)
    except:
        whoYouLiked = []
    return render(request, "network/index.html", {
        "all_posts": all_posts,
        "posts_of_the_page": posts_of_the_page,
        "whoYouLiked": whoYouLiked
    })
    

def home(request):
    all_tasks = Todo.objects.all().order_by("id")


    return render(request, "network/home.html", {
       
        "all_tasks" : all_tasks,
       
    })



def add_like(request, Todo_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    newLike = Like(user=user, post=post)
    newLike.save()
    return JsonResponse({"message": "Like added!"})



def remove_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({"message": "Like removed!"})




def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Change successful", "data": data["content"]})
    
   

def new_post(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()

        return HttpResponseRedirect(reverse(index))


def new_task(request):
    if request.method == "POST":
        title = request.POST.get('title', '')  # Retrieve title from POST data
        pomodoro = request.POST.get('pomodoro', '')  # Retrieve pomodoro from POST data
        user = request.user  # You can directly access the authenticated user
        post = Todo.objects.create(title=title, pomodoro=pomodoro, user=user)
        post.save()
        
        return HttpResponseRedirect(reverse('home'))


def edit_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Todo, pk=task_id)
        title = request.POST.get('title', '')  # Retrieve title from POST data
        pomodoro = request.POST.get('pomodoro', '')  # Retrieve pomodoro from POST data
        
        # Update fields of the Todo object
        task.title = title
        task.pomodoro = pomodoro
        task.save()  # Save the changes
        
        return HttpResponseRedirect(reverse('home'))


def check_true(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Todo, pk=task_id)
        completed = True
        task.completed = completed
        task.save()  # Save the changes
        
        return HttpResponseRedirect(reverse('home'))


def update_pomo_counter(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Todo, pk=task_id)
        task.pomo_counter += 1
        task.save()  # Save the changes
        
        return HttpResponseRedirect(reverse('home'))
    
    


def check_false(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Todo, pk=task_id)
        completed = False
        task.completed = completed
        task.save()  # Save the changes
        
        return HttpResponseRedirect(reverse('home'))

    



def delete_task(request, task_id):
    task = get_object_or_404(Todo, pk=task_id)
    if request.method == "POST":
        task.delete()
        return HttpResponseRedirect(reverse('home')) 



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "network/register.html")
