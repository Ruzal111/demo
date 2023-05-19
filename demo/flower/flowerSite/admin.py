from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .models import Order, Category, Status, User, Product

class OrderAdmin(admin.ModelAdmin):
    list_display = ('date_create', 'user', 'status', 'amount')
    list_filter = ('status', )

class ProductAdmin(admin.ModelAdmin):
    def admin_image(self, obj):
        return mark_safe('<img src="%s" width=50/>' % obj.image.url)

    admin_image.allow_tags = True
    admin_image.short_description = 'Изображение'
    list_display = ('admin_image', 'name', 'category', 'country', 'color', 'price', 'amount')
    readonly_fields = ('admin_image', )


admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)


# Register your models here.
