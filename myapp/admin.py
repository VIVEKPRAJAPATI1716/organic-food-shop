from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *

class NoDeleteAdmin(admin.ModelAdmin):
    """
    Base admin that removes bulk delete and shows explicit
    edit/delete buttons per row.
    """
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def has_delete_permission(self, request, obj=None):
        # Allow delete, but only via explicit buttons
        return True

    def row_actions(self, obj):
        """
        Show small Edit (pencil) and Delete buttons on each row.
        """
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        change_url = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.pk])
        delete_url = reverse(f"admin:{app_label}_{model_name}_delete", args=[obj.pk])
        return format_html(
            '<div class="admin-row-actions">'
            '<a class="btn-admin-action btn-admin-edit" href="{}">'
            '<i class="fas fa-pen"></i></a>'
            '<a class="btn-admin-action btn-admin-delete" href="{}">'
            '<i class="fas fa-trash"></i></a>'
            '</div>',
            change_url,
            delete_url,
        )

    row_actions.short_description = "Actions"


# Register standard User model for easy management
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin, NoDeleteAdmin):
    """
    Standard Django UserAdmin with our custom row actions.
    """
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_superuser", "row_actions")
    
    def get_list_display(self, request):
        return self.list_display


@admin.register(Order)
class OrderAdminget(NoDeleteAdmin):
    list_display = ("id", "total_amount", "address", "order_date", "order", "row_actions")
    search_fields = ("id", "user__first_name", "user__last_name", "user__email", "order", "payment_method")


@admin.register(Category)
class CategoryAdminget(NoDeleteAdmin):
    list_display = ('id', "cat_name", "row_actions")
    search_fields = ("cat_name",)


@admin.register(Product)
class ProductAdminget(NoDeleteAdmin):
    list_display = ("id", "product_image", "description",
                    "price", "product_name", "cat_name", "row_actions")
    search_fields = ("product_name", "cat_name__cat_name", "description")


@admin.register(Cart)
class CartAdminget(NoDeleteAdmin):
    list_display = ("id", "user", "prod_name", "qty", "price", "status", "row_actions")
    search_fields = ("user__email", "user__first_name", "prod_name__product_name")


@admin.register(Feedback)
class FeedbackAdminget(NoDeleteAdmin):
    list_display = ("name", "email", "contact", "subject", "comment", "row_actions")
    search_fields = ("name", "email", "subject")


@admin.register(Register)
class RegisterAdminget(NoDeleteAdmin):
    list_display = ("id", "first_name", "last_name", "email", "row_actions")
    search_fields = ("first_name", "last_name", "email")


@admin.register(Address)
class AddressAdminget(NoDeleteAdmin):
    list_display = ("id", "user", "first_name", "city", "state", "postcode", "row_actions")
    search_fields = ("user__email", "first_name", "last_name", "city", "state")


@admin.register(Coupon)
class CouponAdmin(NoDeleteAdmin):
    list_display = ("code", "discount_percentage", "valid_from", "valid_to", "active", "row_actions")
    search_fields = ("code",)