from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from .models import *
from django.forms import ModelForm, PasswordInput, CharField, Form, BooleanField, Textarea, EmailField
from django.utils.safestring import mark_safe
from django.forms.models import BaseInlineFormSet
from django.contrib.admin.options import flatten_fieldsets


class AdminSite(AdminSite):
    site_header = 'Anemone'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()

        return urls


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1


class CategoryAttributeInline(admin.StackedInline):
    model = Category.attributes.through
    verbose_name = "Attributes"
    verbose_name_plural = "Attributes"
    extra = 3


class ImageInline(admin.StackedInline):
    model = Image
    extra = 3


class ProductVariantsForm(ModelForm):
    def url(self, obj):
        return mark_safe('<a href="/products/{}/">{}</a>'.format(obj.slug, obj.title))

    readonly_fields = ('url',)

    class Meta:
        model = Variant
        fields = ('name', 'attribute_values', 'product',
                  'price', 'images', 'featured',)


class ProductVariantsInline(admin.StackedInline):
    model = Variant
    form = ProductVariantsForm
    extra = 3
    verbose_name = "Variants"
    verbose_name_plural = "Variants"


class AttributeValueInline(admin.StackedInline):
    model = AttributeValue
    extra = 3
    verbose_name = "Attributes"
    verbose_name_plural = "Attribute"


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'number', 'groups', 'password', 'is_active', 'is_superuser',)


class UserAdmin(admin.ModelAdmin):
    form = UserForm
    inlines = [AddressInline]
    readonly_fields = ('last_login', 'date_joined',)

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'category',)


class CategoryForm(ModelForm):
    url = CharField()

    class Meta:
        model = Category
        fields = ('name', 'image',)


class ProductAdmin(admin.ModelAdmin):
    #    def url(self, obj):
    #        return mark_safe('<a href="/products/{}/">{}</a>'.format(obj.slug, obj.title))

    inlines = [ProductVariantsInline]
    form = ProductForm
    readonly_fields = ('created_at',)


class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]


class CategoryAdmin(admin.ModelAdmin):
    def url(self, obj):
        return mark_safe('<a href="/categories/{}/">{}</a>'.format(obj.slug, obj.name))

    inlines = [CategoryAttributeInline]
    form = CategoryForm
    readonly_fields = ('url',)

    class Meta:
        model = Category


admin_site = AdminSite()

admin_site.register(User, UserAdmin)
admin_site.register(Product, ProductAdmin)
# admin_site.register(Product)
admin_site.register(Attribute, AttributeAdmin)
admin_site.register(Category, CategoryAdmin)

admin_site.register(AttributeValue)
admin_site.register(Carousel)
admin_site.register(Banner)
admin_site.register(LandingBanner)
admin_site.register(Order)
admin_site.register(Cart)
admin_site.register(Variant)
admin_site.register(Image)
#admin_site.register(Category, CustomAdmin)
