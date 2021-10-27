from django.shortcuts import render, redirect
from .models import ShoeItem, ShoeRequest, UserAccount
from django.views.generic import View, TemplateView
from .forms import ShoeRequestForm, LoginForm, RegistrationForm
from django.contrib import messages

def latest_updated_list():
    return ShoeItem.objects.order_by("-created")[:20]

class IndexView(View):
    def get(self, *args, **kwargs):
        latest_updated = latest_updated_list()
        ongoing_list = ShoeItem.objects.filter(in_stock=True).order_by("-updated")
        rated_list = ShoeItem.objects.filter(in_stock=True).order_by("-rating")

        context = {
            'latest_list': latest_updated,
            'ongoing_list': ongoing_list,
            'rated_list': rated_list,
        }
        return render(self.request, "index.html", context)

class AboutView(TemplateView):
    template_name = 'about.html'

class FAQView(TemplateView):
    template_name = 'faq.html'

class LoginView(View):
    def get(self, *args, **kwargs):
        form = RegistrationForm()
        context = {
            'form' : form
        }
        return render(self.request, 'login.html', context)

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = UserAccount()
                user.name = name
                user.email = email
                user.password = password
                user.save()
                messages.success(self.request, "We have successfully created your account. Thank You!")
                return redirect("repairelapp:index")
            except:
                messages.info(self.request, "Something went wrong! Please retry after some time.")
                return redirect("repairelapp:registration")
        else:
            messages.info(self.request, "Something went wrong! Please retry after some time.")
            return redirect("repairelapp:registration")


class RegistrationView(View):
    def get(self, *args, **kwargs):
        form = RegistrationForm()
        context = {
            'form' : form
        }
        return render(self.request, 'login.html', context)

    def post(self, *args, **kwargs):
        form = RegistrationForm(self.request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = UserAccount()
                user.name = name
                user.email = email
                user.password = password
                user.save()
                messages.success(self.request, "We have successfully created your account. Thank You!")
                return redirect("repairelapp:index")
            except:
                messages.info(self.request, "Something went wrong! Please retry after some time.")
                return redirect("repairelapp:registration")
        else:
            messages.info(self.request, "Something went wrong! Please retry after some time.")
            return redirect("repairelapp:registration")

class ShoppingCartView(TemplateView):
    template_name = 'shopping-cart.html'

class EngageView(TemplateView):
    template_name = 'engage.html'

class SustainabilityView(TemplateView):
    template_name = 'sustainability.html'

class TermsView(TemplateView):
    template_name = 'terms.html'

class GDPRView(TemplateView):
    template_name = 'gdpr.html'

class RequestView(View):
    def get(self, *args, **kwargs):
        form = ShoeRequestForm()
        context = {
            'form': form
        }
        return render(self.request, 'request.html', context)

    def post(self, *args, **kwargs):
        form = ShoeRequestForm(self.request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            author = form.cleaned_data.get('author')
            try:
                request = ShoeRequest()
                request.name = name
                request.description = description
                request.author = author
                request.save()
                messages.success(self.request, "We have successfully received your request. Thank You!")
                return redirect("repairelapp:index")
            except:
                messages.info(self.request, "Something went wrong! Please retry after some time.")
                return redirect("repairelapp:request")
        else:
            messages.info(self.request, "Something went wrong! Please retry after some time.")
            return redirect("repairelapp:request")