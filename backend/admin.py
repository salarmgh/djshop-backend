from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from .models import *

class MyAdminSite(AdminSite):
    site_header = 'Anemone'
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        urls += [
            path('my_view/', self.admin_view(self.my_view))
        ]
        return urls

    def my_view(self, request):
        return HttpResponse("Hello!")

class ImageInline(admin.StackedInline):
    model = Image
    extra = 5

class CategoryInline(admin.StackedInline):
    model = Category.products.through
    verbose_name = "Categories"
    verbose_name_plural = "Categories"
    extra = 3

#class AttributeInline(admin.StackedInline):
#    model = Attribute.variants.through
#    verbose_name = "Attributes"
#    verbose_name_plural = "Attribute"
#    extra = 3

#class ProductAdmin(admin.ModelAdmin):
#    inlines = [ImageInline, CategoryInline, AttributeInline]

admin_site = MyAdminSite()

admin_site.register(User)
#admin_site.register(Product, ProductAdmin)
admin_site.register(Image)
admin_site.register(Category)
admin_site.register(Attribute)
admin_site.register(AttributeValue)
admin_site.register(Carousel)
admin_site.register(Banner)
admin_site.register(LandingBanner)
admin_site.register(Order)
admin_site.register(Cart)
admin_site.register(Variant)
admin_site.register(Product)

