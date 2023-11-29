from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product_code = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=10000)
    additional_info = models.JSONField(blank=True, null=True)
    image_urls = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name

    @classmethod
    def new(cls, *args, **kwargs):
        return cls.objects.create(*args, **kwargs)

    @classmethod
    def create_from_product_data(cls, product_data: dict):
        if not cls.valid_product_data(product_data):
            return None
        create_product = cls.objects.create(
            name=product_data.get('name'), price=product_data.get('price', 0),
            product_code=product_data.get('product_code', ''),
            description=product_data.get('description', ''),
            additional_info=product_data.get('additional_info', {}),
            image_urls=product_data.get('image_urls', {})
        )
        if create_product:
            return create_product
        return None

    @classmethod
    def valid_product_data(cls, product_data: dict) -> bool:
        valid = True
        required_fields = ['name', 'price']
        for k, v in product_data:
            if not k in required_fields:
                valid = False
        return valid

    @classmethod
    def get_model_fields(cls) -> list:
        fields = cls._meta.fields
        field_names = [field.name for field in fields]
        return field_names
