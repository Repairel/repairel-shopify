from django.http import HttpResponse, JsonResponse
import requests


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

class ShopifyProduct:
    def __init__(self, product_id, title, description, thumbnail, price, tags, product_type, vendor, advanced_info=None):
        self.id = product_id
        self.name = title
        self.description = description
        self.thumbnail = thumbnail
        self.price = price
        self.tags = tags
        self.type = product_type
        self.vendor = vendor
        self.advanced_info = advanced_info

    def __str__(self):
        return '%s: %s' % (self.product_id, self.product_name)

class ShopifyProductAdvancedInfo:
    def __init__(self, environmental_impact):
        #environmental_impact is a dictionary of dictionaries (rating, text)
        self.environmental_impact = environmental_impact

def _shopify_construct_product(shopify_product):
    return ShopifyProduct(shopify_product["id"], shopify_product["title"], shopify_product["body_html"], shopify_product["image"]["src"], shopify_product["variants"][0]["price"], shopify_product["tags"], shopify_product["product_type"], shopify_product["vendor"])

def shopify_all_products():
    result = []
    response = requests.get(shopify_api + "products.json")
    data = response.json()
    products = data["products"]
    for product in products:
        result.append(_shopify_construct_product(product))
    return result

def shopify_get_product(id):
    response_product = requests.get(shopify_api + f"products/{id}.json")
    response_metafields = requests.get(shopify_api + f"products/{id}/metafields.json")
    #this is the base product
    result = _shopify_construct_product(response_product.json()["product"])

    #now parse metafields
    ENVIRONMENTAL_IMPACT_METAFIELDS = ["Design", "Raw Materials", "Material Manufacturing", "Footwear Manufacturing", "Retail", "Use", "Disposal"]
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

    advanced_info = ShopifyProductAdvancedInfo(environmental_impact)
    result.advanced_info = advanced_info
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
                result["products"].append(i.__dict__)
        elif request_type == 'product':
            result = shopify_get_product(argument).__dict__
            if result["advanced_info"]:
                result["advanced_info"] = result["advanced_info"].__dict__
        else:
            return HttpResponse('Unknown request type', status=400)

        return JsonResponse(result, safe=False)
    if request.method == 'POST':
        return HttpResponse("POST requests are not allowed", status=403)

    return HttpResponse(status=403)