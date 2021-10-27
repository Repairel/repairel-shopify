from django.db import models
from django.shortcuts import reverse


DEFAULT_DESCRIPTION = """It was night again ere news came. A man rode in haste from the fords, saying that a host had issued from Minas Morgul and was already drawing nigh to Osgiliath; and it had been joined by regiments from the South, Haradrim, cruel and tall. ‘And we have learned,’ said the messenger, ‘that the Black Captain leads them once again, and the fear of him has passed before him over the River.’ With those ill-boding words the third day closed since Pippin came to Minas Tirith. Few went to rest, for small
hope had any now that even Faramir could hold the fords for long."""

class ShoeItem(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcTLhoyoulsBNROT4YZGAK446q8c6NZuRMU68whWr1vdN4UbWiJs8QYjX06-vr6mAblBU&usqp=CAU")
    description = models.TextField(default=DEFAULT_DESCRIPTION)
    rating = models.FloatField(default=5.0)
    in_stock = models.BooleanField(default=True)
    editors_pick = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Shoe'


