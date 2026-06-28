from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import Task
import google.generativeai as genai
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


model = genai.GenerativeModel("gemini-2.5-flash")

def home(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()

    progress = 0
    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'progress': progress,
    }

    return render(request, 'dashboard.html', context)

@login_required
def task(request):

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        priority = request.POST.get('priority')

        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            deadline=deadline,
            priority=priority
        )

        messages.success(request, "Task added successfully!")

        return redirect('dashboard')

    return render(request, 'task.html')

@login_required
def planner(request):

    response = ""

    if request.method == "POST":

        # Get all pending tasks from the database
        tasks = Task.objects.filter(
            user=request.user,
            completed=False
        )

        # Convert tasks into text for Gemini
        task_list = ""

        for task in tasks:
            task_list += f"""
Title: {task.title}
Description: {task.description}
Deadline: {task.deadline}
Priority: {task.priority}

"""

        # Get available hours from the form
        hours = request.POST.get("hours")

        # Create the prompt
        prompt = f"""
        You are SmartTask AI, an intelligent productivity assistant.

        The user has these pending tasks:

        {task_list}

        The user has {hours} hours available today.

        Your job is to create the BEST possible daily schedule.

        Instructions:

        1. Prioritize tasks according to:
           - Deadline
           - Priority (High > Medium > Low)
           - Estimated workload

        2. Divide the available hours into realistic time blocks.

        3. Mention short breaks whenever appropriate.

        4. Explain why each task is scheduled in that position.

        5. At the end, give 3 productivity tips.

        6. If there are more tasks than available time, recommend which tasks should be postponed.

        7. Keep the response beautiful and easy to read.

        Use the following format exactly:

        ==================================================

        📅 SMARTTASK AI DAILY PLAN

        ⏰ Total Available Time:
        {hours} Hours

        -----------------------------------------

        📌 Task 1
        Task:
        Time:
        Reason:

        -----------------------------------------

        📌 Task 2
        Task:
        Time:
        Reason:

        -----------------------------------------

        📌 Task 3
        Task:
        Time:
        Reason:

        -----------------------------------------

        ☕ Break Recommendation

        -----------------------------------------

        ⚠️ Most Urgent Task

        -----------------------------------------

        💡 Productivity Tips
        • Tip 1
        • Tip 2
        • Tip 3

        ==================================================

        Do not use Markdown (** or *).
        Use plain text only.
        """
        # Generate AI response
        result = model.generate_content(prompt)

        response = result.text

    return render(request, "planner.html", {"response": response})


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        # Create new user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "signup.html")

@login_required
def delete_task(request, id):
    task = Task.objects.get(
        id=id,
        user=request.user
    )

    task.delete()

    messages.success(request, "Task deleted successfully!")

    return redirect('dashboard')

@login_required
def complete_task(request, id):
    task = Task.objects.get(
        id=id,
        user=request.user
    )

    task.completed = True
    task.save()

    messages.success(request, "Task marked as completed!")

    return redirect('dashboard')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")

