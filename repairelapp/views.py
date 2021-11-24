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

        #TODO remove
        #create a list of shoes for testing purposes
        test_items = [
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/1cf81d24ab2037ff96e818898e9740f2_888c369d0c.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "1",
            "size": "9",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/1460smooth_1080x_1ed4f99fc5.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "2",
            "size": "4",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/15933002_b96c8ca547.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "3",
            "size": "5",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/hiking_boots_1_e4deb66ad5.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "4",
            "size": "11",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/wvs_hiking_shoe_women_64d7789834.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "1",
            "size": "9",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/1220509_removebg_preview_1_d6610b1840.png",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "2",
            "size": "4",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/23812002_R_651a79e150.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "3",
            "size": "5",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/small_ezgif_com_gif_maker_a8b62e041f_fd29e9b64d.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "4",
            "size": "11",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/22389101_b0372bb10d.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "1",
            "size": "9",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/assw_2_838ffe854d.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "2",
            "size": "4",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/nyw_5_50de1f0e89.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "3",
            "size": "5",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/cbw_5_680f849035.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "4",
            "size": "11",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/obw_3_9ff89c9c12.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "1",
            "size": "9",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/khw_3_fe58073308.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "2",
            "size": "4",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/gwbm_3_76c5f1e55d.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "3",
            "size": "5",
        },
        {
            "name": "Nike Air Max",
            "price": "100",
            "image": "https://se04-images.s3.eu-west-2.amazonaws.com/P1_repairel_9_4d8840bed4.jpg",
            "description": "This is a test shoe",
            "rating": "4.5",
            "in_stock": True,
            "id": "4",
            "size": "11",
        },
        ]


        context = {
            'latest_list': latest_updated,
            'ongoing_list': ongoing_list,
            'rated_list': rated_list,
            #TODO remove
            'test_items': test_items,
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

class ShoeView(TemplateView):
    def get(self, *args, **kwargs):
        #TODO
        shoe = {
                "name": "Nike Air Max",
                "price": "100",
                "image": "https://se04-images.s3.eu-west-2.amazonaws.com/P1_repairel_9_4d8840bed4.jpg",
                "description": "This is a test shoe,This is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoe,This is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoe,This is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoe,This is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoeThis is a test shoe",
                "rating": "4.5",
                "in_stock": True,
                "id": "4",
                "size": "11",
                "images": [
                    "https://se04-images.s3.eu-west-2.amazonaws.com/small_hiking_shoe_1_square_dc390e7097_Copy_38cc032709.jpg",
                    "https://se04-images.s3.eu-west-2.amazonaws.com/hiking_shoe_4_0861cc0ae0.jpg",
                    "https://se04-images.s3.eu-west-2.amazonaws.com/hiking_shoe_3_3b186f1ccb.jpg",
                    "https://se04-images.s3.eu-west-2.amazonaws.com/hiking_shoe_6_f922e7f808.jpg",
                    "https://se04-images.s3.eu-west-2.amazonaws.com/small_hiking_shoe_1_square_dc390e7097_Copy_38cc032709.jpg",
                    "https://se04-images.s3.eu-west-2.amazonaws.com/hiking_shoe_4_0861cc0ae0.jpg",
                    "https://se04-images.s3.eu-west-2.amazonaws.com/hiking_shoe_3_3b186f1ccb.jpg",
                    "https://se04-images.s3.eu-west-2.amazonaws.com/hiking_shoe_6_f922e7f808.jpg",
                ],
            }
        return render(self.request, 'shoe.html', {"shoe": shoe})