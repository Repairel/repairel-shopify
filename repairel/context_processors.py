from repairelapp.shopify import get_cart

def cart(request):
    return {"cart": get_cart(request)}