from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from classroom.models import Channel, ChannelMember


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    template_name = "classroom/channels/channel_form.html"
    model = Channel

    def form_valid(self, form):
        form.instance.admin = self.request.user.username
        return super(CreateGroup, self).form_valid(form)


class SingleGroup(LoginRequiredMixin, generic.DetailView):
    model = Channel
    template_name = "classroom/channels/channel_detail.html"


class ListGroups(generic.ListView):
    model = Channel
    template_name = "classroom/channels/channel_list.html"


class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("channels:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, slug=self.kwargs.get("slug"))

        try:
            ChannelMember.objects.create(user=self.request.user, channel=channel)

        except IntegrityError:
            messages.warning(self.request, ("Warning, already a member of {}".format(channel.name)))

        else:
            messages.success(self.request, "You are now a member of the {} group.".format(channel.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("channels:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = ChannelMember.objects.filter(
                user=self.request.user,
                channel__slug=self.kwargs.get("slug")
            ).get()

        except ChannelMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
