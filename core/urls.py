# core/urls.py

from django.urls import path

from . import views
from django.views.generic import RedirectView

urlpatterns = [
    # =========================
    # DASHBOARD
    # =========================
    path(
        "accounts/profile/",
        RedirectView.as_view(pattern_name="dashboard", permanent=False),
        name="accounts_profile_redirect",
    ),
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # =========================
    # PROFILE
    # =========================
    path("my-profile/", views.my_profile, name="my_profile"),
    path("dealer-pending/", views.dealer_pending, name="dealer_pending"),

    # =========================
    # EMPLOYEES
    # =========================
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/create/", views.employee_create, name="employee_create"),
    path("employees/<int:pk>/edit/", views.employee_edit, name="employee_edit"),

    # =========================
    # DEALERS
    # =========================
    path("dealers/create/", views.dealer_create, name="dealer_create"),
    path("dealers/", views.dealer_list, name="dealer_list"),

    path(
        "dealers/<int:dealer_id>/edit/",
        views.dealer_edit,
        name="dealer_edit",
    ),

    path(
        "dealers/approvals/",
        views.dealer_approval_list,
        name="dealer_approval_list",
    ),

    path(
        "dealers/approvals/<int:dealer_id>/",
        views.dealer_approval_detail,
        name="dealer_approval_detail",
    ),

    path(
        "dealers/<int:dealer_id>/approve/",
        views.dealer_approve,
        name="dealer_approve",
    ),

    path(
        "dealers/<int:dealer_id>/reject/",
        views.dealer_reject,
        name="dealer_reject",
    ),

    path(
        "dealers/<int:dealer_id>/forward-rm/",
        views.dealer_forward_to_rm,
        name="dealer_forward_to_rm",
    ),

    path(
        "dealers/<int:dealer_id>/forward-state-head/",
        views.dealer_forward_to_state_head,
        name="dealer_forward_to_state_head",
    ),

    # =========================
    # WAREHOUSES
    # =========================
    path("warehouses/", views.warehouse_list, name="warehouse_list"),
    path("warehouses/create/", views.warehouse_create, name="warehouse_create"),

    # =========================
    # FARMER MEETINGS
    # =========================
    path("farmer-meets/", views.farmer_meet_list, name="farmer_meet_list"),

    path(
        "farmer-meets/create/",
        views.farmer_meet_create,
        name="farmer_meet_create",
    ),

    path(
        "farmer-meets/<int:meet_id>/",
        views.farmer_meet_detail,
        name="farmer_meet_detail",
    ),

    path(
        "farmer-meets/<int:meet_id>/approve/",
        views.farmer_meet_approve,
        name="farmer_meet_approve",
    ),

    path(
        "farmer-meets/<int:meet_id>/reject/",
        views.farmer_meet_reject,
        name="farmer_meet_reject",
    ),
    path("product-categories/create/", views.product_category_create, name="product_category_create"),
    path(
        "product-categories/",
        views.product_category_list,
        name="product_category_list",
    ),
    path(
        "product-categories/<int:pk>/edit/",
        views.product_category_edit,
        name="product_category_edit",
    ),

    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.product_create, name="product_create"),
    path(
            "products/<int:product_id>/edit/",
            views.product_edit,
            name="product_edit",
        ),
    path("products/<int:product_id>/deactivate/", views.product_deactivate, name="product_deactivate"),
    path("products/<int:product_id>/force-delete/", views.product_force_delete, name="product_force_delete"),
    path('dealer/product/<int:product_id>/', views.dealer_product_detail, name='dealer_product_detail'),

    path("dealer/products/", views.dealer_products, name="dealer_products"),
    path("dealer/cart/", views.dealer_cart, name="dealer_cart"),
    path("dealer/cart/add/<int:pack_id>/", views.dealer_add_to_cart, name="dealer_add_to_cart"),
    path("dealer/cart/remove/<int:item_id>/", views.dealer_remove_cart_item, name="dealer_remove_cart_item"),
    # =========================
    # DEALER ORDER WORKFLOW
    # =========================
    path("dealer/cart/place-order/", views.dealer_place_order, name="dealer_place_order"),

    path("orders/", views.dealer_order_list, name="dealer_order_list"),
    path("orders/<int:order_id>/", views.dealer_order_detail, name="dealer_order_detail"),

    path("orders/<int:order_id>/approve/", views.dealer_order_approve, name="dealer_order_approve"),
    path("orders/<int:order_id>/reject/", views.dealer_order_reject, name="dealer_order_reject"),

    path("orders/<int:order_id>/warehouse-review/", views.warehouse_order_review, name="warehouse_order_review"),
    path("orders/<int:order_id>/accountant-invoice-review/", views.accountant_invoice_review, name="accountant_invoice_review"),
    path("orders/<int:order_id>/dispatch/", views.warehouse_dispatch_order, name="warehouse_dispatch_order"),

    path("invoices/", views.dealer_invoice_list, name="dealer_invoice_list"),
    path(
        "invoices/<int:invoice_id>/<str:copy_type>/print/",
        views.dealer_invoice_print,
        name="dealer_invoice_print",
    ),
    path(
        "orders/<int:order_id>/accept-delivery/",
        views.dealer_accept_delivery,
        name="dealer_accept_delivery",
    ),
    path(
        "invoices/<int:invoice_id>/convert-sales/",
        views.convert_invoice_to_sales,
        name="convert_invoice_to_sales",
    ),

    path(
        "invoices/<int:invoice_id>/history/",
        views.invoice_edit_history,
        name="invoice_edit_history",
    ),
    path(
        "invoices/<int:invoice_id>/payment-preview/",
        views.invoice_payment_preview,
        name="invoice_payment_preview",
    ),
    path(
    "reports/paid-sales/",
    views.paid_sales_report,
    name="paid_sales_report",
),
path("accounts/", views.accounts_dashboard, name="accounts_dashboard"),

path(
    "accounts/bank/create/",
    views.company_account_create,
    name="company_account_create",
),

path(
    "accounts/payment-in/create/",
    views.company_payment_in_create,
    name="company_payment_in_create",
),

path(
    "accounts/payment-out/create/",
    views.company_payment_out_create,
    name="company_payment_out_create",
),
path(
    "reports/order-payment-difference/",
    views.order_payment_difference_report,
    name="order_payment_difference_report",
),
path(
    "transport-copies/",
    views.transport_copy_list,
    name="transport_copy_list",
),
path(
    "sales-returns/",
    views.sales_return_credit_note_list,
    name="sales_return_credit_note_list",
),

path(
    "sales-returns/create/",
    views.sales_return_credit_note_create,
    name="sales_return_credit_note_create",
),

path(
    "sales-returns/<int:pk>/edit/",
    views.sales_return_credit_note_edit,
    name="sales_return_credit_note_edit",
),

path(
    "sales-returns/<int:pk>/print/",
    views.sales_return_credit_note_print,
    name="sales_return_credit_note_print",
),

path(
    "ajax/return-dealer-invoices/",
    views.ajax_return_dealer_invoices,
    name="ajax_return_dealer_invoices",
),

path(
    "ajax/return-invoice-items/",
    views.ajax_return_invoice_items,
    name="ajax_return_invoice_items",
),
path(
    "sales-returns/<int:pk>/toggle-dealer-visibility/",
    views.sales_return_credit_note_toggle_dealer_visibility,
    name="sales_return_credit_note_toggle_dealer_visibility",
),

path(
    "sales-returns/<int:pk>/delete/",
    views.sales_return_credit_note_delete,
    name="sales_return_credit_note_delete",
),
path(
    "dealer/cart/item/<int:item_id>/increase/",
    views.dealer_increase_cart_item,
    name="dealer_increase_cart_item",
),

path(
    "dealer/cart/item/<int:item_id>/decrease/",
    views.dealer_decrease_cart_item,
    name="dealer_decrease_cart_item",
),
path("employee/attendance/", views.employee_attendance_dashboard, name="employee_attendance_dashboard"),
path("employee/attendance/clock-in/", views.employee_clock_in, name="employee_clock_in"),
path("employee/attendance/gps-ping/", views.employee_gps_ping, name="employee_gps_ping"),
path("employee/attendance/clock-out/", views.employee_clock_out, name="employee_clock_out"),

path("manager/attendance/approvals/", views.manager_attendance_approvals, name="manager_attendance_approvals"),
path("manager/attendance/<int:attendance_id>/approve/", views.manager_approve_attendance, name="manager_approve_attendance"),

path("hr/attendance/claims/", views.hr_attendance_claims, name="hr_attendance_claims"),
path("hr/attendance/<int:attendance_id>/approve/", views.hr_approve_attendance, name="hr_approve_attendance"),

path("accountant/attendance/claims/", views.accountant_attendance_claims, name="accountant_attendance_claims"),
path("accountant/attendance/<int:attendance_id>/release/", views.accountant_release_attendance_claim, name="accountant_release_attendance_claim"),
path(
    "attendance/accountant-claims/bulk-release/",
    views.accountant_bulk_release_attendance_claims,
    name="accountant_bulk_release_attendance_claims"
),

path("employee/leaves/", views.employee_leave_list, name="employee_leave_list"),
path("employee/leaves/apply/", views.employee_leave_request_create, name="employee_leave_request_create"),

path("manager/leaves/approvals/", views.manager_leave_approvals, name="manager_leave_approvals"),
path("manager/leaves/<int:leave_id>/approve/", views.manager_approve_leave, name="manager_approve_leave"),
path("manager/leaves/<int:leave_id>/reject/", views.manager_reject_leave, name="manager_reject_leave"),
path(
    "hr-management-dashboard/",
    views.hr_management_dashboard,
    name="hr_management_dashboard"
),
path("payslips/", views.payslip_list, name="payslip_list"),
path("payslips/generate/", views.payslip_generate, name="payslip_generate"),
path("payslips/<int:payslip_id>/", views.payslip_detail, name="payslip_detail"),
path("payslips/<int:payslip_id>/edit/", views.payslip_edit, name="payslip_edit"),
path("payslips/<int:payslip_id>/release/", views.payslip_release, name="payslip_release"),
path("payslips/release-bulk/", views.payslip_release_bulk, name="payslip_release_bulk"),
path("my-payslips/", views.my_payslips, name="my_payslips"),
path("payslips/<int:payslip_id>/print/", views.payslip_print, name="payslip_print"),
path(
    "employee/tada-calendar/",
    views.employee_tada_calendar,
    name="employee_tada_calendar"
),
path("employee/extra-workdays/", views.employee_extra_workday_list, name="employee_extra_workday_list"),
path("employee/extra-workdays/request/", views.employee_extra_workday_create, name="employee_extra_workday_create"),

path("manager/extra-workdays/", views.manager_extra_workday_requests, name="manager_extra_workday_requests"),
path("manager/extra-workdays/<int:request_id>/approve/", views.manager_approve_extra_workday, name="manager_approve_extra_workday"),
path("manager/extra-workdays/<int:request_id>/reject/", views.manager_reject_extra_workday, name="manager_reject_extra_workday"),

path("hr/extra-workdays/", views.hr_extra_workday_requests, name="hr_extra_workday_requests"),
path("hr/extra-workdays/<int:request_id>/approve/", views.hr_approve_extra_workday, name="hr_approve_extra_workday"),

path("employee/leave-balance/", views.employee_leave_balance, name="employee_leave_balance"),
path(
    "warehouse/my-products/",
    views.warehouse_my_products,
    name="warehouse_my_products"
),

path(
    "warehouse/my-orders/",
    views.warehouse_my_orders,
    name="warehouse_my_orders"
),
path(
    "products/<int:product_id>/stickers/",
    views.product_sticker_print,
    name="product_sticker_print",
),

path(
    "product-info/<int:product_id>/",
    views.public_product_detail,
    name="public_product_detail",
),
path("assets/", views.asset_list, name="asset_list"),
path("assets/create/", views.asset_create_bulk, name="asset_create_bulk"),
path("assets/<int:asset_id>/assign/", views.asset_assign, name="asset_assign"),
path("assets/my-assets/", views.my_assets, name="my_assets"),
path("assets/<int:asset_id>/history/", views.asset_detail, name="asset_detail"),
path("assets/return/<int:assignment_id>/", views.asset_return, name="asset_return"),
path("assets/employee/<int:employee_id>/", views.employee_assets_detail, name="employee_assets_detail"),
path("dealer/farmer-data/", views.dealer_farmer_data, name="dealer_farmer_data"),
path("dealer/points/", views.dealer_points_dashboard, name="dealer_points_dashboard"),
path("dealer/points/redeem/", views.dealer_redemption_create, name="dealer_redemption_create"),

path("dealer/redemptions/approvals/", views.dealer_redemption_approvals, name="dealer_redemption_approvals"),
path("dealer/redemptions/<int:request_id>/approve/", views.dealer_redemption_approve, name="dealer_redemption_approve"),
path("dealer/redemptions/<int:request_id>/reject/", views.dealer_redemption_reject, name="dealer_redemption_reject"),
path("dealer/points/settings/", views.dealer_point_admin_settings, name="dealer_point_admin_settings"),
path("farmer-data/all/", views.farmer_data_admin_list, name="farmer_data_admin_list"),
path("farmer-data/export/<str:export_type>/", views.farmer_data_admin_export, name="farmer_data_admin_export"),
path("dealer-visits/", views.dealer_visit_list, name="dealer_visit_list"),
path("dealer-visits/create/", views.dealer_visit_create, name="dealer_visit_create"),
path("dealer-visits/<int:visit_id>/", views.dealer_visit_detail, name="dealer_visit_detail"),
path("dealers/credit-scores/", views.dealer_credit_score_list, name="dealer_credit_score_list"),
path("dealers/<int:dealer_id>/credit-score/", views.dealer_credit_score_update, name="dealer_credit_score_update"),
path("dealer/my-credit-score/", views.dealer_my_credit_score, name="dealer_my_credit_score"),
# ==========================================================
# SIMPLE PURCHASE MODULE - URLS
# Paste these paths inside urlpatterns in core/urls.py
# ==========================================================
# ==========================================================
# SIMPLE PURCHASE MANAGEMENT
# ==========================================================

path("purchase/", views.purchase_dashboard, name="purchase_dashboard"),
path("purchase/dashboard/excel/", views.purchase_dashboard_excel, name="purchase_dashboard_excel"),

path("purchase/entries/", views.purchase_dashboard, name="purchase_entry_list"),
path("purchase/orders/", views.purchase_dashboard, name="purchase_order_list"),
path("purchase/bills/", views.purchase_dashboard, name="purchase_bill_list"),

path("purchase/entry/new/", views.purchase_entry_create, name="purchase_entry_create"),
path("purchase/entry/<int:bill_id>/edit/", views.purchase_entry_edit, name="purchase_entry_edit"),
path("purchase/entry/<int:bill_id>/print/", views.purchase_entry_print, name="purchase_entry_print"),

path("purchase/payment-out/", views.purchase_payment_out_create, name="purchase_payment_out_create"),
path("purchase/payments/", views.purchase_payment_out_create, name="purchase_payment_out_list"),

path("purchase/return/", views.purchase_return_create, name="purchase_return_create"),
path("purchase/returns/", views.purchase_return_create, name="purchase_return_list"),

path("purchase/production/", views.production_make_product_create, name="production_make_product_create"),

# Compatibility old names
path("purchase/inventory/", views.purchase_dashboard, name="inventory_item_list"),
path("purchase/recipes/", views.production_make_product_create, name="production_recipe_list"),
path("purchase/batches/", views.production_make_product_create, name="production_batch_list"),
path("purchase/repacking/", views.production_make_product_create, name="repacking_batch_list"),
path("purchase/parties/", views.purchase_entry_create, name="purchase_party_list"),
path("purchase/types/", views.purchase_entry_create, name="purchase_type_list"),
path("purchase/entry/<int:bill_id>/view/", views.purchase_entry_detail, name="purchase_entry_detail"),
path("purchase/entry/<int:bill_id>/delete/", views.purchase_entry_delete, name="purchase_entry_delete"),
path("purchase/entry/<int:bill_id>/duplicate/", views.purchase_entry_duplicate, name="purchase_entry_duplicate"),
path("purchase/entry/<int:bill_id>/history/", views.purchase_entry_history, name="purchase_entry_history"),
path("products/stock-transfer/", views.product_stock_transfer_list, name="product_stock_transfer_list"),
path("products/stock-transfer/create/", views.product_stock_transfer_create, name="product_stock_transfer_create"),
path("purchase/stock-history/", views.purchase_stock_history, name="purchase_stock_history"),
path("purchase/formulas/", views.product_formula_list, name="product_formula_list"),
path("purchase/formulas/create/", views.product_formula_create, name="product_formula_create"),
path("purchase/formulas/<int:formula_id>/edit/", views.product_formula_edit, name="product_formula_edit"),

path("purchase/smart-production/", views.smart_production_create, name="smart_production_create"),
path("purchase/smart-production/runs/", views.smart_production_run_list, name="smart_production_run_list"),
path("purchase/smart-production/runs/<int:run_id>/", views.smart_production_run_detail, name="smart_production_run_detail"),
path("gst/gstr2b/", views.gstr2b_report, name="gstr2b_report"),
path("gst/gstr1/", views.gstr1_report, name="gstr1_report"),
path("gst/gstr3b/", views.gstr3b_report, name="gstr3b_report"),
# Add this in urls.py if not already added:

path(
    "pending-action-badges/",
    views.pending_action_badges_api,
    name="pending_action_badges_api"
),

]