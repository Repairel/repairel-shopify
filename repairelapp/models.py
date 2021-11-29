from django.db import models
from django.shortcuts import reverse
import datetime
from django.utils import timezone


DEFAULT_DESCRIPTION = """It was night again ere news came. A man rode in haste from the fords, saying that a host had issued from Minas Morgul and was already drawing nigh to Osgiliath; and it had been joined by regiments from the South, Haradrim, cruel and tall. ‘And we have learned,’ said the messenger, ‘that the Black Captain leads them once again, and the fear of him has passed before him over the River.’ With those ill-boding words the third day closed since Pippin came to Minas Tirith. Few went to rest, for small
hope had any now that even Faramir could hold the fords for long."""

class ShoeItem(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(default="https://se04-images.s3.eu-west-2.amazonaws.com/1460smooth_1080x_1ed4f99fc5.jpg")
    description = models.TextField(default=DEFAULT_DESCRIPTION)
    rating = models.FloatField(default=5.0)
    size = models.FloatField(default=6.0)
    price = models.FloatField(default=10.00)
    new = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    brand = models.CharField(max_length=100, default="Nike")
    in_stock = models.BooleanField(default=True)
    editors_pick = models.BooleanField(default=False)
    created = models.DateTimeField('date created')
    updated = models.DateTimeField(auto_now=True)
    design_score = models.FloatField(default=5.0)
    raw_materials_score = models.FloatField(default=5.0)
    material_manufacturing_score = models.FloatField(default=5.0)
    footwear_score = models.FloatField(default=5.0)
    retail_score = models.FloatField(default=5.0)
    use_score = models.FloatField(default=5.0)
    disposal_score = models.FloatField(default=5.0)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created <= now
    
    def was_updated_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.updated <= now
    
    def get_absolute_url(self):
        return reverse("repairelapp:index", kwargs={'pk': self.id})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Shoe Item'


class WishListItem(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcTLhoyoulsBNROT4YZGAK446q8c6NZuRMU68whWr1vdN4UbWiJs8QYjX06-vr6mAblBU&usqp=CAU")
    description = models.TextField(default=DEFAULT_DESCRIPTION)
    rating = models.FloatField(default=5.0)
    size = models.FloatField(default=6.0)
    price = models.FloatField(default=10.00)
    discount_price = models.FloatField(blank=True, null=True)
    new = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    brand = models.CharField(max_length=100, default="Nike")
    in_stock = models.BooleanField(default=True)
    editors_pick = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Wish Item'


class UserAccount(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default="Last Name")
    email = models.EmailField()
    password = models.CharField(max_length=100)
    image = models.ImageField(default="https://images.fineartamerica.com/images/artworkimages/mediumlarge/2/chipmunk-and-oak-im-spadecaller.jpg")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "User Accounts"


class ShoeRequest(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Shoe Requests"

    