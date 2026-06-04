from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import *

# =========================================================
# COMMON HELPERS
# =========================================================

def image_thumb(obj, field_name, width=48, height=48, radius=10):
    image = getattr(obj, field_name, None)

    if image:
        try:
            return format_html(
                '<img src="{}" style="width:{}px;height:{}px;border-radius:{}px;object-fit:cover;border:1px solid #e5e7eb;" />',
                image.url,
                width,
                height,
                radius,
            )
        except Exception:
            return "Image not found"

    return format_html(
        '<div style="width:{}px;height:{}px;border-radius:{}px;background:#e5e7eb;display:flex;align-items:center;justify-content:center;font-weight:800;color:#475569;">-</div>',
        width,
        height,
        radius,
    )


def badge(text, color="#64748b"):
    return format_html(
        '<span style="background:{};color:white;padding:4px 10px;border-radius:999px;font-weight:800;font-size:12px;white-space:nowrap;">{}</span>',
        color,
        text,
    )


# =========================================================
# MASTER DATA
# =========================================================

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "state")
    list_filter = ("state",)
    search_fields = ("name", "state__name")
    ordering = ("state__name", "name")


# =========================================================
# USER PROFILE / TARGETS
# =========================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "profile_photo",
        "user",
        "employee_code",
        "role",
        "manager",
        "phone",
        "salary_amount",
        "state",
        "district",
        "bike_ta_per_km",
        "car_ta_per_km",
        "daily_da_amount",
        "created_at",
    )
    list_filter = (
        "role",
        "state",
        "district",
        "pf_applicable",
        "insurance_applicable",
        "work_monday",
        "work_tuesday",
        "work_wednesday",
        "work_thursday",
        "work_friday",
        "work_saturday",
        "work_sunday",
        "created_at",
    )
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "employee_code",
        "manager__username",
        "manager__first_name",
        "manager__last_name",
        "phone",
        "pan_number",
        "bank_account_number",
        "pf_uan_number",
        "insurance_policy_number",
        "state__name",
        "district__name",
    )
    readonly_fields = ("profile_photo_preview", "created_at")
    autocomplete_fields = ("user", "manager", "state", "district")
    ordering = ("-created_at",)

    fieldsets = (
        ("User Details", {
            "fields": (
                "user",
                "role",
                "employee_code",
                "manager",
                "profile_image",
                "profile_photo_preview",
            )
        }),
        ("Contact & Location", {
            "fields": (
                "phone",
                "address",
                "state",
                "district",
            )
        }),
        ("Salary & Target", {
            "fields": (
                "salary_amount",
                "manager_target_extra_percentage",
            )
        }),
        ("Payroll / Bank / PAN", {
            "fields": (
                "date_of_birth",
                "pan_number",
                "bank_name",
                "bank_account_number",
                "bank_ifsc_code",
                "bank_account_holder_name",
            )
        }),
        ("PF Details", {
            "fields": (
                "pf_applicable",
                "pf_uan_number",
                "pf_deduction_percentage",
            )
        }),
        ("Insurance Details", {
            "fields": (
                "insurance_applicable",
                "insurance_provider_name",
                "insurance_policy_number",
                "insurance_deduction_amount",
            )
        }),
        ("Duty & Work Week", {
            "fields": (
                "duty_start_time",
                "duty_end_time",
                "work_monday",
                "work_tuesday",
                "work_wednesday",
                "work_thursday",
                "work_friday",
                "work_saturday",
                "work_sunday",
            )
        }),
        ("TA / DA / Leave Settings", {
            "fields": (
                "bike_ta_per_km",
                "car_ta_per_km",
                "daily_da_amount",
                "paid_leaves_per_year",
                "sick_leaves_per_year",
                "other_leaves_per_year",
                "unpaid_leaves_per_year",
                "earned_extra_other_leaves",
            )
        }),
        ("System Info", {
            "fields": ("created_at",)
        }),
    )

    def profile_photo(self, obj):
        return image_thumb(obj, "profile_image", 42, 42, 50)

    profile_photo.short_description = "Photo"

    def profile_photo_preview(self, obj):
        if obj and obj.profile_image:
            try:
                return format_html(
                    '<img src="{}" style="width:160px;height:160px;border-radius:20px;object-fit:cover;border:1px solid #ddd;" />',
                    obj.profile_image.url,
                )
            except Exception:
                return "Image not found"
        return "No image uploaded"

    profile_photo_preview.short_description = "Profile Image Preview"


@admin.register(EmployeeYearlyTarget)
class EmployeeYearlyTargetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "employee",
        "employee_role",
        "employee_manager",
        "year",
        "target_amount",
        "achieved_amount",
        "balance_amount",
        "target_percentage",
        "created_at",
    )
    list_filter = ("year", "employee__profile__role", "employee__profile__manager", "created_at")
    search_fields = (
        "employee__username",
        "employee__first_name",
        "employee__last_name",
        "employee__email",
    )
    autocomplete_fields = ("employee",)
    ordering = ("-year", "employee__username")

    def employee_role(self, obj):
        profile = getattr(obj.employee, "profile", None)
        return profile.get_role_display() if profile else "-"

    employee_role.short_description = "Role"

    def employee_manager(self, obj):
        profile = getattr(obj.employee, "profile", None)
        return profile.manager if profile and profile.manager else "-"

    employee_manager.short_description = "Manager"

    def target_percentage(self, obj):
        percent = obj.achieved_percentage
        color = "#16a34a" if percent >= 100 else "#f59e0b" if percent >= 50 else "#dc2626"
        return format_html('<strong style="color:{};">{}%</strong>', color, percent)

    target_percentage.short_description = "Reached"


# =========================================================
# DEALERS
# =========================================================

class DealerApprovalHistoryInline(admin.TabularInline):
    model = DealerApprovalHistory
    extra = 0
    readonly_fields = ("action", "performed_by", "remarks", "created_at")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.action(description="Approve selected dealers and activate login")
def approve_selected_dealers(modeladmin, request, queryset):
    count = 0
    for dealer in queryset.exclude(approval_status="APPROVED"):
        dealer.activate_dealer_login()
        DealerApprovalHistory.objects.create(
            dealer=dealer,
            action="ASM_APPROVED",
            performed_by=request.user,
            remarks="Approved from admin panel.",
        )
        count += 1
    modeladmin.message_user(request, f"{count} dealer(s) approved and login activated successfully.")


@admin.action(description="Reject selected dealers")
def reject_selected_dealers(modeladmin, request, queryset):
    count = 0
    for dealer in queryset.exclude(approval_status="REJECTED"):
        dealer.reject_dealer(request.user, "Rejected from admin panel.")
        DealerApprovalHistory.objects.create(
            dealer=dealer,
            action="REJECTED",
            performed_by=request.user,
            remarks="Rejected from admin panel.",
        )
        count += 1
    modeladmin.message_user(request, f"{count} dealer(s) rejected successfully.")


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dealer_photo",
        "dealer_code",
        "firm_name",
        "owner_name",
        "phone",
        "email",
        "gst_number",
        "firm_type",
        "deposit_amount",
        "cheque_number",
        "flag_badge",
        "yearly_target_amount",
        "achieved_amount",
        "target_percentage",
        "approval_badge",
        "login_status",
        "concerned_asm",
        "created_by_sales_officer",
        "created_at",
    )
    list_filter = (
        "flag",
        "firm_type",
        "deposit_mode",
        "approval_status",
        "is_active",
        "state",
        "district",
        "created_at",
    )
    search_fields = (
        "dealer_code",
        "firm_name",
        "owner_name",
        "phone",
        "email",
        "gst_number",
        "license_number",
        "cheque_number",
        "user__username",
        "created_by_sales_officer__username",
        "concerned_asm__username",
    )
    readonly_fields = (
        "dealer_photo_preview",
        "created_at",
        "updated_at",
        "asm_approved_at",
        "regional_manager_approved_at",
        "state_head_approved_at",
        "rejected_at",
        "target_percentage",
        "login_status",
    )
    autocomplete_fields = (
        "user",
        "state",
        "district",
        "created_by_sales_officer",
        "concerned_asm",
        "forwarded_regional_manager",
        "forwarded_state_head",
        "asm_approved_by",
        "regional_manager_approved_by",
        "state_head_approved_by",
        "rejected_by",
    )
    ordering = ("-created_at",)
    actions = (approve_selected_dealers, reject_selected_dealers)
    inlines = [DealerApprovalHistoryInline]

    fieldsets = (
        ("Dealer Login", {
            "fields": ("user", "is_active", "login_status")
        }),
        ("Dealer Owner Details", {
            "fields": ("dealer_code", "dealer_image", "dealer_photo_preview", "owner_name", "phone", "email", "owner_address")
        }),
        ("Firm Details", {
            "fields": ("firm_name", "gst_number", "firm_address", "state", "district", "firm_type", "license_number")
        }),
        ("Deposit / Cheque Details", {
            "fields": ("deposit_amount", "deposit_mode", "cheque_number")
        }),
        ("Flag & Target", {
            "fields": ("flag", "yearly_target_amount", "achieved_amount", "target_percentage")
        }),
        ("Approval Flow", {
            "fields": ("approval_status", "created_by_sales_officer", "concerned_asm", "forwarded_regional_manager", "forwarded_state_head")
        }),
        ("Approved By", {
            "fields": (
                "asm_approved_by",
                "asm_approved_at",
                "regional_manager_approved_by",
                "regional_manager_approved_at",
                "state_head_approved_by",
                "state_head_approved_at",
            )
        }),
        ("Rejection Details", {
            "fields": ("rejected_by", "rejected_at", "rejection_reason")
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        role = getattr(getattr(request.user, "profile", None), "role", None)
        can_edit_cheque = request.user.is_superuser or role in ["ADMIN", "ACCOUNTANT"]
        if not can_edit_cheque:
            readonly_fields.extend(["deposit_amount", "deposit_mode", "cheque_number"])
        return readonly_fields

    def dealer_photo(self, obj):
        return image_thumb(obj, "dealer_image", 46, 46, 14)

    dealer_photo.short_description = "Photo"

    def dealer_photo_preview(self, obj):
        if obj and obj.dealer_image:
            try:
                return format_html(
                    '<img src="{}" style="width:160px;height:160px;border-radius:22px;object-fit:cover;border:1px solid #ddd;" />',
                    obj.dealer_image.url,
                )
            except Exception:
                return "Image not found"
        return "No dealer image uploaded"

    dealer_photo_preview.short_description = "Dealer Image Preview"

    def flag_badge(self, obj):
        colors = {"GREEN": "#16a34a", "ORANGE": "#f59e0b", "RED": "#dc2626"}
        return badge(obj.get_flag_display(), colors.get(obj.flag, "#64748b"))

    flag_badge.short_description = "Flag"

    def approval_badge(self, obj):
        colors = {
            "PENDING_ASM": "#f59e0b",
            "FORWARDED_RM": "#2563eb",
            "FORWARDED_STATE_HEAD": "#7c3aed",
            "APPROVED": "#16a34a",
            "REJECTED": "#dc2626",
        }
        return badge(obj.get_approval_status_display(), colors.get(obj.approval_status, "#64748b"))

    approval_badge.short_description = "Approval"

    def login_status(self, obj):
        if obj.user and obj.user.is_active and obj.is_active and obj.approval_status == "APPROVED":
            return format_html('<strong style="color:#16a34a;">Active</strong>')
        return format_html('<strong style="color:#dc2626;">Blocked</strong>')

    login_status.short_description = "Login Status"

    def target_percentage(self, obj):
        percent = obj.target_achieved_percentage
        color = "#16a34a" if percent >= 100 else "#f59e0b" if percent >= 50 else "#dc2626"
        return format_html('<strong style="color:{};">{}%</strong>', color, percent)

    target_percentage.short_description = "Target Reached"


@admin.register(DealerApprovalHistory)
class DealerApprovalHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "dealer", "action", "performed_by", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("dealer__firm_name", "dealer__owner_name", "performed_by__username", "remarks")
    readonly_fields = ("dealer", "action", "performed_by", "remarks", "created_at")
    autocomplete_fields = ("dealer", "performed_by")
    ordering = ("-created_at",)


# =========================================================
# WAREHOUSE
# =========================================================

@admin.action(description="Mark selected warehouses as active")
def mark_warehouses_active(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"{updated} warehouse(s) marked as active.")


@admin.action(description="Mark selected warehouses as inactive")
def mark_warehouses_inactive(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, f"{updated} warehouse(s) marked as inactive.")


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "state", "district", "warehouse_manager", "status_badge", "created_at")
    list_filter = ("state", "district", "is_active", "created_at")
    search_fields = (
        "name",
        "state__name",
        "district__name",
        "warehouse_manager__username",
        "warehouse_manager__first_name",
        "warehouse_manager__last_name",
    )
    readonly_fields = ("created_at",)
    autocomplete_fields = ("state", "district", "warehouse_manager")
    ordering = ("state__name", "district__name", "name")
    actions = (mark_warehouses_active, mark_warehouses_inactive)

    def status_badge(self, obj):
        return badge("Active", "#16a34a") if obj.is_active else badge("Inactive", "#dc2626")

    status_badge.short_description = "Status"


# =========================================================
# FARMER MEETS
# =========================================================

class FarmerMeetApprovalHistoryInline(admin.TabularInline):
    model = FarmerMeetApprovalHistory
    extra = 0
    readonly_fields = ("action", "performed_by", "remarks", "created_at")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.action(description="Approve selected farmer meet requests to next level")
def approve_selected_farmer_meets(modeladmin, request, queryset):
    count = 0
    for meet in queryset.exclude(approval_status__in=["APPROVED", "REJECTED"]):
        old_status = meet.approval_status
        meet.approval_status = meet.get_next_status_after_approval()
        meet.save(update_fields=["approval_status"])
        FarmerMeetApprovalHistory.objects.create(
            farmer_meet=meet,
            action=f"Approved from {old_status} to {meet.approval_status}",
            performed_by=request.user,
            remarks="Approved from admin panel.",
        )
        count += 1
    modeladmin.message_user(request, f"{count} farmer meet request(s) moved to next approval level.")


@admin.action(description="Reject selected farmer meet requests")
def reject_selected_farmer_meets(modeladmin, request, queryset):
    count = 0
    for meet in queryset.exclude(approval_status="REJECTED"):
        meet.approval_status = "REJECTED"
        meet.rejected_by = request.user
        meet.rejected_at = timezone.now()
        meet.rejection_reason = "Rejected from admin panel."
        meet.save()
        FarmerMeetApprovalHistory.objects.create(
            farmer_meet=meet,
            action="Rejected",
            performed_by=request.user,
            remarks="Rejected from admin panel.",
        )
        count += 1
    modeladmin.message_user(request, f"{count} farmer meet request(s) rejected.")


@admin.register(FarmerMeetRequest)
class FarmerMeetRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "location",
        "meeting_date",
        "expected_farmer_count",
        "approval_badge",
        "created_by_mdo",
        "sales_officer",
        "asm",
        "regional_manager",
        "state_head",
        "created_at",
    )
    list_filter = ("approval_status", "meeting_date", "created_at")
    search_fields = (
        "title",
        "location",
        "description",
        "created_by_mdo__username",
        "sales_officer__username",
        "asm__username",
        "regional_manager__username",
        "state_head__username",
    )
    readonly_fields = ("created_at", "rejected_at")
    autocomplete_fields = ("created_by_mdo", "sales_officer", "asm", "regional_manager", "state_head", "rejected_by")
    ordering = ("-created_at",)
    actions = (approve_selected_farmer_meets, reject_selected_farmer_meets)
    inlines = [FarmerMeetApprovalHistoryInline]

    def approval_badge(self, obj):
        colors = {
            "PENDING_SALES_OFFICER": "#f59e0b",
            "PENDING_ASM": "#2563eb",
            "PENDING_REGIONAL_MANAGER": "#7c3aed",
            "PENDING_STATE_HEAD": "#9333ea",
            "APPROVED": "#16a34a",
            "REJECTED": "#dc2626",
        }
        return badge(obj.get_approval_status_display(), colors.get(obj.approval_status, "#64748b"))

    approval_badge.short_description = "Status"


@admin.register(FarmerMeetApprovalHistory)
class FarmerMeetApprovalHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "farmer_meet", "action", "performed_by", "created_at")
    list_filter = ("created_at",)
    search_fields = ("farmer_meet__title", "performed_by__username", "action", "remarks")
    readonly_fields = ("farmer_meet", "action", "performed_by", "remarks", "created_at")
    autocomplete_fields = ("farmer_meet", "performed_by")
    ordering = ("-created_at",)


# =========================================================
# PRODUCTS / SCHEMES / STICKERS
# =========================================================

class CategoryPaymentRuleInline(admin.TabularInline):
    model = CategoryPaymentRule
    extra = 1


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at",)
    ordering = ("name",)
    inlines = [CategoryPaymentRuleInline]


@admin.register(CategoryPaymentRule)
class CategoryPaymentRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "rule_type", "title", "discount_percent", "from_day", "to_day", "is_active")
    list_filter = ("rule_type", "is_active", "category")
    search_fields = ("category__name", "title")
    autocomplete_fields = ("category",)
    ordering = ("category__name", "rule_type", "from_day")


class ProductPackSizeInline(admin.TabularInline):
    model = ProductPackSize
    extra = 1
    fields = (
        "warehouse",
        "pack_size",
        "unit",
        "packing_type",
        "units_per_box",
        "mrp_per_unit",
        "sale_price_per_unit",
        "purchase_price_per_unit",
        "box_sale_price",
        "stock_boxes",
        "is_active",
    )
    autocomplete_fields = ("warehouse",)


class ProductSchemeInline(admin.TabularInline):
    model = ProductScheme
    extra = 0
    autocomplete_fields = ("pack_size",)


class ProductStickerSettingInline(admin.StackedInline):
    model = ProductStickerSetting
    extra = 0
    max_num = 1
    autocomplete_fields = ("pack_size",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_image", "name", "category", "hsn_number", "available_pack_count", "in_stock", "is_active", "created_at")
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("name", "hsn_number", "description", "category__name")
    readonly_fields = ("product_image_preview", "created_at", "available_pack_count", "in_stock")
    autocomplete_fields = ("category",)
    ordering = ("-created_at",)
    inlines = [ProductPackSizeInline, ProductSchemeInline, ProductStickerSettingInline]

    fieldsets = (
        ("Product", {
            "fields": ("category", "name", "image", "product_image_preview", "hsn_number", "description", "is_active")
        }),
        ("System", {
            "fields": ("available_pack_count", "in_stock", "created_at")
        }),
    )

    def product_image(self, obj):
        return image_thumb(obj, "image", 46, 46, 12)

    product_image.short_description = "Image"

    def product_image_preview(self, obj):
        if obj and obj.image:
            try:
                return format_html(
                    '<img src="{}" style="width:180px;height:180px;border-radius:18px;object-fit:cover;border:1px solid #ddd;" />',
                    obj.image.url,
                )
            except Exception:
                return "Image not found"
        return "No image uploaded"

    product_image_preview.short_description = "Product Image Preview"


@admin.register(ProductPackSize)
class ProductPackSizeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "warehouse",
        "display_pack",
        "display_box",
        "total_quantity_label",
        "mrp_per_unit",
        "sale_price_per_unit",
        "purchase_price_per_unit",
        "box_sale_price",
        "stock_boxes",
        "margin_percent",
        "is_active",
    )
    list_filter = ("unit", "packing_type", "is_active", "warehouse", "product__category")
    search_fields = ("product__name", "warehouse__name", "product__hsn_number")
    autocomplete_fields = ("product", "warehouse")
    ordering = ("product__name", "pack_size")


@admin.register(ProductStickerSetting)
class ProductStickerSettingAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "pack_size", "width_mm", "height_mm", "copies", "show_barcode", "show_qr", "updated_at")
    list_filter = ("show_barcode", "show_qr", "updated_at")
    search_fields = ("product__name", "company_name", "barcode_value", "batch_no")
    autocomplete_fields = ("product", "pack_size")
    readonly_fields = ("updated_at",)


@admin.register(ProductScheme)
class ProductSchemeAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "pack_size", "scheme_name", "scheme_type", "min_boxes", "discount_percent", "free_boxes", "valid_from", "valid_to", "is_active")
    list_filter = ("scheme_type", "is_active", "valid_from", "valid_to", "product__category")
    search_fields = ("product__name", "scheme_name")
    autocomplete_fields = ("product", "pack_size")
    ordering = ("product__name", "min_boxes")


# =========================================================
# CARTS
# =========================================================

class DealerCartItemInline(admin.TabularInline):
    model = DealerCartItem
    extra = 0
    autocomplete_fields = ("product_pack",)


@admin.register(DealerCart)
class DealerCartAdmin(admin.ModelAdmin):
    list_display = ("id", "dealer", "total_amount", "created_at", "updated_at")
    search_fields = ("dealer__username", "dealer__email", "dealer__dealer_profile__firm_name")
    readonly_fields = ("total_amount", "created_at", "updated_at")
    autocomplete_fields = ("dealer",)
    inlines = [DealerCartItemInline]


@admin.register(DealerCartItem)
class DealerCartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product_pack", "quantity_boxes", "total_units", "total_amount", "created_at")
    search_fields = ("cart__dealer__username", "product_pack__product__name")
    autocomplete_fields = ("cart", "product_pack")
    readonly_fields = ("total_units", "total_amount", "created_at")


# =========================================================
# ORDERS / INVOICES / DISPATCH
# =========================================================

class DealerOrderItemInline(admin.TabularInline):
    model = DealerOrderItem
    extra = 0
    autocomplete_fields = ("product_pack",)
    fields = (
        "product_pack",
        "product_name",
        "pack_label",
        "quantity_boxes",
        "total_units",
        "unit_name",
        "price_per_unit",
        "taxable_amount",
        "gst_percent",
        "gst_amount",
        "total_amount",
        "hsn_code",
        "batch_no",
        "mfg_date",
        "expiry_date",
        "warehouse_checked",
        "accountant_checked",
    )


class DealerOrderApprovalLogInline(admin.TabularInline):
    model = DealerOrderApprovalLog
    extra = 0
    readonly_fields = ("user", "role", "action", "note", "created_at")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(DealerOrder)
class DealerOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dealer",
        "dealer_flag_badge",
        "status_badge",
        "concerned_sales_officer",
        "concerned_asm",
        "concerned_rsm",
        "warehouse_manager",
        "subtotal_amount",
        "gst_amount",
        "total_amount",
        "placed_at",
    )
    list_filter = ("dealer_flag", "status", "placed_at", "updated_at")
    search_fields = (
        "id",
        "dealer__firm_name",
        "dealer__dealer_code",
        "dealer_user__username",
        "concerned_sales_officer__username",
        "concerned_asm__username",
        "concerned_rsm__username",
        "warehouse_manager__username",
    )
    readonly_fields = (
        "placed_at",
        "updated_at",
        "sales_approved_at",
        "asm_approved_at",
        "rsm_approved_at",
        "accountant_order_approved_at",
        "warehouse_reviewed_at",
        "invoice_released_at",
        "dispatched_at",
        "delivered_at",
    )
    autocomplete_fields = (
        "dealer",
        "dealer_user",
        "concerned_sales_officer",
        "concerned_asm",
        "concerned_rsm",
        "warehouse_manager",
        "rejected_by",
    )
    ordering = ("-placed_at",)
    inlines = [DealerOrderItemInline, DealerOrderApprovalLogInline]

    def dealer_flag_badge(self, obj):
        colors = {"GREEN": "#16a34a", "ORANGE": "#f59e0b", "RED": "#dc2626"}
        return badge(obj.get_dealer_flag_display(), colors.get(obj.dealer_flag, "#64748b"))

    dealer_flag_badge.short_description = "Flag"

    def status_badge(self, obj):
        colors = {
            "PLACED": "#64748b",
            "REJECTED": "#dc2626",
            "SALES_APPROVAL": "#f59e0b",
            "ASM_APPROVAL": "#2563eb",
            "RSM_APPROVAL": "#7c3aed",
            "ACCOUNTANT_ORDER_APPROVAL": "#9333ea",
            "WAREHOUSE_REVIEW": "#0ea5e9",
            "ACCOUNTANT_INVOICE_REVIEW": "#8b5cf6",
            "INVOICE_RELEASED": "#16a34a",
            "DISPATCH_PENDING": "#d97706",
            "DISPATCHED": "#0284c7",
            "DELIVERED": "#15803d",
        }
        return badge(obj.get_status_display(), colors.get(obj.status, "#64748b"))

    status_badge.short_description = "Status"


@admin.register(DealerOrderItem)
class DealerOrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product_name",
        "pack_label",
        "quantity_boxes",
        "total_units",
        "unit_name",
        "price_per_unit",
        "gst_percent",
        "gst_amount",
        "total_amount",
        "hsn_code",
        "batch_no",
        "mfg_date",
        "expiry_date",
        "warehouse_checked",
        "accountant_checked",
    )
    list_filter = ("warehouse_checked", "accountant_checked", "gst_percent")
    search_fields = ("order__id", "product_name", "hsn_code", "batch_no")
    autocomplete_fields = ("order", "product_pack")


@admin.register(DealerOrderApprovalLog)
class DealerOrderApprovalLogAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "user", "role", "action", "created_at")
    list_filter = ("action", "role", "created_at")
    search_fields = ("order__id", "user__username", "role", "note")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("order", "user")
    ordering = ("-created_at",)


@admin.register(InvoiceNumberSequence)
class InvoiceNumberSequenceAdmin(admin.ModelAdmin):
    list_display = ("id", "financial_year", "last_number")
    search_fields = ("financial_year",)


class DealerInvoicePaymentInline(admin.TabularInline):
    model = DealerInvoicePayment
    extra = 0
    readonly_fields = ("created_at",)
    autocomplete_fields = ("created_by",)


class DealerInvoiceEditHistoryInline(admin.TabularInline):
    model = DealerInvoiceEditHistory
    extra = 0
    readonly_fields = ("edited_by", "action", "old_values", "new_values", "note", "created_at")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(DealerInvoice)
class DealerInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "invoice_number",
        "financial_year",
        "order",
        "dealer_name",
        "invoice_date",
        "total_amount",
        "discount_amount",
        "final_payable_amount",
        "return_credit_amount",
        "net_payable_after_return",
        "paid_amount",
        "balance_amount",
        "is_converted_to_sales",
        "released_at",
    )
    list_filter = ("financial_year", "invoice_date", "is_converted_to_sales", "released_at", "last_payment_date")
    search_fields = ("invoice_number", "order__id", "order__dealer__firm_name", "place_of_supply")
    readonly_fields = ("released_at", "sales_converted_at", "balance_amount")
    autocomplete_fields = ("order", "released_by", "sales_converted_by")
    ordering = ("-invoice_date", "-id")
    inlines = [DealerInvoicePaymentInline, DealerInvoiceEditHistoryInline]

    def dealer_name(self, obj):
        return obj.order.dealer.firm_name if obj.order and obj.order.dealer else "-"

    dealer_name.short_description = "Dealer"


@admin.register(DealerInvoicePayment)
class DealerInvoicePaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "invoice",
        "payment_status",
        "payment_mode",
        "payment_date",
        "payment_amount",
        "discount_type",
        "discount_percent",
        "discount_amount",
        "net_received_amount",
        "balance_after_payment",
        "created_by",
        "created_at",
    )
    list_filter = ("payment_status", "payment_mode", "discount_type", "payment_date", "created_at")
    search_fields = (
        "invoice__invoice_number",
        "upi_reference_number",
        "bank_transaction_number",
        "cheque_number",
        "category_rule_note",
        "selected_category_rule_name",
    )
    readonly_fields = ("created_at",)
    autocomplete_fields = ("invoice", "created_by")
    ordering = ("-payment_date", "-created_at")


@admin.register(DealerInvoiceEditHistory)
class DealerInvoiceEditHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "invoice", "action", "edited_by", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("invoice__invoice_number", "action", "note", "edited_by__username")
    readonly_fields = ("invoice", "edited_by", "action", "old_values", "new_values", "note", "created_at")
    autocomplete_fields = ("invoice", "edited_by")
    ordering = ("-created_at",)


@admin.register(DealerDispatch)
class DealerDispatchAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "transport_type", "vehicle_name", "vehicle_number", "driver_name", "driver_phone", "dispatch_date", "created_by", "created_at")
    list_filter = ("transport_type", "dispatch_date", "created_at")
    search_fields = ("order__id", "vehicle_name", "vehicle_number", "driver_name", "driver_phone", "other_transport_tracking_id")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("order", "created_by")
    ordering = ("-dispatch_date", "-created_at")


# =========================================================
# ACCOUNTS
# =========================================================

@admin.register(CompanyAccount)
class CompanyAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "account_name", "bank_name", "account_number", "ifsc_code", "current_balance", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("account_name", "bank_name", "branch_name", "account_number", "ifsc_code", "account_holder_name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("account_name",)


@admin.register(CompanyPaymentIn)
class CompanyPaymentInAdmin(admin.ModelAdmin):
    list_display = ("id", "payment_date", "account", "source_type", "dealer", "payment_mode", "amount", "created_by", "created_at")
    list_filter = ("source_type", "payment_mode", "payment_date", "created_at")
    search_fields = ("dealer__firm_name", "reference_number", "cheque_number", "reason", "account__account_name")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("account", "dealer", "created_by")
    ordering = ("-payment_date", "-created_at")


@admin.register(CompanyPaymentOut)
class CompanyPaymentOutAdmin(admin.ModelAdmin):
    list_display = ("id", "payment_date", "account", "expense_type", "payee_name", "payment_mode", "amount", "created_by", "created_at")
    list_filter = ("expense_type", "payment_mode", "payment_date", "created_at")
    search_fields = ("payee_name", "reference_number", "cheque_number", "reason", "account__account_name")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("account", "created_by")
    ordering = ("-payment_date", "-created_at")


# =========================================================
# SALES RETURN / CREDIT NOTE
# =========================================================

@admin.register(CreditNoteNumberSequence)
class CreditNoteNumberSequenceAdmin(admin.ModelAdmin):
    list_display = ("id", "financial_year", "last_number")
    search_fields = ("financial_year",)


class SalesReturnCreditNoteItemInline(admin.TabularInline):
    model = SalesReturnCreditNoteItem
    extra = 0
    autocomplete_fields = ("order_item", "product_pack")


@admin.register(SalesReturnCreditNote)
class SalesReturnCreditNoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "credit_note_number",
        "dealer",
        "invoice",
        "return_date",
        "subtotal_amount",
        "gst_amount",
        "grand_total",
        "status",
        "show_to_dealer",
        "created_by",
        "created_at",
    )
    list_filter = ("status", "show_to_dealer", "return_date", "created_at")
    search_fields = ("credit_note_number", "dealer__firm_name", "invoice__invoice_number", "reason")
    readonly_fields = ("credit_note_number", "created_at", "updated_at")
    autocomplete_fields = ("dealer", "invoice", "order", "created_by", "updated_by")
    ordering = ("-return_date", "-id")
    inlines = [SalesReturnCreditNoteItemInline]


@admin.register(SalesReturnCreditNoteItem)
class SalesReturnCreditNoteItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "credit_note",
        "product_name_snapshot",
        "pack_label_snapshot",
        "sold_quantity_boxes",
        "return_quantity_boxes",
        "total_return_units",
        "price_per_box",
        "gst_percent",
        "gst_amount",
        "total_amount",
    )
    list_filter = ("gst_percent",)
    search_fields = ("credit_note__credit_note_number", "product_name_snapshot", "hsn_code", "batch_no")
    autocomplete_fields = ("credit_note", "order_item", "product_pack")


# =========================================================
# ATTENDANCE / LEAVES / PAYROLL
# =========================================================

class EmployeeGPSTrackInline(admin.TabularInline):
    model = EmployeeGPSTrack
    extra = 0
    readonly_fields = ("latitude", "longitude", "recorded_at")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(EmployeeAttendance)
class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "employee",
        "attendance_date",
        "vehicle_type",
        "clock_in_at",
        "clock_out_at",
        "clock_in_odometer_reading",
        "clock_out_odometer_reading",
        "system_distance_km",
        "manager_approved_km",
        "ta_amount",
        "da_amount",
        "total_claim_amount",
        "status_badge",
        "created_at",
    )
    list_filter = ("status", "vehicle_type", "attendance_date", "created_at")
    search_fields = ("employee__username", "employee__first_name", "employee__last_name", "employee__email")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("employee", "manager_approved_by", "hr_approved_by", "released_by")
    ordering = ("-attendance_date", "-clock_in_at")
    inlines = [EmployeeGPSTrackInline]

    fieldsets = (
        ("Employee", {"fields": ("employee", "attendance_date", "status")}),
        ("Clock In", {"fields": ("clock_in_at", "clock_in_latitude", "clock_in_longitude", "clock_in_odometer_reading")}),
        ("Clock Out", {"fields": ("clock_out_at", "clock_out_latitude", "clock_out_longitude", "clock_out_odometer_reading")}),
        ("Vehicle / Claim", {
            "fields": (
                "vehicle_type",
                "public_vehicle_amount",
                "public_vehicle_bill",
                "system_distance_km",
                "manager_approved_km",
                "ta_rate_per_km",
                "ta_amount",
                "da_amount",
                "total_claim_amount",
            )
        }),
        ("Old Dealer Visit Fields", {
            "fields": ("dealers_connected_count", "dealer_visit_image_1", "dealer_visit_image_2"),
            "classes": ("collapse",),
        }),
        ("Manager Approval", {"fields": ("manager_approved_by", "manager_approved_at", "manager_remarks")}),
        ("HR Approval", {"fields": ("hr_approved_by", "hr_approved_at", "hr_remarks")}),
        ("Release", {"fields": ("released_by", "released_at", "release_remarks")}),
        ("System", {"fields": ("created_at",)}),
    )

    def status_badge(self, obj):
        colors = {
            "CLOCKED_IN": "#2563eb",
            "PENDING_MANAGER": "#f59e0b",
            "MANAGER_APPROVED": "#7c3aed",
            "HR_APPROVED": "#0ea5e9",
            "RELEASED": "#16a34a",
            "REJECTED": "#dc2626",
        }
        return badge(obj.get_status_display(), colors.get(obj.status, "#64748b"))

    status_badge.short_description = "Status"


@admin.register(EmployeeGPSTrack)
class EmployeeGPSTrackAdmin(admin.ModelAdmin):
    list_display = ("id", "attendance", "employee_name", "latitude", "longitude", "recorded_at")
    list_filter = ("recorded_at",)
    search_fields = ("attendance__employee__username", "attendance__employee__first_name", "attendance__employee__last_name")
    readonly_fields = ("recorded_at",)
    autocomplete_fields = ("attendance",)
    ordering = ("-recorded_at",)

    def employee_name(self, obj):
        return obj.attendance.employee if obj.attendance else "-"

    employee_name.short_description = "Employee"


@admin.register(EmployeeLeaveRequest)
class EmployeeLeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "leave_type", "day_type", "from_date", "to_date", "status", "salary_deduction_required", "deduction_days", "created_at")
    list_filter = ("leave_type", "day_type", "status", "salary_deduction_required", "from_date", "created_at")
    search_fields = ("employee__username", "employee__first_name", "employee__last_name", "reason", "manager_remarks")
    readonly_fields = ("created_at", "approved_at")
    autocomplete_fields = ("employee", "approved_by")
    ordering = ("-created_at",)


@admin.register(EmployeePayslip)
class EmployeePayslipAdmin(admin.ModelAdmin):
    list_display = ("id", "payslip_number", "employee", "month", "year", "gross_salary", "total_deductions", "net_salary", "status", "generated_at")
    list_filter = ("status", "month", "year", "generated_at", "released_at")
    search_fields = ("payslip_number", "employee__username", "employee__first_name", "employee__last_name", "employee_pan_number", "employee_bank_account_number")
    readonly_fields = ("gross_salary", "total_deductions", "net_salary", "generated_at", "released_at")
    autocomplete_fields = ("employee", "generated_by", "released_by")
    ordering = ("-year", "-month", "employee__username")

    fieldsets = (
        ("Payslip", {"fields": ("employee", "payslip_number", "month", "year", "status", "remarks")}),
        ("Salary", {"fields": ("basic_salary", "allowance_amount", "gross_salary")}),
        ("Deductions", {"fields": ("leave_deduction_amount", "other_deduction_amount", "pf_deduction_amount", "insurance_deduction_amount", "total_deductions", "net_salary")}),
        ("Employee Snapshot", {
            "fields": (
                "employee_dob",
                "employee_pan_number",
                "employee_bank_name",
                "employee_bank_account_number",
                "employee_bank_ifsc_code",
                "employee_bank_account_holder_name",
                "employee_pf_uan_number",
                "employee_pf_percentage",
                "employee_insurance_provider_name",
                "employee_insurance_policy_number",
            ),
            "classes": ("collapse",),
        }),
        ("Generated / Released", {"fields": ("generated_by", "generated_at", "released_by", "released_at")}),
    )


@admin.register(EmployeeExtraWorkDayRequest)
class EmployeeExtraWorkDayRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "work_date", "status", "extra_leave_added", "manager_approved_by", "hr_approved_by", "created_at")
    list_filter = ("status", "extra_leave_added", "work_date", "created_at")
    search_fields = ("employee__username", "employee__first_name", "employee__last_name", "reason", "manager_remarks", "hr_remarks")
    readonly_fields = ("created_at", "manager_approved_at", "hr_approved_at")
    autocomplete_fields = ("employee", "manager_approved_by", "hr_approved_by")
    ordering = ("-created_at",)


# =========================================================
# ASSET MANAGEMENT
# =========================================================

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code_prefix", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "code_prefix", "description")
    readonly_fields = ("created_at",)
    ordering = ("name",)


class AssetAssignmentInline(admin.TabularInline):
    model = AssetAssignment
    extra = 0
    readonly_fields = ("assigned_at", "returned_at")
    autocomplete_fields = ("employee", "assigned_by", "returned_by")


@admin.register(AssetItem)
class AssetItemAdmin(admin.ModelAdmin):
    list_display = ("id", "asset_code", "name", "category", "brand", "model_number", "serial_number", "status", "current_employee", "purchase_date", "purchase_value", "updated_at")
    list_filter = ("category", "status", "purchase_date", "created_at", "updated_at")
    search_fields = ("asset_code", "name", "brand", "model_number", "serial_number", "description", "current_employee__username")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("category", "current_employee", "created_by")
    ordering = ("category__name", "asset_code")
    inlines = [AssetAssignmentInline]


@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "asset", "employee", "assigned_by", "assigned_at", "is_active", "returned_at", "returned_by")
    list_filter = ("is_active", "assigned_at", "returned_at")
    search_fields = ("asset__asset_code", "asset__name", "employee__username", "employee__first_name", "employee__last_name", "handover_note", "return_note")
    readonly_fields = ("assigned_at", "returned_at")
    autocomplete_fields = ("asset", "employee", "assigned_by", "returned_by")
    ordering = ("-assigned_at",)


# =========================================================
# DEALER POINTS / REDEMPTION
# =========================================================

@admin.register(DealerPointSetting)
class DealerPointSettingAdmin(admin.ModelAdmin):
    list_display = ("id", "farmer_points", "rupees_per_point", "minimum_money_redemption_points", "minimum_product_redemption_points", "is_active", "updated_at")
    list_filter = ("is_active", "updated_at")
    readonly_fields = ("updated_at",)


@admin.register(FarmerData)
class FarmerDataAdmin(admin.ModelAdmin):
    list_display = ("id", "farmer_name", "mobile_number", "place", "dealer", "points_awarded", "created_by", "created_at")
    list_filter = ("points_awarded", "created_at")
    search_fields = ("farmer_name", "mobile_number", "place", "dealer__firm_name", "created_by__username")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("dealer", "created_by")
    ordering = ("-created_at",)


@admin.register(DealerPointLedger)
class DealerPointLedgerAdmin(admin.ModelAdmin):
    list_display = ("id", "dealer", "transaction_type", "points", "farmer_data", "redemption_request", "note", "created_at")
    list_filter = ("transaction_type", "created_at")
    search_fields = ("dealer__firm_name", "farmer_data__farmer_name", "note")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("dealer", "farmer_data", "redemption_request")
    ordering = ("-created_at",)


@admin.register(DealerPointProductRule)
class DealerPointProductRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "pack_size", "title", "points_required", "free_quantity", "is_active", "created_at")
    list_filter = ("is_active", "created_at", "product__category")
    search_fields = ("product__name", "title")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("product", "pack_size")
    ordering = ("product__name", "points_required")


@admin.register(DealerPointRedemptionRequest)
class DealerPointRedemptionRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dealer",
        "redemption_type",
        "points_requested",
        "money_amount",
        "product_rule",
        "request_quantity",
        "requested_free_quantity",
        "status_badge",
        "sales_officer",
        "asm",
        "accountant",
        "created_at",
    )
    list_filter = ("redemption_type", "status", "created_at")
    search_fields = ("dealer__firm_name", "requested_by__username", "rejection_reason")
    readonly_fields = ("sales_officer_approved_at", "asm_approved_at", "accountant_approved_at", "rejected_at", "created_at")
    autocomplete_fields = ("dealer", "requested_by", "product_rule", "sales_officer", "asm", "accountant", "rejected_by")
    ordering = ("-created_at",)

    def status_badge(self, obj):
        colors = {
            "PENDING_SALES_OFFICER": "#f59e0b",
            "PENDING_ASM": "#2563eb",
            "PENDING_ACCOUNTANT": "#7c3aed",
            "APPROVED": "#16a34a",
            "REJECTED": "#dc2626",
        }
        return badge(obj.get_status_display(), colors.get(obj.status, "#64748b"))

    status_badge.short_description = "Status"


@admin.register(DealerVisit)
class DealerVisitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dealer",
        "sales_officer",
        "visit_date",
        "visit_time",
        "reason",
        "latitude",
        "longitude",
        "created_at",
    )

    list_filter = (
        "reason",
        "visit_date",
        "created_at",
    )

    search_fields = (
        "dealer__firm_name",
        "dealer__owner_name",
        "dealer__phone",
        "sales_officer__username",
        "sales_officer__first_name",
        "sales_officer__last_name",
        "note",
    )

    readonly_fields = (
        "stamped_image_preview",
        "created_at",
    )

    ordering = ("-visit_date", "-visit_time")

    def stamped_image_preview(self, obj):
        if obj and obj.stamped_image:
            return format_html(
                '<img src="{}" style="width:320px;border-radius:16px;border:1px solid #ddd;" />',
                obj.stamped_image.url
            )

        return "No stamped image"

    stamped_image_preview.short_description = "Stamped Image"

