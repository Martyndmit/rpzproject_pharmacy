from django.contrib import admin
from .models import Category, Symptom, Medicine, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_prescription', 'is_available']
    list_filter = ['is_available', 'is_prescription', 'category', 'created']
    list_editable = ['price', 'stock', 'is_available', 'is_prescription']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    filter_horizontal = ['symptoms']
    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'slug', 'category', 'manufacturer', 'price', 'stock', 'is_available')
        }),
        ('Медична інформація', {
            'fields': ('description', 'composition', 'dosage', 'contraindications', 'is_prescription', 'symptoms')
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['medicine']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name', 'first_name', 'phone', 'delivery_method', 'status', 'total_price', 'created']
    list_filter = ['status', 'delivery_method', 'created']
    list_editable = ['status']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    inlines = [OrderItemInline]
