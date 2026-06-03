from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from mailing.models import Client

from .forms import LoginForm, RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Автоматически добавляем нового пользователя в клиенты
        Client.objects.get_or_create(
            email=self.object.email,
            defaults={"full_name": self.object.email, "comment": "Автоматически создан при регистрации"},
        )
        return response


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"
    next_page = reverse_lazy("mailing:home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("mailing:home")
