from app.models import Product


_PRODUCTS = [
    Product(id=101, name="4K Smart Television", category="Televisions", price=42999, stock_quantity=12),
    Product(id=102, name="Wireless Headphones", category="Audio", price=2499, stock_quantity=4),
    Product(id=103, name="Front Load Washing Machine", category="Appliances", price=31990, stock_quantity=0),
    Product(id=104, name="Android Smartphone", category="Mobiles", price=18999, stock_quantity=25),
]


def list_products(search: str | None = None) -> list[Product]:
    products = [product for product in _PRODUCTS if product.active]
    if search:
        term = search.strip().casefold()
        products = [product for product in products if term in product.name.casefold()]
    return products


def get_product(product_id: int) -> Product | None:
    return next((product for product in _PRODUCTS if product.id == product_id), None)


def list_low_stock_products(threshold: int = 5) -> list[Product]:
    return [
        product
        for product in _PRODUCTS
        if product.active and product.stock_quantity <= threshold
    ]
