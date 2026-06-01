from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Client, Message, Mailing, Attempt
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect


def home(request):
    return render(request, 'mailing/home.html')


# ==================== Клиенты ====================
class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    context_object_name = 'client'


class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')


# ==================== Сообщения ====================
class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')


# ==================== Рассылки ====================
class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # 👈 обновляем статус при просмотре
        return obj


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'message', 'recipients']
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'message', 'recipients']
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


def send_mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)

    # Проверка времени
    now = timezone.now()
    if not (mailing.start_time <= now <= mailing.end_time):
        messages.error(request, 'Отправка возможна только в период с {mailing.start_time} по {mailing.end_time}')
        return redirect('mailing:mailing_detail', pk=pk)

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
            Attempt.objects.create(
                status='success',
                server_response='Письмо успешно отправлено',
                mailing=mailing
            )
            success_count += 1
        except Exception as e:
            Attempt.objects.create(
                status='failed',
                server_response=str(e),
                mailing=mailing
            )
            fail_count += 1

    messages.success(request, f'Отправлено: {success_count}, Ошибок: {fail_count}')
    return redirect('mailing:mailing_detail', pk=pk)
