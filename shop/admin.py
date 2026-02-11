from django.contrib import admin
from .models import Category, Product, Customer, Cart, CartItem, Address, UserProfile, Wishlist, WishlistItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    list_filter = ('category', 'created_at', 'price')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'category', 'price')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('get_customer_name', 'user', 'phone_number', 'city', 'created_at')
    list_filter = ('created_at', 'country', 'state')
    search_fields = ('user__username', 'user__email', 'phone_number', 'address')
    readonly_fields = ('user', 'created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone_number',)
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_customer_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_customer_name.short_description = 'Customer Name'


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'added_at', 'updated_at')
    fields = ('product', 'quantity', 'added_at', 'updated_at')
    can_delete = True


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_items', 'get_total_price', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user', 'created_at', 'updated_at')
    inlines = [CartItemInline]
    fieldsets = (
        ('Cart Information', {
            'fields': ('user',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'

    def get_total_price(self, obj):
        return f"${obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'get_total_price', 'added_at')
    list_filter = ('added_at', 'updated_at', 'cart__user')
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ('cart', 'product', 'added_at', 'updated_at')
    fieldsets = (
        ('Cart Item Information', {
            'fields': ('cart', 'product', 'quantity')
        }),
        ('Metadata', {
            'fields': ('added_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_total_price(self, obj):
        return f"${obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('get_customer_name', 'user', 'address', 'city', 'country', 'created_at')
    list_filter = ('country', 'city', 'created_at')
    search_fields = ('user__username', 'user__email', 'first_name', 'last_name', 'address', 'city')
    readonly_fields = ('user', 'created_at', 'updated_at')
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'first_name', 'last_name', 'email')
        }),
        ('Address Details', {
            'fields': ('address', 'address2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Contact', {
            'fields': ('phone',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_customer_name.short_description = 'Name'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'user', 'gender', 'phone_number', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    readonly_fields = ('user', 'created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'profile_picture')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'bio')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'country_code')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = 'Name'


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0
    fields = ('product', 'added_at')
    readonly_fields = ('added_at',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'user', 'get_items_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('user', 'created_at', 'updated_at')
    inlines = [WishlistItemInline]
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = 'User'
    
    def get_items_count(self, obj):
        return obj.items.count()
    get_items_count.short_description = 'Items in Wishlist'


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('get_product_name', 'get_user_name', 'added_at')
    list_filter = ('added_at', 'wishlist__user')
    search_fields = ('product__name', 'wishlist__user__username', 'wishlist__user__email')
    readonly_fields = ('added_at',)
    fieldsets = (
        ('Item Information', {
            'fields': ('wishlist', 'product')
        }),
        ('Metadata', {
            'fields': ('added_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = 'Product'
    
    def get_user_name(self, obj):
        return obj.wishlist.user.get_full_name() or obj.wishlist.user.username
    get_user_name.short_description = 'User'
