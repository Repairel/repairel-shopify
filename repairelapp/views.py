from django.shortcuts import render, redirect
from .models import ShoeItem, ShoeRequest, UserAccount
from django.views.generic import View, TemplateView
from .forms import ShoeRequestForm, LoginForm, RegistrationForm
from django.contrib import messages
from django.utils import timezone
from repairelapp.shopify import shopify_all_products, shopify_get_product
def latest_updated_list():
    return ShoeItem.objects.order_by("-created")[:20]

class IndexView(View):

    def get_queryset(self):
        return ShoeItem.objects.filter(created__lte=timezone.now()).order_by('-created')[:5]

    def get(self, *args, **kwargs):
        latest_updated = ShoeItem.objects.filter(created__lte=timezone.now()).order_by('-created')[:5]
        ongoing_list = ShoeItem.objects.filter(in_stock=True).order_by("-updated")
        rated_list = ShoeItem.objects.filter(in_stock=True).order_by("-rating")

        items = shopify_all_products()
        context = {
            'latest_list': latest_updated,
            'ongoing_list': ongoing_list,
            'rated_list': rated_list,
            'items': items,
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

class ScoringView(TemplateView):
    template_name = 'scoring.html'

# class ShopifyView(View):
#     def get(self, *args, **kwargs):
#         get_products = shopify_products.get_products()
#         products = get_products['products']
#         display_items = []
#         for prod in products:
#             if prod["status"] != "active":
#                 continue
#             sizes = [variant["option1"] for variant in prod["variants"]]
#             price = min([variant["price"] for variant in prod["variants"]])
#             max_size = max(sizes)
#             min_size = min(sizes)
#             display_items.append({
#                 "title": prod["title"],
#                 "image": prod["image"]["src"],
#                 "size": f'{min_size}-{max_size}',
#                 "price": price,
#             })
#
#         context = {
#             'products': display_items,
#         }
#         return render(self.request, "shopify_items.html", context)

class BlogView(TemplateView):
    def get(self, *args, **kwargs):

        context = {
            'blogs': blogs
        }

        return render(self.request, "blog.html", context)

class ShoeView(TemplateView):
    def get(self, *args, **kwargs):

        shoe = shopify_get_product(self.kwargs['shoe_id'])
        attributes = {
            "design": {"title": "Design", "image": "data:image/svg+xml;base64,PHN2ZyBpZD0iQ2FwYV8xIiBlbmFibGUtYmFja2dyb3VuZD0ibmV3IDAgMCA1MTAuMTMxIDUxMC4xMzEiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA1MTAuMTMxIDUxMC4xMzEiIHdpZHRoPSI0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Zz48cGF0aCBkPSJtNDYxLjkxNCA1MDkuODYzIDQ4LjIxNy00OC4yMDgtMjcuOTExLTM0LjI0NyAyNy45MTEtMzQuMjUtMjcuOTExLTM0LjI1MSAyNy45MTEtMzQuMjU1LTI3LjkxMS0zNC4yNTYgMjcuOTExLTM0LjI1NS0yNy45MTEtMzQuMjU3IDI3LjkxMS0zNC4yNjItNDguMjA4LTQ4LjIxNy0zNC4yNDcgMjcuOTExLTM0LjI1LTI3LjkxMS0zNC4yNTEgMjcuOTExLTM0LjI1NS0yNy45MTEtMzQuMjU2IDI3LjkxMS0zNC4yNTUtMjcuOTExLTM0LjI1NyAyNy45MTEtMzQuMjYyLTI3LjkxMS00OC4yMTcgNDguMjA4IDI3LjkxMSAzNC4yNDctMjcuOTExIDM0LjI1IDI3LjkxMSAzNC4yNTEtMjcuOTExIDM0LjI1NSAyNy45MTEgMzQuMjU2LTI3LjkxMSAzNC4yNTUgNC40NjggNS40ODQgMjMuNDQzIDI4Ljc3My0yNy43MTggMzYuNTc3IDQ4LjAxNSA0NS45MDIgMzQuMjQ3LTI3LjkxMSAzNC4yNSAyNy45MTEgMzQuMjUxLTI3LjkxMSAzNC4yNTUgMjcuOTExIDM0LjI1Ni0yNy45MTEgMzQuMjU1IDI3LjkxMSAzNC4yNTctMjcuOTExem0tMjEyLjAxMy04MC4yM2gtMzB2LTMwaDMwem0wLTYwaC0zMHYtMzBoMzB6bTAtNjBoLTMwdi0zMGgzMHptMC02MGgtMzB2LTMwaDMwem02MCAxODBoLTMwdi0zMGgzMHptMC02MGgtMzB2LTMwaDMwem0wLTYwaC0zMHYtMzBoMzB6bTAtNjBoLTMwdi0zMGgzMHptNjAgMTgwaC0zMHYtMzBoMzB6bTAtNjBoLTMwdi0zMGgzMHptMC02MGgtMzB2LTMwaDMwem0wLTYwaC0zMHYtMzBoMzB6bTMwLTMwaDMwdjMwaC0zMHptMCA2MGgzMHYzMGgtMzB6bTAgNjBoMzB2MzBoLTMwem0wIDYwaDMwdjMwaC0zMHoiLz48cGF0aCBkPSJtMTI4Ljg4NiAzNTguODcxLTI3LjkxMS0zNC4yNTUgMjcuOTEtMzQuMjU0LTI3LjkxMi0zNC4yNTMgMjcuOTEtMzQuMjQ5LTI5LjU4Ni0zNi4zMDIgODYuNTM5LTg2LjUyMiAzNi4zMTQgMjkuNTg0IDM0LjI1OS0yNy45MTMgMzQuMjU1IDI3LjkxMSAzNC4yNTYtMjcuOTExIDM0LjI1NCAyNy45MSAyNC43NzMtMjAuMTg3LTIzLjg1NC0yMS40NTggMjkuMzQtMzYuMDE3LTUwLjY3Ny01MC42ODctMzYuMDAxIDI5LjM0MS0zNi4wMDQtMjkuMzQxLTM2LjAwNiAyOS4zNDEtMzYuMDEtMjkuMzQxLTM2LjAxIDI5LjM0MS0zNi4wMS0yOS4zNDEtMzYuMDExIDI5LjM0MS0zNi4wMTctMjkuMzQxLTUwLjY4NyA1MC42NzggMjkuMzQxIDM2LTI5LjM0MSAzNi4wMDUgMjkuMzQxIDM2LjAwNS0yOS4zNDEgMzYuMDEgMjkuMzQxIDM2LjAxMS0yOS4zNDEgMzYuMDA5IDI5LjM0MSAzNi4wMTItMjkuMTM4IDM4LjQ1MSA1MC40NzQgNDguMjUzIDM2LjAwMS0yOS4zNDEgMjIuNjUzIDIyLjUxMXoiLz48L2c+PC9zdmc+"},
            "raw_materials": {"title": "Raw Materials", "image": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiA/PjwhRE9DVFlQRSBzdmcgIFBVQkxJQyAnLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4nICAnaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkJz48c3ZnICBlbmFibGUtYmFja2dyb3VuZD0ibmV3IDAuMTA3IC05LjU2NyAxNDEuNzMyIDE0MS43MzIiIHdpZHRoPSc0MCcgaGVpZ2h0PSc0MCcgaWQ9IkxpdmVsbG9fMSIgdmVyc2lvbj0iMS4xIiB2aWV3Qm94PSIwLjEwNyAtOS41NjcgMTQxLjczMiAxNDEuNzMyIiAgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+PGcgaWQ9IkxpdmVsbG9fNTQiPjxwYXRoIGQ9Ik0yOS4xMTYsMTE1LjM4M2gxMy40Mzh2LTExLjk5NkgyOS4xMTZWMTE1LjM4M3ogTTk5LjM5MywxMTUuMzgzaDEzLjQzOHYtMTEuOTk2SDk5LjM5M1YxMTUuMzgzeiBNMTMuNDM4LDQ4LjE5aDYuNzU2ICAgTDQuNDgxLDcwLjY5NWgxMy4xNjhMMCw5Ny40NjVoMjkuMTE1djIuMjEzTDQ2LjY0LDcxLjUzMUgzMS44NGwxNy42NjItMjYuNzc0aC03LjU5NGw2Ljg4NS0xMS42NjJMMzUuODM0LDEyLjM1NkwxMy40MzgsNDguMTl6ICAgIE05My4xNTIsMzMuMDkybDYuODg1LDExLjY2MmgtNy41OTRsMTcuNjYyLDI2Ljc3NEg5NS4zMDNsMTcuNTI0LDI4LjE0NnYtMi4yMTNoMjkuMTE3bC0xNy42NS0yNi43NzFoMTMuMTcxTDEyMS43NTIsNDguMTloNi43NTYgICBsLTIyLjM5Ni0zNS44MzRMOTMuMTUyLDMzLjA5MnogTTQ1Ljk1LDQyLjY0M2g3LjU5MkwzNS44NzksNjkuNDJoMTQuODA2bC0xOS44MzYsMzEuODU0aDMyLjcyNXYyMS4zMjNoMTUuMTA0di0yMS4zMjNoMzIuNzI3ICAgTDkxLjU2MSw2OS40MmgxNC44MDNMODguNzAxLDQyLjY0M2g3LjU5Mkw3MS4xMjIsMEw0NS45NSw0Mi42NDN6Ii8+PC9nPjxnIGlkPSJMaXZlbGxvXzFfMV8iLz48L3N2Zz4="},
            "material_manufacturing": {"title": "Material Manufacturing", "image": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTkuMC4wLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiBoZWlnaHQ9IjQwIiB3aWR0aD0iNDAiIHg9IjBweCIgeT0iMHB4IgoJIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiBzdHlsZT0iZW5hYmxlLWJhY2tncm91bmQ6bmV3IDAgMCA1MTIgNTEyOyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+CjxnPgoJPGc+CgkJPHBhdGggZD0iTTI0NS4zMzMsNDQ4SDEwLjY2N0M0Ljc3OSw0NDgsMCw0NTIuNzc5LDAsNDU4LjY2N3Y0Mi42NjdDMCw1MDcuMjIxLDQuNzc5LDUxMiwxMC42NjcsNTEyaDIzNC42NjcKCQkJYzUuODg4LDAsMTAuNjY3LTQuNzc5LDEwLjY2Ny0xMC42Njd2LTQyLjY2N0MyNTYsNDUyLjc3OSwyNTEuMjIxLDQ0OCwyNDUuMzMzLDQ0OHoiLz4KCTwvZz4KPC9nPgo8Zz4KCTxnPgoJCTxjaXJjbGUgY3g9IjQ4MCIgY3k9IjIwMi42NjciIHI9IjMyIi8+Cgk8L2c+CjwvZz4KPGc+Cgk8Zz4KCQk8cGF0aCBkPSJNMjI0LDM0MS4zMzNoLTMyVjMyMGMwLTM1LjI4NS0yOC43MTUtNjQtNjQtNjRzLTY0LDI4LjcxNS02NCw2NHYyMS4zMzNIMzJjLTUuODg4LDAtMTAuNjY3LDQuNzc5LTEwLjY2NywxMC42Njd2NzQuNjY3CgkJCWgyMTMuMzMzVjM1MkMyMzQuNjY3LDM0Ni4xMTIsMjI5Ljg4OCwzNDEuMzMzLDIyNCwzNDEuMzMzeiBNODUuMzMzLDM5NC42NjdjMCw1Ljg4OC00Ljc3OSwxMC42NjctMTAuNjY3LDEwLjY2NwoJCQlTNjQsNDAwLjU1NSw2NCwzOTQuNjY3di0yMS4zMzNjMC01Ljg4OCw0Ljc3OS0xMC42NjcsMTAuNjY3LTEwLjY2N3MxMC42NjcsNC43NzksMTAuNjY3LDEwLjY2N1YzOTQuNjY3eiBNMTI4LDM5NC42NjcKCQkJYzAsNS44ODgtNC43NzksMTAuNjY3LTEwLjY2NywxMC42NjdzLTEwLjY2Ny00Ljc3OS0xMC42NjctMTAuNjY3di0yMS4zMzNjMC01Ljg4OCw0Ljc3OS0xMC42NjcsMTAuNjY3LTEwLjY2NwoJCQlTMTI4LDM2Ny40NDUsMTI4LDM3My4zMzNWMzk0LjY2N3oiLz4KCTwvZz4KPC9nPgo8Zz4KCTxnPgoJCTxwYXRoIGQ9Ik00NzYuODg1LDMxMi40NjlsLTE5LjI2NC0xOS4yNjRjMC40NDgtMS43MDcsMS4wNDUtMy4zNDksMS4wNDUtNS4yMDVjMC0xLjg5OS0wLjYxOS0zLjU4NC0xLjA4OC01LjMzM2wyMS4xNjMtMjYuNzk1CgkJCWMtMTYuNDkxLTAuMzg0LTMwLjk5Ny04LjM0MS00MC41MTItMjAuNDU5bC05LjQ3MiwzMy4xMzFjLTQuMDc1LDEuODEzLTcuMjExLDQuOTkyLTkuNDcyLDguNzg5aC0yNC42MTkKCQkJYy01Ljg4OCwwLTEwLjY2Nyw0Ljc3OS0xMC42NjcsMTAuNjY3djQyLjY2N2MwLDUuODg4LDQuNzc5LDEwLjY2NywxMC42NjcsMTAuNjY3czEwLjY2Ny00Ljc3OSwxMC42NjctMTAuNjY3di0zMmgxMy45NTIKCQkJYzMuNzMzLDYuMjUxLDEwLjI2MSwxMC42NjcsMTguMDQ4LDEwLjY2N2MxLjgzNSwwLDMuNDk5LTAuNjE5LDUuMjA1LTEuMDQ1TDQ1NC4yNTEsMzIwbC0yNC40NDgsMjQuNDQ4CgkJCWMtNC4xNiw0LjE2LTQuMTYsMTAuOTIzLDAsMTUuMDgzYzIuMDY5LDIuMDkxLDQuOCwzLjEzNiw3LjUzMSwzLjEzNmMyLjczMSwwLDUuNDYxLTEuMDQ1LDcuNTUyLTMuMTE1bDMyLTMyCgkJCUM0ODEuMDQ1LDMyMy4zOTIsNDgxLjA0NSwzMTYuNjI5LDQ3Ni44ODUsMzEyLjQ2OXoiLz4KCTwvZz4KPC9nPgo8Zz4KCTxnPgoJCTxwYXRoIGQ9Ik0yNjYuNjY3LDEyOGMtMjcuODQsMC01MS45MDQtMTUuNTA5LTY0LjcyNS0zOC4xNjVsLTkzLjA1NiwxNDcuMTc5YzYuMTY1LTEuNDI5LDEyLjUyMy0yLjM0NywxOS4xMTUtMi4zNDcKCQkJYzMzLjk4NCwwLDYzLjE0NywyMC4wOTYsNzYuODY0LDQ4LjkxN2w3MC4zNzktMTU2LjQ1OUMyNzIuMzg0LDEyNy40NjcsMjY5LjYxMSwxMjgsMjY2LjY2NywxMjh6Ii8+Cgk8L2c+CjwvZz4KPGc+Cgk8Zz4KCQk8Y2lyY2xlIGN4PSIyNjYuNjY3IiBjeT0iNTMuMzMzIiByPSI1My4zMzMiLz4KCTwvZz4KPC9nPgo8Zz4KCTxnPgoJCTxwYXRoIGQ9Ik0zNDAuMjI0LDY0LjM2M2MtMy40NTYsMjMuMDgzLTE3LjQwOCw0Mi41MzktMzYuOTQ5LDUzLjYzMmwxMjQuMDk2LDc3LjY1M2MyLjMwNC0xNy4xOTUsMTIuNzM2LTMxLjcyMywyNy40MTMtMzkuNjgKCQkJTDM0MC4yMjQsNjQuMzYzeiIvPgoJPC9nPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+Cjwvc3ZnPgo="},
            "footwear_manufacturing": {"title": "Footwear Manufacturing", "image": "data:image/svg+xml;base64,PHN2ZyBpZD0iTGF5ZXJfMSIgZW5hYmxlLWJhY2tncm91bmQ9Im5ldyAwIDAgNTEyIDUxMiIgaGVpZ2h0PSI0MCIgd2lkdGg9IjQwIiB2aWV3Qm94PSIwIDAgNTEyIDUxMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Zz48Zz48Zz48cGF0aCBkPSJtNTA1Ljg1NCAxNTAuMzM2Yy0zLjY5MS0xLjc0OS04LjE0OS0xLjE3My0xMS4zNDkgMS40NTFsLTExMC41MDcgOTIuMDk2di04My44ODNjMC00LjEzOS0yLjM4OS03LjkxNS02LjE0NC05LjY2NC0zLjcxMi0xLjc0OS04LjE0OS0xLjE3My0xMS4zNDkgMS40NTFsLTExMC41MDcgOTIuMDk2di04My44ODNjMC00LjIyNC0yLjQ5Ni04LjA2NC02LjM3OS05Ljc3MS0zLjg0LTEuNzQ5LTguMzg0LS45Ni0xMS40OTkgMS44OTlsLTY2Ljg1OSA2MS4yOTFjLTIuNDMyIDIuMjQtMy43MTIgNS40ODMtMy40MTMgOC43ODlsMjQuMDIxIDI3Ni4yNjcgMTAuNTgxLS4zNjMtMTAuNjY3IDMuMjIxYzAgNS44ODggNC43NzkgMTAuNjY3IDEwLjY2NyAxMC42NjdoMjk4Ljg4YzUuODg4IDAgMTAuNjY3LTQuNzc5IDEwLjY2Ny0xMC42Njd2LTM0MS4zMzNjLjAwMS00LjEzOS0yLjM4OC03LjkxNS02LjE0My05LjY2NHptLTE4NS44NTYgMjQ0LjMzMWMwIDUuODg4LTQuNzc5IDEwLjY2Ny0xMC42NjcgMTAuNjY3aC02NGMtNS44ODggMC0xMC42NjctNC43NzktMTAuNjY3LTEwLjY2N3YtNjRjMC01Ljg4OCA0Ljc3OS0xMC42NjcgMTAuNjY3LTEwLjY2N2g2NGM1Ljg4OCAwIDEwLjY2NyA0Ljc3OSAxMC42NjcgMTAuNjY3em0xMjggMGMwIDUuODg4LTQuNzc5IDEwLjY2Ny0xMC42NjcgMTAuNjY3aC02NGMtNS44ODggMC0xMC42NjctNC43NzktMTAuNjY3LTEwLjY2N3YtNjRjMC01Ljg4OCA0Ljc3OS0xMC42NjcgMTAuNjY3LTEwLjY2N2g2NGM1Ljg4OCAwIDEwLjY2NyA0Ljc3OSAxMC42NjcgMTAuNjY3eiIvPjxwYXRoIGQ9Im0xMjcuOTU2IDkuNzQ5Yy0uNDctNS41MjUtNS4wOTktOS43NDktMTAuNjI0LTkuNzQ5aC02NGMtNS41MjUgMC0xMC4xNTUgNC4yMjQtMTAuNjI0IDkuNzQ5bC00Mi42NjcgNDkwLjY2N2MtLjI1NiAyLjk4Ny43NDcgNS45MzEgMi43NTIgOC4xMjhzNC44ODUgMy40NTYgNy44NzIgMy40NTZoMTQ5LjMzM2MuMTI4IDAgLjI3Ny0uMDIxLjQyNyAwIDUuODg4IDAgMTAuNjY3LTQuNzc5IDEwLjY2Ny0xMC42NjcgMC0xLjM2NS0uMjU2LTIuNjY3LS43MjUtMy44NjF6Ii8+PC9nPjwvZz48L2c+PGcvPjxnLz48Zy8+PGcvPjxnLz48Zy8+PGcvPjxnLz48Zy8+PGcvPjxnLz48Zy8+PGcvPjxnLz48Zy8+PC9zdmc+"},
            "retail": {"title": "Retail", "image": "data:image/svg+xml;base64,PHN2ZyBpZD0iQ2FwYV8xIiBlbmFibGUtYmFja2dyb3VuZD0ibmV3IDAgMCA0OTkgNDk5IiBoZWlnaHQ9IjQwIiB2aWV3Qm94PSIwIDAgNDk5IDQ5OSIgd2lkdGg9IjQwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxnPjxwYXRoIGQ9Im0xOTIuNSA4N2MzLjEzOS03NS42MzMgMTEwLjg4NS03NS41ODMgMTE0IDB2MjdoMzB2LTI3YzAtNDcuOTctMzkuMDMtODctODctODdzLTg3IDM5LjAzLTg3IDg3djI3aDMweiIvPjxwYXRoIGQ9Im0yMTEuMzMgMzU5LjUyIDUwLjgxIDE4LjQ4aDc0LjM2di0zMC4xYy0yMS4zNC0zLjA3LTQ0LjU3LTEyLjUzLTY5LjI5LTI4LjI0LTE1LjI5LTkuNzEtMjcuMjQtMTkuNC0zMy4zOC0yNC42NmgtNzEuMzN2ODNoMzEuNXoiLz48cGF0aCBkPSJtMzM2LjUgMTE0djY5aC0zMGMwLTE4LjUyNSAwLTUwLjgwNyAwLTY5aC0xMTR2NjloLTMwYzAtMTguNTI1IDAtNTAuODA3IDAtNjloLTE2MXYzODVoNDk2di0zODV6bS05MS4xIDE1MWM0LjExNiAzLjQ0IDU0LjM5NiA1Mi42MiAxMDYuMSA1NC4wMDEgMC0uMDAxIDE1LS4wMDEgMTUtLjAwMXY4OWgtMTA5LjY0bC0zNy4xOS0xMy41Mi0xMi42NyAxMy41MmgtNzQuNXYtMTQzeiIvPjwvZz48L3N2Zz4="},
            "use": {"title": "Use", "image": "data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjQwIiB2aWV3Qm94PSIwIC0xNiA1MTIgNTEyIiB3aWR0aD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0ibTkxIDQ1MC4wNTA3ODFoMTUwdjMwaC0xNTB6bTAgMCIvPjxwYXRoIGQ9Im0wIDM5MC4wNTA3ODFoMTUxdjMwaC0xNTF6bTAgMCIvPjxwYXRoIGQ9Im05Ny43NjU2MjUgMTMyLjY2NDA2MmMtNC45Njg3NS03LjQ5MjE4Ny0xMC44MzIwMzEtMTQuMTcxODc0LTE3LjQ0OTIxOS0yMC4wNDI5NjhsLTI5Ljc4OTA2MiA0MC44MTY0MDYgNjMuMTI4OTA2IDUwLjQ5MjE4OGMzLjQ1MzEyNS0yNC42ODM1OTQtMS44Nzg5MDYtNTAuMTQ4NDM4LTE1Ljg5MDYyNS03MS4yNjU2MjZ6bTAgMCIvPjxwYXRoIGQ9Im0xMjIuNzY5NTMxIDExNi4wODIwMzFjMjEuMjk2ODc1IDMyLjEwNTQ2OSAyNy4zMTI1IDcyLjAzNTE1NyAxNy4xNjc5NjkgMTA4Ljg3MTA5NGwyMDIuMzI4MTI1IDE2NS4wOTc2NTZoMTY4LjY5NTMxM2MtNC44NTU0NjktMzYuNTYyNS0yOC4yNDIxODgtNjguNDEwMTU2LTYxLjkyNTc4Mi04NS4yNTM5MDZsLTE1LjY4NzUtNy44NTE1NjNjLS40MTAxNTYtLjIwNzAzMS0uNzYxNzE4LS40ODgyODEtMS4xNjc5NjgtLjY5NTMxMmwtMjcuNzYxNzE5IDU1LjUwNzgxMi0yNi44MzU5MzgtMTMuNDE3OTY4IDI5LjQ3NjU2My01OC45NDE0MDZjLTMuNTExNzE5LTIuOTA2MjUtNi45MTc5NjktNS44ODI4MTMtMTAuMTA1NDY5LTkuMDkzNzVsLTQyLjE3OTY4NyA0Mi4xNzk2ODctMjEuMjEwOTM4LTIxLjIxMDkzNyA0NC41ODIwMzEtNDQuNTc4MTI2Yy0zLjIwNzAzMS01LjA3MDMxMi02LjAxNTYyNS0xMC4zMzk4NDMtOC41NDI5NjktMTUuNzg1MTU2bC02NC44MzU5MzcgMjUuMjIyNjU2LTEwLjg3MTA5NC0yNy45NDkyMTggNjUuOTc2NTYzLTI1LjY2Nzk2OWMtMi42MzY3MTktMTEuODk0NTMxLTMuOTM3NS0yNC4xOTUzMTMtMy4zMjQyMTktMzYuNzM0Mzc1bC43NjE3MTktMTUuNzMwNDY5aC0yMS40MDIzNDRjLTU1LjAxOTUzMSAwLTk3LjE1MjM0NC00MS4yMjI2NTYtMTAzLjQyMTg3NS05NS44OTA2MjUtMy42MTcxODctMzEuNTIzNDM3LTMxLjgzMjAzMS01NS41NjI1LTYyLjk0NTMxMy01NC4wOTc2NTZsLTcuMjY1NjI0LjI2NTYyNS02NC4yNjU2MjYgODguMDU0Njg3YzkuMzk0NTMyIDguMDAzOTA3IDE3Ljc3NzM0NCAxNy4xNzU3ODIgMjQuNzYxNzE5IDI3LjY5OTIxOXptMCAwIi8+PHBhdGggZD0ibTMzMS43NDYwOTQgNDIwLjA1MDc4MS0yOTguNDQ1MzEzLTI0MS45NjQ4NDMtMzMuMzAwNzgxIDUwLjA5NzY1NiAzMTAuNzQyMTg4IDI1MS44NjcxODdoMjAxLjI1NzgxMnYtNjB6bTAgMCIvPjwvc3ZnPg=="},
            "disposal": {"title": "Disposal", "image": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTguMC4wLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+CjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiBoZWlnaHQ9IjQwIiB3aWR0aD0iNDAiIHg9IjBweCIgeT0iMHB4IgoJIHZpZXdCb3g9IjAgMCAzMjQuNzI2IDMyNC43MjYiIHN0eWxlPSJlbmFibGUtYmFja2dyb3VuZDpuZXcgMCAwIDMyNC43MjYgMzI0LjcyNjsiIHhtbDpzcGFjZT0icHJlc2VydmUiPgo8Zz4KCTxwYXRoIGQ9Ik0xNTYuMzg2LDExNC43MzZsODUuNTUyLDEzLjYzMWwzMC4zOTktNzcuODczbC00LjE3MS04LjI1NmwtMTguMzkzLDguNjI0Yy0zLjU3Ny03LjkyNS05LjA1Ni0xOC41NjItMTcuMjY1LTI3LjY3MwoJCUMyMTcuMjcxLDYuMjc3LDE5OS4yNDUsNC44NjEsMTgzLjU0Myw0Ljg2MWMtMC4yMjMsMC02Ny42NjgtMC4wMjEtNjcuNjcxLTAuMDIxYy0xMC4yNzgsMC4wMDktMTguMTI0LDQuMzk4LTIzLjMxLDEzLjAyOAoJCUw1My4yNDcsODIuMDM0bDY5Ljc4MywzNi40MzZsMS4yMDMtMi4wNTRjNy44NjctMTMuNDE5LDE1Ljk0MS0yNy4wMTgsMjMuNzQ4LTQwLjE3YzIuMzc1LTQuMDAyLDQuNzUyLTguMDA0LDcuMTI1LTEyLjAwNwoJCWwxNy4xNzMsMzAuOTM2bC0yMS4wOTMsMTAuMTdMMTU2LjM4NiwxMTQuNzM2eiBNMTYzLjgxNyw0OS43MjRsMTYuODc1LTI5LjY4NmMxNS42OTIsMC4wMTcsMzAuNjI1LDEuMDcxLDQxLjE1NSwxMi43NTUKCQljNy43ODgsOC42NDYsMTIuNzIsMTguODk4LDE2LjUxNSwyNy43ODhsNC41MTIsOS4zNjVsNy45MS0zLjcwOGwtMTguMDA4LDQ2LjEzN2wtNDcuNDM2LTcuNTU4bDYuMjE5LTMuMDE2TDE2My44MTcsNDkuNzI0eiIvPgoJPHBhdGggZD0iTTMyMC42NTcsMTc2LjAzbC0zOC4zNDgtNjQuNzQ0bC02NC44MjgsNDQuNjYzbDEuMjUzLDIuMDI0YzcuOTAzLDEyLjc2NywxNS44NjgsMjUuNzkzLDIzLjU3MSwzOC4zOTEKCQljMi43MDksNC40MjksNS40MTYsOC44NTcsOC4xMjcsMTMuMjg0bC0zNS4zOTcsMC43MjJjMC4xNDctNC41NDcsMC40MjUtMTEuNjkzLDAuNTcxLTE1LjI3M2wwLjMyNC04LjEyNmwtMTAuNzQyLDAuMjA4CgkJbC01Mi4wMzUsNjkuMjYybDU0LjYzMyw2My4yNzFsOS4yNTEsMC4xNzNsMC45NzQtMjAuMjkzYzMuMzIsMC4yMDYsNi4zODEsMC4zMDcsOS4yOTcsMC4zMDdjOC42MDQsMCwxNi4yMDctMC44NjMsMjMuMjQtMi42MzYKCQljMjIuMDctNS41NjYsMzEuNzUtMjAuODQyLDM5LjA5NC0zNC43MzFjMC4yNjYtMC41MDYsMzEuMzIxLTU5LjIwOCwzMS42MzYtNTkuODAyQzMyNi4wNzcsMTkzLjY0NSwzMjUuODY0LDE4NC42NTUsMzIwLjY1NywxNzYuMDMKCQl6IE0yNDcuMDM4LDI4My4zNDljLTUuOSwxLjQ4OC0xMi4zMDYsMi4yMTItMTkuNTgyLDIuMjEyYy00LjkyNiwwLTkuNjA5LTAuMzQyLTEyLjcwMy0wLjU5OWwtMTAuMzkxLTAuMzg1bC0wLjQxOCw4LjcyMgoJCWwtMzIuMzY5LTM3LjQ4NGwyOC44NTItMzguMzk4bC0wLjI0Miw2Ljg5OWw1OS4wMS0wLjE4M2wxOC4zNTMsMjguNzkxQzI3MC4xOTksMjY2Ljc5LDI2Mi4yODgsMjc5LjUsMjQ3LjAzOCwyODMuMzQ5eiIvPgoJPHBhdGggZD0iTTc3LjU0NiwyMjEuMDgybDE3LjY0OC0zMC43MTljNC4zMDgsMi43ODUsMTEuMjI1LDcuMzMyLDEyLjc5Myw4LjM2NWw2Ljc5Miw0LjQ3MWw1LjM2NS05LjMxbC0zMi41MDEtODAuMzAzCgkJTDUuMjU2LDEyNy43NjFsLTQuOTIsNy44MzlsMTYuODg1LDExLjNjLTQuOTQ1LDcuMTY2LTExLjIzLDE3LjM1OC0xNC43ODUsMjkuMDcxYy02LjYxNywyMS43ODUsMS40OCwzNy45NTQsOS41NzYsNTEuMzc1CgkJYzAuMTEzLDAuMTkyLDI5LjEyMSw0OC4zMzEsMzQuOTM2LDU3Ljk4MmM1LjMwOSw4Ljc4NCwxMy4xMDIsMTMuMjM3LDIzLjIxMiwxMy4yMzdsNzIuMDc3LDAuMDE1bC0wLjAyNS03Ny42NzlMNzcuNTQ2LDIyMS4wODJ6CgkJIE02MC42MzUsMjIxLjA5N2wtMzQuMTM3LDAuODc3Yy04LjA5LTEzLjQ1Mi0xNC44OTktMjYuNzg3LTEwLjMzLTQxLjgzYzMuMzgxLTExLjEzMyw5LjYxNS0yMC42NTEsMTUuMjctMjguNDk1bDUuNjg2LTguNjk5CgkJbC03LjI1Ni00Ljg1OGw0OC44MS04LjQwMmwxOC4wMTcsNDQuNTIzbC01Ljc4OS0zLjc2OUw2MC42MzUsMjIxLjA5N3oiLz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8L3N2Zz4K"},
        }
        return render(self.request, "shoe.html", {"shoe": shoe, "attributes": attributes})