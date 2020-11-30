from django.urls import path
from . import views
from .views import LeaveCreateView , LeaveListView , LeaveUpdateView , LeaveDetailView , All_LeaveListView , LeaveAcceptorRejectView , add_reply , ReplyDeleteView , ReplyUpdateView
urlpatterns = [
    path('leaves', LeaveListView.as_view(), name='leave-home'),
    path('leave/reports', All_LeaveListView.as_view(), name='all-leaves'),
    path('leave/<int:pk>/update', LeaveUpdateView.as_view(), name='leave-update'),
    path('leave/<int:pk>', LeaveDetailView.as_view(), name='leave-detail'),
    path('leave/new', LeaveCreateView.as_view(), name='leave-create'),
    path('leave/<int:pk>/accept-reject', LeaveAcceptorRejectView.as_view(), name='leave-accept-reject'),
    path('leave/<int:pk>/reply/', views.add_reply, name='add_reply'),
    path('reply/<int:pk>/update/', ReplyUpdateView.as_view(), name='reply-update'),
    path('reply/<int:pk>/delete/', ReplyDeleteView.as_view(), name='reply-delete'),
    #path('report/<int:pk>/update', ReportUpdateView.as_view(), name='report-update'),
    #path('post/<int:pk>/feedback/', views.add_feedback, name='add_feedback'),
    #path('feedback/<int:pk>/update/', FeedbackUpdateView.as_view(), name='feedback-update'),
    #path('feedback/<int:pk>/delete/', FeedbackDeleteView.as_view(), name='feedback-delete'),
]