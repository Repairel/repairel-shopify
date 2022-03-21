def get_keys():
    try:
        from repairelapp import keys
        SHOPIFY_API_KEY = keys.API_KEY
        SHOPIFY_API_PASSWORD = keys.PASSWORD
        REPAIREL_API_KEY = keys.REPAIREL_API_KEY
        REPAIREL_API_PASSWORD = keys.REPAIREL_API_PASSWORD
        
        return (SHOPIFY_API_KEY,
                SHOPIFY_API_PASSWORD,
                REPAIREL_API_KEY,
                REPAIREL_API_PASSWORD
                )
        
    except ImportError:
        #alternative for AWS production server
        import os
        SHOPIFY_API_KEY = os.environ.get('SHOPIFY_API_KEY')
        SHOPIFY_API_PASSWORD = os.environ.get('SHOPIFY_API_PASSWORD')
        REPAIREL_API_KEY = os.environ.get('REPAIREL_API_KEY')
        REPAIREL_API_PASSWORD = os.environ.get('REPAIREL_API_PASSWORD')
        
        return (SHOPIFY_API_KEY,
                SHOPIFY_API_PASSWORD,
                REPAIREL_API_KEY,
                REPAIREL_API_PASSWORD
                )