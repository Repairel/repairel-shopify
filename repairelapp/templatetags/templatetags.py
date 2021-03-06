from django import template
from django.conf import settings
from django.urls import reverse

register = template.Library()

@register.simple_tag
def get_value(dict, key):
    try:
        return dict[key]
    except:
        return ""

@register.filter(name='times') 
def times(number):
    number = int(number)
    return range(number)

@register.simple_tag
def shoe_decide_ball_color(number):
    number = int(number)
    base = "custom_scoring_balls_"
    if number == -1:
        return base + "grey"
    elif(number < 3):
        return base + "red"
    elif(number == 3):
        return base + "orange"
    else:
        return base + "green"
    

@register.simple_tag
def product_get_sizes(product):
    if product.options:
        for option in product.options:
            if option.name == "Size":
                return option.values
    return ""

@register.simple_tag
def array_to_string(array):
    if array:
        return ", ".join(array)
    return ""

@register.simple_tag
def sizes_to_limit_string(value):
    if value:
        if type(value) is list or type(value) is tuple:
            if len(value) == 1:
                return value[0]
            elif len(value) > 1:
                values = []
                non_values = []
                for a in value:
                    try:
                        values.append(float(a))
                    except:
                        non_values.append(a)
                if len(values) > 0:
                    maximum = max(values)
                    minimum = min(values)
                    def get_rid_of_zero(x):
                        if x % 1 == 0:
                            return int(x)
                        else:
                            return x
                    
                    comma = " "
                    if len(non_values) > 0:
                        comma = ", "
                    return f"{get_rid_of_zero(minimum)}-{get_rid_of_zero(maximum)}{comma}{', '.join(non_values)}"
                else:
                    return ", ".join(non_values)
            else:
                return ""
        else:
            return value
    return ""

@register.simple_tag
def cart_total_quantity(cart):
    return sum([item["quantity"] for item in cart])

@register.simple_tag
def construct_checkout_url(cart):
    #cart is a list of dictionaries
    arguments = []
    for item in cart:
        arguments.append(item["variant_id"] + ":" + str(item["quantity"]))
    return f"{settings.SHOPIFY_STORE_URL}cart/{','.join(arguments)}"

@register.simple_tag
def blog_get_url(blog):
    return reverse("repairelapp:blog", kwargs={"blog_name": blog.title.replace(" ", "-")})

@register.simple_tag
def get_page_url(page):
    return reverse("repairelapp:page", kwargs={"page_name": page.title.replace(" ", "-")})