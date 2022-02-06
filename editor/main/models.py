from django.db import models

class Mobile(models.Model): 
    name = models.CharField(max_length=100, null=False, blank=False) 
    def __str__(self): 
        return self.name 
class Category(models.Model): 
    mobile = models.ForeignKey( 
        Mobile, on_delete=models.SET_NULL, null=True, blank=True) 
    name = models.CharField(max_length=100, null=False, blank=False) 
    # image = models.ImageField(null=False, blank=False) 
    # description = models.TextField() 
    def __str__(self): 
        return self.name 
class Photo(models.Model): 
    mobile = models.ForeignKey( 
        Mobile, on_delete=models.SET_NULL, null=True, blank=True) 
    category = models.ForeignKey( 
        Category, on_delete=models.SET_NULL, null=True, blank=True) 
    image = models.ImageField(null=False, blank=False) 
    cname = models.CharField(max_length=100, null=False, blank=False, default="samsung")
    def __str__(self): 
        return self.cname

class Photocrop(models.Model): 
    mobile = models.ForeignKey( 
        Mobile, on_delete=models.SET_NULL, null=True, blank=True) 
    category = models.ForeignKey( 
        Category, on_delete=models.SET_NULL, null=True, blank=True) 
    photo = models.ForeignKey( 
        Photo, on_delete=models.SET_NULL, null=True, blank=True) 
    cimage = models.ImageField(null=False, blank=False) 
    def __str__(self): 
        return self.id

class Comments(models.Model):
    mobile = models.ForeignKey( 
        Mobile, on_delete=models.SET_NULL, null=True, blank=True) 
    category = models.ForeignKey( 
        Category, on_delete=models.SET_NULL, null=True, blank=True) 
    name = models.CharField(max_length=100, null=False, blank=False)
    comment = models.TextField(null=False,blank=False)
    def __str__(self):
        return self.name

