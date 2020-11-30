from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Report, Feedback
from .forms import FeedbackForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q


# Create your views here.


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reportsick/reports.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'reports'
    paginate_by = 5

    # this method override is used for sending specific model's attibutes to the template and use it there
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        number = Report.objects.filter(author=self.request.user).all()
        context['number'] = number
        return context


class AllReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reportsick/allreports.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'reports'
    paginate_by = 5


# Multiple object mixin is used for two related models pagination
class ReportDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = Report
    paginate_by = 5

    def get_context_data(self, **kwargs):
        object_list = Feedback.objects.filter(report=self.get_object()).all()
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class ReportCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Report
    fields = ['title', 'content', 'document']
    success_message = 'Your Report is successfully made'

    # override for current logged in user

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ReportUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Report
    fields = ['title', 'content', 'document']
    success_message = 'Your Report is successfully Updated'

    # override for current logged in user

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        report = self.get_object()
        return self.request.user == report.author


@login_required
def add_feedback(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.report = report
            feedback.save()
            messages.success(request, 'Reply is successfully made')
            return redirect('report-detail', pk=pk)
    else:
        form = FeedbackForm(user=request.user)
    return render(request, 'reportsick/add_feedback.html', {'form': form})


class FeedbackUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Feedback
    fields = ['content', 'document']
    success_message = 'Your Reply is successfully Updated'

    # override for current logged in user

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        report = self.get_object()
        return self.request.user == report.author


class FeedbackDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Feedback
    success_message = 'Your Reply is successfully Deleted'

    def get_success_url(self):
        report = self.object.report
        return reverse_lazy('report-detail', kwargs={'pk': report.id})

    def test_func(self):
        report = self.get_object()
        return self.request.user == report.author

    # overriding delete method just to make success message work , SuccessMessageMixin is not supported in DeleteViews.
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
