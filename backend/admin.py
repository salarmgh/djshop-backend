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

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline, CategoryInline]

admin_site = MyAdminSite()

admin_site.register(User, UserAdmin)
admin_site.register(Product, ProductAdmin)
admin_site.register(Image)
admin_site.register(Category)
admin_site.register(ProductAttribute)
admin_site.register(ProductAttributeValue)
admin_site.register(Carousel)
admin_site.register(Banner)
admin_site.register(LandingBanner)
admin_site.register(Order)
admin_site.register(Cart)

