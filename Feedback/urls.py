from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    # path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('moderator-dashboard/', views.moderator_dashboard, name='moderator_dashboard'),
    path('department-dashboard/', views.department_dashboard, name='department_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('give-feedback/', views.give_feedback, name='give_feedback'),
    path('view-feedback/', views.view_feedback, name='view_feedback'),
    # path('success/', views.success, name='success'),
    path("moderator/", views.moderator_dashboard, name="moderator_dashboard"),
    path("update-status/<int:feedback_id>/<str:status>/", views.update_status, name="update_status"),
    # path("approve/<int:feedback_id>/", views.approve_feedback, name="approve_feedback"),
    path("reject/<int:feedback_id>/", views.reject_feedback, name="reject_feedback"),
    path('track-feedback/', views.track_feedback, name="track_feedback"),
    path('logout/', views.logout_view, name='logout'),
]
