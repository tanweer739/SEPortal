from django.urls import path
from . import views
from .views import ReportListView , ReportDetailView , ReportCreateView , AllReportListView , ReportUpdateView , FeedbackUpdateView , FeedbackDeleteView
urlpatterns = [
    path('reports', ReportListView.as_view(), name='reports-home'),
    path('emp/reports', AllReportListView.as_view(), name='all-reports'),
    path('report/<int:pk>', ReportDetailView.as_view(), name='report-detail'),
    path('report/new', ReportCreateView.as_view(), name='report-create'),
    path('report/<int:pk>/update', ReportUpdateView.as_view(), name='report-update'),
    path('post/<int:pk>/feedback/', views.add_feedback, name='add_feedback'),
    path('feedback/<int:pk>/update/', FeedbackUpdateView.as_view(), name='feedback-update'),
    path('feedback/<int:pk>/delete/', FeedbackDeleteView.as_view(), name='feedback-delete'),
]