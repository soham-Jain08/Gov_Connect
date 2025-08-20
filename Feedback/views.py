from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserAccount, Feedback
from django.contrib.auth import logout

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username').strip()
#         password = request.POST.get('password').strip()

#         try:
#             user = UserAccount.objects.get(username=username, password=password)
#         except UserAccount.DoesNotExist:
#             messages.error(request, "Invalid username or password")
#             return render(request, 'login.html')

#         # Store user info in session (optional)
#         request.session['username'] = user.username
#         request.session['role'] = user.role
#         request.session['department'] = user.department

#         # Redirect based on role
#         if user.role == 'admin':
#             return redirect('/admin-dashboard/')
#         elif user.role == 'moderator':
#             return redirect('/moderator-dashboard/')
#         elif user.role == 'department':
#             return redirect('/department-dashboard/')
#         else:
#             messages.error(request, "Invalid role assigned to user.")
#             return render(request, 'login.html')

#     return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        try:
            user = UserAccount.objects.get(username=username, password=password)

            # Redirect based on role
            if user.role == 'moderator':
                return redirect(f'/moderator/?moderator_name={user.username}')
            elif user.role == 'department':
                return redirect(f'/department-dashboard/?dept_name={user.department}&name={user.username}')

                # return render(request, 'deptHome.html', {'representative_name': user.username, 'dept_name':user.department})
            elif user.role == 'admin':
                return render(request, 'modHome.html', {'moderator_name': user.username})
            else:
                messages.error(request, "Invalid role.")
        except UserAccount.DoesNotExist:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def admin_dashboard(request):
    return render(request, 'modHome.html')

# def moderator_dashboard(request):
#     moderator_name = request.GET.get('moderator_name')
#     return render(request, 'modHome.html', {'moderator_name': moderator_name})

def moderator_dashboard(request):
    moderator_name = request.GET.get('moderator_name')
    department = request.GET.get('department')
    state = request.GET.get('state')
    location = request.GET.get('location')

    feedbacks = Feedback.objects.all()

    if department:
        feedbacks = feedbacks.filter(department_name=department)
    if state:
        feedbacks = feedbacks.filter(state=state)
    if location:
        feedbacks = feedbacks.filter(city=location)

    return render(request, "modHome.html", {"feedbacks": feedbacks, "moderator_name": moderator_name})

def update_status(request, feedback_id, status):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.status = status
    feedback.save()
    return redirect("moderator_dashboard")

def reject_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    return redirect("moderator_dashboard")

def department_dashboard(request):
    dept_name = request.GET.get('dept_name')
    name = request.GET.get('name')
    return render(request, 'deptHome.html', {'dept_name': dept_name, 'name': name})

def dashboard(request):
    return render(request, 'home.html')

def track_feedback(request):
    tracking_id = request.GET.get("trackingId")  # retrieve from form input

    feedback = None
    if tracking_id:
        # fetch feedback by feedback_id (your tracking column)
        feedback = Feedback.objects.filter(feedback_id=tracking_id).first()

    context = {
        "tracking_id": tracking_id,
        "feedback": feedback,  # pass full feedback object
    }

    return render(request, "track.html", context)


# def give_feedback(request):
#     return render(request, 'giveFeedback.html')

def view_feedback(request):
    return render(request, 'viewFeedback.html')

# def success(request):
#     return render(request, 'success.html')

def give_feedback(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        department_name = request.POST.get("department_name")
        city = request.POST.get("city")
        state = request.POST.get("state")
        media = request.FILES.get("mediaUpload")

        feedback = Feedback(
            subject=subject,
            description=description,
            department_name=department_name,
            city=city,
            state=state,
            media=media,
        )
        feedback.save()

        return render(request, "success.html", {"feedback_id": feedback.feedback_id})

    return render(request, "giveFeedback.html")

def logout_view(request):
    logout(request)
    return redirect('login')  

