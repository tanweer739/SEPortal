from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Leave, Reply
from .forms import LeaveForm, UpdateForm, AcceptorReject, ReplyForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


# Create your views here.

class LeaveListView(LoginRequiredMixin, ListView):
    model = Leave
    template_name = 'bookleave/leaves.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'leaves'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        leaves = Leave.objects.all()
        total_leaves = 0
        total_sick = 0
        total_vacation = 0
        for leave in leaves:
            total_leaves += leave.difference
        context['total_leave'] = total_leaves

        sickleaves = Leave.objects.filter(type='Sickday', owner=self.request.user).all()
        for leave in sickleaves:
            total_sick += leave.difference
        context['total_sick'] = total_sick

        vacationleaves = Leave.objects.filter(type='Vacation', owner=self.request.user).all()
        for leave in vacationleaves:
            total_vacation += leave.difference
        context['total_vacation'] = total_vacation

        number = Leave.objects.filter(owner=self.request.user).all()
        context['number'] = number
        return context


class All_LeaveListView(LoginRequiredMixin, ListView):
    model = Leave
    template_name = 'bookleave/all_leaves.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'leaves'
    paginate_by = 5


class LeaveCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'bookleave/new_leave.html'
    success_message = 'Leave is successfully Created'

    # override for current logged in user

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class LeaveDetailView(LoginRequiredMixin, DetailView):
    model = Leave

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(leave=self.object).all()
        return context


class LeaveUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Leave
    form_class = UpdateForm
    success_message = 'Leave is successfully Updated'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['current_leave'] = self.get_object()
        return kwargs

    def test_func(self):
        leave = self.get_object()
        return self.request.user == leave.owner


class LeaveAcceptorRejectView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Leave
    form_class = AcceptorReject
    template_name = 'bookleave/accept_or_reject.html'
    success_message = 'Leave status successfully Updated , You can give Feedback now'

    def get_success_url(self):
        leave = self.get_object()
        return reverse_lazy('leave-detail', kwargs={'pk': leave.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@login_required
def add_reply(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    if request.method == "POST":
        form = ReplyForm(request.POST, user=request.user)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.leave = leave
            reply.save()
            messages.success(request, 'Feedback is successfully added')
            return redirect('leave-detail', pk=pk)
    else:
        form = ReplyForm(user=request.user)
    return render(request, 'bookleave/add_reply.html', {'form': form, 'leave': leave})


class ReplyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Reply
    fields = ['content', ]
    success_message = 'Feedback is successfully Updated'

    # override for current logged in user

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        leave = self.get_object()
        return self.request.user == leave.owner


class ReplyDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Reply
    success_message = 'Feedback is successfully Deleted'

    def get_success_url(self):
        leave = self.object.leave
        return reverse_lazy('leave-detail', kwargs={'pk': leave.id})

    def test_func(self):
        leave = self.get_object()
        return self.request.user == leave.owner

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
