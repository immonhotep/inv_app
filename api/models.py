from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid



def unique_slug(instance):
    model = instance.__class__
    unique_slug = str(uuid.uuid4())[:20]
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = str(uuid.uuid4())[:20]
    return unique_slug



class Category(models.Model):

    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(null=True,blank=True)
    description = models.TextField(max_length=3000, null=True, blank=True)


    def __str__(self):
        return self.name


@receiver(pre_save,sender=Category)
def category_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug(instance)
    

class Distributor(models.Model):

    name = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(null=True,blank=True)
    address =  models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

    
@receiver(pre_save,sender=Distributor)
def distributor_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug(instance)


class Item(models.Model):

    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(null=True, blank=True)
    in_stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    distributor = models.ForeignKey(Distributor, on_delete=models.SET_NULL,null=True, blank=True)
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    

@receiver(pre_save,sender=Item)
def item_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
         instance.slug = unique_slug(instance)



class Company_Premises(models.Model):

    name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(null=True, blank=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
       
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural='Premises'

    
@receiver(pre_save,sender=Company_Premises)
def premises_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug(instance)
    

STATUS = (

    ('P','Placed'),
    ('T','In Transit'),
    ('D','Delivered'),
    ('C','Closed'),
)


class Order(models.Model):

    slug = models.SlugField(null=True, blank=True)
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Company_Premises,on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1, choices=STATUS,default="P")
    date_placed = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(null=True, blank=True)

    
    def __str__(self):
        return self.slug
    

    
@receiver(pre_save,sender=Order)
def order_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug(instance)

     
        
             

