from django.db import models
import uuid

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        null=True,
        blank=True
    )
    
class SeasonalEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
class Attribute(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
class AttributeValue(models.Model):
    id = models.BigAutoField(primary_key=True)
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name='values'
    )
    
class ProductType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True
    )

class Product(models.Model):
    
    IN_STOCK = 'IS'
    OUT_OF_STOCK = 'OSS'
    BACKORDERED = 'BO'
    
    STOCK_STATUS_CHOICES = [
        (IN_STOCK, "In Stock"),
        (OUT_OF_STOCK, "Out Of Stock"),
        (BACKORDERED, "Back Ordered"),
    ]
    
    id = models.BigAutoField(primary_key=True)
    pid = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    is_digital = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    stock_status = models.CharField(
        max_length=3,
        choices=STOCK_STATUS_CHOICES,
        default=OUT_OF_STOCK
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, null=True,
        related_name='products'
    )
    seasonal_event = models.ForeignKey(
        SeasonalEvent,
        on_delete=models.SET_NULL, null=True,
        related_name='products'
    )
    product_type = models.ManyToManyField(
        ProductType,
        through='Product_ProductType',
        related_name='products'
    )
    
class ProductLine(models.Model):
    id = models.BigAutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sku = models.UUIDField(default=uuid.uuid4)
    stock_qty = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='product_lines'
    )
    attribute = models.ManyToManyField(
        AttributeValue,
        through='ProductLine_AttributeValue',
        related_name='product_lines'
    )
    
class ProductImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to='product_images')
    product_line = models.ForeignKey(
        ProductLine,
        on_delete=models.CASCADE,
        related_name='images'
    )
    
class ProductLine_AttributeValue(models.Model):
    product_line = models.ForeignKey(
        ProductLine,
        on_delete=models.CASCADE,
        related_name='attribute_values_relation'
    )
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name='product_line_attribute_values'
    )
    
class Product_ProductType(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_types_relation'
    )
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='product_product_types'
    )
    
class StockControl(models.Model):
    id = models.BigAutoField(primary_key=True)
    stock_qty = models.IntegerField(default=0)
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_control'
    ) 