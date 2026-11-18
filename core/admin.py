from django.contrib import admin

from .models import Category, Movement, Product, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'current_quantity', 'minimum_stock', 'is_active')
    search_fields = ('name',)
    list_filter = ('category', 'is_active')


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('occurred_at', 'product', 'type', 'quantity', 'reason', 'user')
    list_filter = ('type', 'reason')
    search_fields = ('product__name', 'user__username')
    readonly_fields = ('product', 'user', 'type', 'quantity', 'reason', 'occurred_at', 'notes')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(UserProfile)

# Register your models here.
