from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from .models import *
from django.forms import ModelForm, PasswordInput, CharField
from django.utils.safestring import mark_safe


class AdminSite(AdminSite):
    site_header = 'Anemone'
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()

        return urls

    
class AddressInline(admin.StackedInline):
    model = Address
    extra = 1


class ImageInline(admin.StackedInline):
    model = Image
    extra = 3

class ProductAttributeInline(admin.StackedInline):
    model = Product.attributes.through
    extra = 3
    verbose_name = "Attributes"
    verbose_name_plural = "Attributes"


class ProductVariantsInline(admin.StackedInline):
    model = Variant
    extra = 3
    verbose_name = "Variants"
    verbose_name_plural = "Variants"
    
class ProductCategoryInline(admin.StackedInline):
    model = Product.categories.through
    extra = 1
    verbose_name = "Categories"
    verbose_name_plural = "Categories"


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'number', 'groups', 'password', 'is_active', 'is_superuser',)

    
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    inlines = [AddressInline]
    readonly_fields=('last_login', 'date_joined',)
    
    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


class ProductForm(ModelForm):
    url = CharField()
    
    class Meta:
        model = Product
        fields = ('title', 'description', 'featured',)


class ProductAdmin(admin.ModelAdmin):
    def url(self, obj):
        return mark_safe('<a href="/products/{}/">{}</a>'.format(obj.slug, obj.title))


    inlines = [ProductAttributeInline, ProductVariantsInline, ProductCategoryInline]
    form = ProductForm
    readonly_fields=('created_at','url',)

    
admin_site = AdminSite()

admin_site.register(User, UserAdmin)
admin_site.register(Product, ProductAdmin)

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

