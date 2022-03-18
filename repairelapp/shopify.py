from ast import Index
from django.http import HttpResponse, JsonResponse
import requests
import json
import shopify as shopify_lib


SHOPIFY_API_KEY = None
SHOPIFY_API_PASSWORD = None
REPAIREL_API_KEY = None
REPAIREL_API_PASSWORD = None
try:
    from repairelapp import keys
    SHOPIFY_API_KEY = keys.API_KEY
    SHOPIFY_API_PASSWORD = keys.PASSWORD
    REPAIREL_API_KEY = keys.REPAIREL_API_KEY
    REPAIREL_API_PASSWORD = keys.REPAIREL_API_PASSWORD

except:
    #alternative for AWS production server
    import os
    SHOPIFY_API_KEY = os.environ.get('SHOPIFY_API_KEY')
    SHOPIFY_API_PASSWORD = os.environ.get('SHOPIFY_API_PASSWORD')
    REPAIREL_API_KEY = os.environ.get('REPAIREL_API_KEY')
    REPAIREL_API_PASSWORD = os.environ.get('REPAIREL_API_PASSWORD')

shopify_api = 'https://%s:%s@repairel-dev.myshopify.com/admin/api/2021-10/' % (SHOPIFY_API_KEY, SHOPIFY_API_PASSWORD)




class Variant:
    def __init__(self, id, title, price, option1, option2, option3):
        self.id = id
        self.title = title
        self.price = price
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3

class Option:
    def __init__(self, name, position, values):
        self.name = name
        self.position = position
        #array of possible values
        self.values = values

class ShopifyProduct:
    
    def __init__(self, id, name, description, thumbnail, images, price, tags, product_type, vendor, exact_sizes, colors, condition, gender, group, material, options, variants, compare_price, extra_info=None):
        self.id = id
        self.name = name
        self.description = description
        self.thumbnail = thumbnail
        self.images = images
        self.price = price
        self.tags = tags
        self.product_type = product_type
        self.vendor = vendor
        self.options = options
        self.variants = variants
        self.extra_info = extra_info
        self.sizes : list[float] = exact_sizes
        self.colors = colors
        self.material = material
        self.condition = condition
        self.gender = gender
        self.group = group
        self.compare_price = compare_price
        
        
    def __str__(self):
        return '%s: %s' % (self.id, self.name)

    def to_dict(self):
        if self.options:
            for i in range(len(self.options)):
                self.options[i] = self.options[i].__dict__
        if self.variants:
            for i in range(len(self.variants)):
                self.variants[i] = self.variants[i].__dict__
        if self.extra_info:
            self.extra_info = self.extra_info.__dict__
        return self.__dict__

class ShopifyProductAdvancedInfo:
    def __init__(self, environmental_impact, is_affiliate, affiliate_link):
        #environmental_impact is a dictionary of dictionaries (rating, text)
        self.environmental_impact = environmental_impact
        self.is_affiliate = is_affiliate
        self.affiliate_link = affiliate_link

class BlogPost:
    def __init__(self, title, date, body, excerpt, image):
        self.title = title
        self.date = date
        self.body = body
        self.excerpt = excerpt
        self.image = image

class Page:
    def __init__(self, title, body):
        self.title = title
        self.body = body

class Cart:
    def __init__(self, products):
        self.products = products


def _shopify_construct_page(page):
    return Page(page['title'], page['body_html'])
        
def _shopify_construct_article(article):
    """
    :param article: The blog post to be constructed
    :return: A class containing a blog post
    """

    published = article['published_at']
    y, m, d, t = published[:4], published[5:7], published[8:10], published[11:16]
    date = str(f'Published: {d}/{m}/{y} {t}')

    try:
        excerpt = article["summary_html"]
    except KeyError:
        print("There is no excerpt created: will use default blog description as the excerpt instead.")
        excerpt = article['body_html']

    try:
        image = article['image']['src']
    except KeyError:
        image = False

    return BlogPost(article['title'], date, article['body_html'], excerpt, image)

def all_articles():
    """
    Function to access all blog posts (known as articles in the API)
    :return: An array of blog post classes
    """

    r = requests.get(shopify_api + "blogs.json")
    blog = r.json()["blogs"][0]["id"]
    articles = requests.get(shopify_api + f"blogs/{blog}/articles.json")
    article_list = articles.json()["articles"]

    articles = []
    for article in article_list:
        articles.append(_shopify_construct_article(article))

    return articles

def _shopify_construct_product(shopify_product):
    #construct image urls
    images = []
    for image in shopify_product["images"]:
        images.append(image["src"])
    
    #construct options
    options = []
    for option in shopify_product["options"]: 
        options.append(Option(option["name"], option["position"], option["values"]))

    #construct variants
    variants = []
    for variant in shopify_product["variants"]:
        variants.append(Variant(variant["id"], variant["title"], variant["price"], variant["option1"], variant["option2"], variant["option3"]))
        
    # TODO: Search For Price Option
    sizes = None
    colors = None
    sizes = shopify_product["options"][0]["values"]
    try:
        colors = shopify_product["options"][1]["values"]
    except IndexError:
        print("No colours option have been assigned to the shoe item.")
    # price = min([var["price"] for var in shopify_product["variants"]])
    try:
        (condition, gender, group, material) = extract_tag(shopify_product["tags"])
    except ValueError:
        print("Couldn't unpack all values: one or more tags might be missing")

    return ShopifyProduct(
        id = shopify_product["id"], 
        name = shopify_product["title"], 
        description = shopify_product["body_html"], 
        thumbnail = shopify_product["image"]["src"],
        images = images, 
        price = shopify_product["variants"][0]["price"], 
        tags = shopify_product["tags"],
        product_type = shopify_product["product_type"], 
        vendor = shopify_product["vendor"],
        exact_sizes = sizes,
        colors = colors,
        condition = condition,
        gender = gender,
        group = group,
        material = material,
        options = options,
        variants = variants,
        compare_price = shopify_product["variants"][0]["compare_at_price"]
    )

    # TODO To be removed
    # return ShopifyProduct(shopify_product["id"], shopify_product["title"], shopify_product["body_html"], shopify_product["image"]["src"], images, shopify_product["variants"][0]["price"], shopify_product["tags"].split(", "), shopify_product["product_type"], shopify_product["vendor"], options, variants)

def shopify_all_products():
    """
    Get all active products from Shopify
    :return: An array of product classes
    """

    result = []
    response = requests.get(shopify_api + "products.json")
    data = response.json()
    products = data["products"]
    for product in products:
        if product["status"] != "active":
            continue
        result.append(_shopify_construct_product(product))
    return result

def shopify_get_product(id):
    """
    Get data on a specific product from its ID
    :param id: Shopify Product ID
    :return: A product class
    """

    response_product = requests.get(shopify_api + f"products/{id}.json")
    response_metafields = requests.get(shopify_api + f"products/{id}/metafields.json")
    #this is the base product
    result = _shopify_construct_product(response_product.json()["product"])

    #now parse metafields
    ENVIRONMENTAL_IMPACT_METAFIELDS = ["Design", "Raw Materials", "Material Manufacturing", "Footwear Manufacturing", "Retail", "Use", "Disposal", "Governance"]
    metafields = response_metafields.json()["metafields"]
    environmental_impact = {}
    for metafield in metafields:
        split = metafield["key"].split(" ")
        if len(split) >= 2:
            metafield_name = " ".join(split[:-1])
            if metafield_name in ENVIRONMENTAL_IMPACT_METAFIELDS:
                environmental_impact[metafield_name] = environmental_impact.get(metafield_name, {})
                environmental_impact[metafield_name][split[-1].lower()] = metafield["value"]
    for key in ENVIRONMENTAL_IMPACT_METAFIELDS:
        if key not in environmental_impact:
            environmental_impact[key] = {"rating": None, "text": None}
        else:
            if "rating" not in environmental_impact[key]:
                environmental_impact[key]["rating"] = None
            if "text" not in environmental_impact[key]:
                environmental_impact[key]["text"] = None

    #you can use this function for other values           
    def get_metafield_value(name):
        for metafield in metafields:
            if metafield["key"] == name:
                return metafield["value"]
        return None

    is_affiliate = get_metafield_value("Is Affiliate")
    if is_affiliate == None:
        is_affiliate = False
    affiliate_link = get_metafield_value("Affiliate Link")

    extra_info = ShopifyProductAdvancedInfo(environmental_impact, is_affiliate, affiliate_link)
    result.extra_info = extra_info
    return result

def api_view(request, key, password, request_type, argument=None):
    #verify the key and password
    if key != REPAIREL_API_KEY or password != REPAIREL_API_PASSWORD:
        return HttpResponse('Wrong API key or password', status=401)

    #for now we only support GET requests
    if request.method == 'GET':
        result = {}

        if request_type == 'all_products':
            raw_result = shopify_all_products()
            result["products"] = []
            for i in raw_result:
                result["products"].append(i.to_dict())
        elif request_type == 'product':
            result = shopify_get_product(argument).to_dict()
        else:
            return HttpResponse('Unknown request type', status=400)

        return JsonResponse(result, safe=False)
    if request.method == 'POST':
        return HttpResponse("POST requests are not allowed", status=403)

    return HttpResponse(status=403)


def all_pages():
    """
    Function to get all misc pages from the Shopify backend
    :return: An array of page classes
    """

    r = requests.get(shopify_api + "pages.json")
    pages = r.json()['pages']
    page_list = []

    for page in pages:
        page_list.append(_shopify_construct_page(page))

    # TODO REMOVE
    # page_dict = {}
    # for i in range(len(r.json()['pages'])):
    #     page_dict[r.json()["pages"][i]["title"]] = r.json()["pages"][i]["body_html"]

    return page_list


def cart_remove_duplicates(request):
    cart = json.loads(request.session.get('cart', '[]'))
    #merge duplicate items
    dictionary = {}
    for item in cart:
        dictionary[item['variant_id']] = dictionary.get(item['variant_id'], 0) + item['quantity']

    #convert to list
    result = []
    for key, value in dictionary.items():
        result.append({'variant_id': key, 'quantity': value})

    #save back to session
    request.session['cart'] = json.dumps(result)

def add_to_cart(request, variant_id, quantity):
    #TODO protection against taking more than stock
    request.session['cart'] = json.dumps(json.loads(request.session.get('cart', '[]')) + [{'variant_id': variant_id, 'quantity': quantity}])
    cart_remove_duplicates(request)

#returns list [{'variant_id': x 'quantity': y}, ...]
def get_cart(request):
    cart_remove_duplicates(request)
    return json.loads(request.session.get('cart', '[]'))

def extract_tag(string):
    print(string)
    tag = string.split(',')
    condition = None
    gender = None
    group = None
    material = None

    for item in tag:
        item = item.replace(' ', '')
        if item == "Refurbished":
            condition = "Refurbished"
        elif item == "New":
            condition = "New"
            
        if item == "Women":
            gender = "Women"
        elif item == "Men":
            gender = "Men"
        elif item == "Unisex":
            gender = "Unisex"
            
        if item == "Kids":
            group = "Kids"
        elif item == "Adults":
            group = "Adults"
            
        if item == "Leather":
            material = "Leather"
        if item == "Suede":
            material = "Suede"
        if item == "Textile":
            material = "Textile"
        if item == "Synthetic":
            material = "Synthetic"
        if item == "Vegan(Synthetic)":
            material = "Vegan (Synthetic)"
            
            
    return (condition, gender, group, material)

def newsletter_signup(email):
    customer = shopify_lib.Customer()
    customer.accepts_marketing = True
    customer.email = email
    customer.save()
