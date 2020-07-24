from django.shortcuts import render
from django.contrib import messages
from groups.models import Group,GroupMember
from . import models
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.views.generic import RedirectView,CreateView,DetailView,ListView
# Create your views here.
class CreateGroup(LoginRequiredMixin,CreateView):
    fields = ('name','description')
    model = Group
class SingleGroup(DetailView):
    model = Group
class ListGroup(ListView):
    model = Group
class JoinGroup(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self,*args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    def get(self,request,*args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,('Warning, already a member of {}'.format(group.name)))
        else:
            messages.success(self.request,"You are now a member of the {} group".format(group.name))
        return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    def get(self,request,*args,**kwargs):
        try:
            membership = GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug')).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request,"You can't leave this group because you aren't in it.")
        else:
            membership.delete()
            messages.success(self.request,"You have successfully left this group.")
        return super().get(request,*args,**kwargs)