from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.forms import CheckboxSelectMultiple
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import Attempt, Client, Mailing, Message


@cache_page(60 * 15)
def home(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='started').count()
    total_clients = Client.objects.count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'total_clients': total_clients,
    }
    return render(request, "mailing/home.html", context)


# ==================== Клиенты ====================
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "mailing/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        # Менеджер видит всех клиентов
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Client.objects.all()
        # Обычный пользователь видит только своих
        cache_key = f'clients_user_{self.request.user.id}'
        queryset = cache.get(cache_key)
        if queryset is None:
            queryset = Client.objects.filter(owner=self.request.user)
            cache.set(cache_key, queryset, 60 * 15)
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "mailing/client_detail.html"
    context_object_name = "client"


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        # Менеджер не может редактировать чужие данные
        if user.groups.filter(name='Менеджер').exists():
            return False
        return obj.owner == user


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = "mailing/client_confirm_delete.html"
    success_url = reverse_lazy("mailing:client_list")

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        if user.groups.filter(name='Менеджер').exists():
            return False
        return obj.owner == user


# ==================== Сообщения ====================
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/message_list.html"
    context_object_name = "messages"


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing/message_detail.html"
    context_object_name = "message"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")


# ==================== Рассылки ====================
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        # Менеджер видит все рассылки
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Mailing.objects.all()
        # Обычный пользователь видит только свои
        cache_key = f'mailings_user_{self.request.user.id}'
        queryset = cache.get(cache_key)
        if queryset is None:
            queryset = Mailing.objects.filter(owner=self.request.user)
            cache.set(cache_key, queryset, 60 * 15)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ["start_time", "end_time", "message", "recipients"]
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['recipients'].widget = CheckboxSelectMultiple()
        form.fields['recipients'].queryset = Client.objects.filter(owner=self.request.user)
        form.fields['message'].queryset = Message.objects.all()
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    fields = ["start_time", "end_time", "message", "recipients"]
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['recipients'].widget = CheckboxSelectMultiple()
        form.fields['recipients'].queryset = Client.objects.filter(owner=self.request.user)
        form.fields['message'].queryset = Message.objects.all()
        return form

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        if user.groups.filter(name='Менеджер').exists():
            return False
        return obj.owner == user


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        if user.groups.filter(name='Менеджер').exists():
            return False
        return obj.owner == user


def send_mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)

    # Проверка времени
    now = timezone.now()
    if not (mailing.start_time <= now <= mailing.end_time):
        messages.error(request, f"Отправка возможна только в период с {mailing.start_time} по {mailing.end_time}")
        return redirect("mailing:mailing_detail", pk=pk)

    recipients = mailing.recipients.all()
    success_count = 0
    fail_count = 0

    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            Attempt.objects.create(status="success", server_response="Письмо успешно отправлено", mailing=mailing)
            success_count += 1
        except Exception as e:
            Attempt.objects.create(status="failed", server_response=str(e), mailing=mailing)
            fail_count += 1

    messages.success(request, f"Отправлено: {success_count}, Ошибок: {fail_count}")
    return redirect("mailing:mailing_detail", pk=pk)
