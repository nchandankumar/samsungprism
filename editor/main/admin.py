from django.contrib import admin
from .models import Mobile,Category, Photo, Photocrop
# Register your models here.
admin.site.register(Mobile)
admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(Photocrop)