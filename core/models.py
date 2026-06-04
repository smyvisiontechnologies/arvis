from decimal import Decimal
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import calendar


class State(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class District(models.Model):
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="districts"
    )
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = ("state", "name")
        ordering = ["state__name", "name"]

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("ACCOUNTANT", "Accountant"),
        ("HR", "HR"),
        ("STATE_HEAD", "State Head"),
        ("REGIONAL_MANAGER", "Regional Manager"),
        ("ASM", "Area Sales Manager"),
        ("SALES_OFFICER_SENIOR", "Senior Sales Officer"),
        ("SALES_OFFICER_JUNIOR", "Junior Sales Officer"),
        ("WAREHOUSE_MANAGER", "Warehouse Manager"),
        ("INVENTORY_MANAGER", "Inventory Manager"),
        ("DEVELOPMENT_OFFICER", "Market Development Officer"),
        ("ASSET_MANAGER", "Asset Manager"),
        ("DEALER", "Dealer"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(max_length=40, choices=ROLE_CHOICES)

    profile_image = models.ImageField(
        upload_to="profile_images/",
        null=True,
        blank=True
    )

    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_employees",
        help_text="Assigned reporting manager"
    )

    salary_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Monthly salary amount"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Employee date of birth"
    )

    pan_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="PAN Number"
    )

    bank_name = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    bank_account_number = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )

    bank_ifsc_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    bank_account_holder_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    pf_applicable = models.BooleanField(
        default=False,
        help_text="Is PF applicable for this employee?"
    )

    pf_uan_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text="PF UAN Number"
    )

    pf_deduction_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Example: 12 means 12% PF deduction from salary"
    )

    insurance_applicable = models.BooleanField(
        default=False,
        help_text="Is employee related to company insurance?"
    )

    insurance_provider_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    insurance_policy_number = models.CharField(
        max_length=80,
        blank=True,
        null=True
    )

    insurance_deduction_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Monthly insurance deduction from salary"
    )
    manager_target_extra_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Extra target percentage over direct reporting employees target. Example: 50 means team target + 50%."
    )
    employee_code = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        help_text="Employee ID"
    )

    duty_start_time = models.TimeField(null=True, blank=True)
    duty_end_time = models.TimeField(null=True, blank=True)
    # Work week settings
    work_monday = models.BooleanField(default=True)
    work_tuesday = models.BooleanField(default=True)
    work_wednesday = models.BooleanField(default=True)
    work_thursday = models.BooleanField(default=True)
    work_friday = models.BooleanField(default=True)
    work_saturday = models.BooleanField(default=True)
    work_sunday = models.BooleanField(default=False)

    # Earned extra leaves from approved extra working days
    earned_extra_other_leaves = models.PositiveIntegerField(default=0)

    bike_ta_per_km = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    car_ta_per_km = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    daily_da_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    paid_leaves_per_year = models.PositiveIntegerField(default=0)
    sick_leaves_per_year = models.PositiveIntegerField(default=0)
    other_leaves_per_year = models.PositiveIntegerField(default=0)
    unpaid_leaves_per_year = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class EmployeeYearlyTarget(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_yearly_targets"
    )

    year = models.PositiveIntegerField(default=timezone.now().year)

    target_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    achieved_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "year")
        ordering = ["-year"]

    @property
    def balance_amount(self):
        balance = self.target_amount - self.achieved_amount
        return balance if balance > 0 else Decimal("0.00")

    @property
    def achieved_percentage(self):
        if not self.target_amount:
            return 0

        percentage = (self.achieved_amount / self.target_amount) * 100
        return round(min(percentage, 100), 2)

    def __str__(self):
        return f"{self.employee.username} - {self.year}"


class Dealer(models.Model):
    FLAG_CHOICES = (
        ("GREEN", "Green Flag"),
        ("ORANGE", "Orange Flag"),
        ("RED", "Red Flag"),
    )

    FIRM_TYPE_CHOICES = (
        ("OWNED", "Owned"),
        ("RENTED", "Rented"),
        ("LEASED", "Leased"),
    )

    DEPOSIT_MODE_CHOICES = (
        ("CHEQUE", "Cheque"),
    )

    APPROVAL_STATUS_CHOICES = (
        ("PENDING_ASM", "Pending ASM Approval"),
        ("FORWARDED_RM", "Forwarded to Regional Manager"),
        ("FORWARDED_STATE_HEAD", "Forwarded to State Head"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dealer_profile",
        null=True,
        blank=True,
    )
    dealer_code = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True
    )

    dealer_image = models.ImageField(
        upload_to="dealer_images/",
        null=True,
        blank=True
    )

    firm_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)

    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    owner_address = models.TextField(blank=True, null=True)

    gst_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="GST Number"
    )

    firm_address = models.TextField(blank=True, null=True)

    firm_type = models.CharField(
        max_length=20,
        choices=FIRM_TYPE_CHOICES,
        default="OWNED"
    )

    license_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Optional"
    )

    state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    deposit_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("15000.00")
    )

    deposit_mode = models.CharField(
        max_length=20,
        choices=DEPOSIT_MODE_CHOICES,
        default="CHEQUE"
    )

    cheque_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    flag = models.CharField(
        max_length=20,
        choices=FLAG_CHOICES,
        default="GREEN",
    )

    yearly_target_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    achieved_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )
    credit_score = models.PositiveSmallIntegerField(
        default=650,
        help_text="Dealer credit score between 300 and 900"
    )

    credit_score_change_points = models.IntegerField(
        default=0,
        help_text="Last score change points. Example: 71 or -20"
    )

    credit_score_note = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Reason/note for credit score update"
    )

    credit_score_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dealer_credit_score_updates"
    )

    credit_score_updated_at = models.DateTimeField(
        null=True,
        blank=True
    )
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    location_accuracy_meters = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    visit_radius_meters = models.PositiveIntegerField(
        default=15
    )

    created_by_sales_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dealers_created_by_sales_officer",
    )

    concerned_asm = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dealers_under_asm",
    )
    asm_approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dealer_asm_approvals",
    )

    asm_approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    regional_manager_approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dealer_rm_approvals",
    )

    regional_manager_approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    state_head_approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dealer_state_head_approvals",
    )

    state_head_approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    rejected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dealer_rejections",
    )

    rejected_at = models.DateTimeField(
        null=True,
        blank=True
    )

    rejection_reason = models.TextField(
        blank=True,
        null=True
    )
    forwarded_regional_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dealers_forwarded_to_rm",
    )

    forwarded_state_head = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dealers_forwarded_to_state_head",
    )

    approval_status = models.CharField(
        max_length=40,
        choices=APPROVAL_STATUS_CHOICES,
        default="PENDING_ASM",
    )

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.firm_name:
            if self.dealer_code:
                return f"{self.firm_name} - {self.dealer_code}"
            return self.firm_name

        if self.owner_name:
            return self.owner_name

        return f"Dealer {self.id}"
    
    @property
    def target_balance_amount(self):
        balance = self.yearly_target_amount - self.achieved_amount

        if balance > 0:
            return balance

        return Decimal("0.00")

    @property
    def target_achieved_percentage(self):
        if not self.yearly_target_amount:
            return 0

        percentage = (self.achieved_amount / self.yearly_target_amount) * 100

        if percentage > 100:
            percentage = 100

        return round(percentage, 2)

    def activate_dealer_login(self):
        self.is_active = True
        self.approval_status = "APPROVED"

        if self.user:
            self.user.is_active = True
            self.user.save(update_fields=["is_active"])

        self.save(update_fields=["is_active", "approval_status", "updated_at"])


    def deactivate_dealer_login(self):
        self.is_active = False

        if self.user:
            self.user.is_active = False
            self.user.save(update_fields=["is_active"])

        self.save(update_fields=["is_active", "updated_at"])


    def reject_dealer(self, user, reason):
        self.approval_status = "REJECTED"
        self.is_active = False
        self.rejected_by = user
        self.rejected_at = timezone.now()
        self.rejection_reason = reason

        if self.user:
            self.user.is_active = False
            self.user.save(update_fields=["is_active"])

        self.save()

    

    def clean(self):
        super().clean()

        if self.deposit_amount is not None and self.deposit_amount < Decimal("15000.00"):
            raise ValidationError({
                "deposit_amount": "Minimum cheque deposit amount is ₹15,000."
            })

        if self.deposit_mode != "CHEQUE":
            raise ValidationError({
                "deposit_mode": "Deposit mode must be cheque only."
            })
        
        if self.credit_score is not None:
            if self.credit_score < 300 or self.credit_score > 900:
                raise ValidationError({
                    "credit_score": "Credit score must be between 300 and 900."
                })


    def save(self, *args, **kwargs):
        # Dealer deposit mode must always be cheque
        self.deposit_mode = "CHEQUE"

        # Validate dealer before saving
        self.full_clean()

        # First save, so Django creates the ID
        super().save(*args, **kwargs)

        # Create dealer code after ID is available
        if not self.dealer_code:
            self.dealer_code = f"DLR{self.id:05d}"
        super().save(update_fields=["dealer_code"])

class DealerCreditScoreHistory(models.Model):
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name="credit_score_history"
    )

    old_score = models.PositiveSmallIntegerField(default=650)
    new_score = models.PositiveSmallIntegerField(default=650)
    change_points = models.IntegerField(default=0)

    note = models.CharField(max_length=255, blank=True, null=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.dealer.firm_name} - {self.old_score} to {self.new_score}"
        

def current_local_time():
    return timezone.localtime().time()


class DealerVisit(models.Model):
    REASON_CHOICES = (
        ("REGULAR_VISIT", "Regular Visit"),
        ("PAYMENT_FOLLOWUP", "Payment Follow-up"),
        ("ORDER_FOLLOWUP", "Order Follow-up"),
        ("PRODUCT_PROMOTION", "Product Promotion"),
        ("COMPLAINT_VISIT", "Complaint Visit"),
        ("STOCK_CHECK", "Stock Check"),
        ("SCHEME_EXPLANATION", "Scheme Explanation"),
        ("OTHER", "Other"),
    )

    sales_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dealer_visits"
    )

    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name="dealer_visits"
    )

    visit_date = models.DateField(default=timezone.localdate)
    visit_time = models.TimeField(default=current_local_time)

    reason = models.CharField(
        max_length=40,
        choices=REASON_CHOICES,
        default="REGULAR_VISIT"
    )

    note = models.TextField(blank=True, null=True)

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    visit_image = models.ImageField(
        upload_to="dealer_visits/original/",
        null=True,
        blank=True
    )

    stamped_image = models.ImageField(
        upload_to="dealer_visits/stamped/",
        null=True,
        blank=True
    )
    gps_accuracy_meters = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    distance_from_dealer_meters = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    location_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-visit_date", "-visit_time", "-created_at"]

    def __str__(self):
        return f"{self.dealer.firm_name} - {self.sales_officer.username} - {self.visit_date}"



class DealerApprovalHistory(models.Model):
    ACTION_CHOICES = (
        ("CREATED", "Created"),
        ("ASM_APPROVED", "ASM Approved"),
        ("FORWARDED_RM", "Forwarded to Regional Manager"),
        ("RM_APPROVED", "Regional Manager Approved"),
        ("FORWARDED_STATE_HEAD", "Forwarded to State Head"),
        ("STATE_HEAD_APPROVED", "State Head Approved"),
        ("REJECTED", "Rejected"),
    )

    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name="approval_history"
    )

    action = models.CharField(max_length=40, choices=ACTION_CHOICES)

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.dealer.firm_name} - {self.action}"


class Warehouse(models.Model):
    state = models.ForeignKey(
        State,
        on_delete=models.PROTECT,
        related_name="warehouses"
    )

    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name="warehouses"
    )

    name = models.CharField(max_length=255)

    warehouse_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="managed_warehouses"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("district", "name")
        ordering = ["state__name", "district__name", "name"]

    def __str__(self):
        return f"{self.name} - {self.district.name}"


class FarmerMeetRequest(models.Model):
    STATUS_CHOICES = (
        ("PENDING_SALES_OFFICER", "Pending Sales Officer"),
        ("PENDING_ASM", "Pending ASM"),
        ("PENDING_REGIONAL_MANAGER", "Pending Regional Manager"),
        ("PENDING_STATE_HEAD", "Pending State Head"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    meeting_date = models.DateField()

    expected_farmer_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    created_by_mdo = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_farmer_meets"
    )

    sales_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales_officer_farmer_meets"
    )

    asm = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asm_farmer_meets"
    )

    regional_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rm_farmer_meets"
    )

    state_head = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="state_head_farmer_meets"
    )

    approval_status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default="PENDING_SALES_OFFICER"
    )

    rejected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rejected_farmer_meets"
    )

    rejection_reason = models.TextField(blank=True, null=True)
    rejected_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_next_status_after_approval(self):
        if self.approval_status == "PENDING_SALES_OFFICER":
            return "PENDING_ASM"

        if self.approval_status == "PENDING_ASM":
            if self.expected_farmer_count <= 50:
                return "APPROVED"
            return "PENDING_REGIONAL_MANAGER"

        if self.approval_status == "PENDING_REGIONAL_MANAGER":
            if self.expected_farmer_count <= 100:
                return "APPROVED"
            return "PENDING_STATE_HEAD"

        if self.approval_status == "PENDING_STATE_HEAD":
            return "APPROVED"

        return self.approval_status

    def __str__(self):
        return self.title


class FarmerMeetApprovalHistory(models.Model):
    farmer_meet = models.ForeignKey(
        FarmerMeetRequest,
        on_delete=models.CASCADE,
        related_name="approval_history"
    )

    action = models.CharField(max_length=80)

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]





from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class ProductCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CategoryPaymentRule(models.Model):
    RULE_TYPE_CHOICES = (
        ("ADVANCE", "Advance Payment"),
        ("INSTANT", "Instant Payment"),
        ("DAY_RANGE", "Day Wise Payment"),
    )

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name="payment_rules"
    )

    rule_type = models.CharField(
        max_length=20,
        choices=RULE_TYPE_CHOICES
    )

    title = models.CharField(
        max_length=120,
        help_text="Example: 1 to 20 Days Payment Discount"
    )

    discount_percent = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00")
    )

    from_day = models.PositiveIntegerField(null=True, blank=True)
    to_day = models.PositiveIntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "rule_type", "from_day"]

    def clean(self):
        if self.rule_type == "DAY_RANGE":
            if self.from_day is None or self.to_day is None:
                raise ValidationError("From day and To day are required for day wise payment rule.")

            if self.from_day > self.to_day:
                raise ValidationError("From day cannot be greater than To day.")

    def __str__(self):
        return f"{self.category.name} - {self.title} - {self.discount_percent}%"


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="products"
    )

    name = models.CharField(max_length=180)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    hsn_number = models.CharField(max_length=50, blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def available_pack_count(self):
        return self.pack_sizes.filter(is_active=True, stock_boxes__gt=0).count()

    @property
    def in_stock(self):
        return self.pack_sizes.filter(is_active=True, stock_boxes__gt=0).exists()

    def __str__(self):
        return self.name


class ProductPackSize(models.Model):
    UNIT_CHOICES = (
        ("GRAM", "Gram"),
        ("KG", "Kg"),
        ("ML", "ML"),
        ("LITRE", "Litre"),
        ("PIECE", "Piece"),
    )

    PACKING_TYPE_CHOICES = (
        ("BAG", "Bag"),
        ("BOX", "Box"),
        ("BOTTLE", "Bottle"),
        ("PACKET", "Packet"),
        ("CARTON", "Carton"),
        ("PIECE", "Piece"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="pack_sizes"
    )

    warehouse = models.ForeignKey(
        "Warehouse",
        on_delete=models.PROTECT,
        related_name="product_pack_sizes"
    )

    pack_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Example: 1, 5, 25, 100"
    )

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default="KG"
    )

    packing_type = models.CharField(
        max_length=20,
        choices=PACKING_TYPE_CHOICES,
        default="BAG"
    )

    units_per_box = models.PositiveIntegerField(
        default=1,
        help_text="Example: 1KG bag × 25 pieces in one box"
    )

    mrp_per_unit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    sale_price_per_unit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    purchase_price_per_unit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Internal purchase price, not shown to dealer"
    )

    box_sale_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Total sale price for full box/bag/carton"
    )

    stock_boxes = models.PositiveIntegerField(
        default=0,
        help_text="Available boxes/cartons/bags for this pack"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["product", "pack_size"]

    def clean(self):
        if self.units_per_box <= 0:
            raise ValidationError("Units per box must be greater than 0.")

        if self.sale_price_per_unit < 0 or self.mrp_per_unit < 0 or self.purchase_price_per_unit < 0:
            raise ValidationError("Prices cannot be negative.")

    def save(self, *args, **kwargs):
        if not self.box_sale_price or self.box_sale_price <= 0:
            self.box_sale_price = self.sale_price_per_unit * self.units_per_box

        super().save(*args, **kwargs)

    @property
    def display_pack(self):
        size = int(self.pack_size) if self.pack_size == int(self.pack_size) else self.pack_size
        return f"{size} {self.get_unit_display()}"

    @property
    def display_box(self):
        return f"{self.units_per_box} {self.get_packing_type_display()}s"

    @property
    def total_quantity_label(self):
        total = self.pack_size * self.units_per_box
        total_display = int(total) if total == int(total) else total
        return f"{total_display} {self.get_unit_display()}"

    @property
    def margin_percent(self):
        if not self.sale_price_per_unit:
            return 0

        margin = ((self.sale_price_per_unit - self.purchase_price_per_unit) / self.sale_price_per_unit) * 100
        return round(margin, 2)

    @property
    def is_in_stock(self):
        return self.is_active and self.stock_boxes > 0

    def __str__(self):
        return f"{self.product.name} - {self.display_pack} - {self.warehouse.name}"

class ProductStickerSetting(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="sticker_setting"
    )

    pack_size = models.ForeignKey(
        ProductPackSize,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    width_mm = models.DecimalField(max_digits=6, decimal_places=2, default=100)
    height_mm = models.DecimalField(max_digits=6, decimal_places=2, default=75)
    copies = models.PositiveIntegerField(default=1)

    company_name = models.CharField(
        max_length=255,
        default="ARVIS FERTILIZERS & CHEMICALS PVT. LTD."
    )
    company_address = models.CharField(
        max_length=300,
        default="Company Address, Telangana, India"
    )
    company_email = models.EmailField(
        max_length=150,
        blank=True,
        default="info@arvisfertilizers.com"
    )
    company_website = models.CharField(
        max_length=150,
        blank=True,
        default="www.arvisfertilizers.com"
    )
    customer_care = models.CharField(
        max_length=50,
        blank=True,
        default="8500352005"
    )
    body_font_mm = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("2.25")
    )

    company_subtitle = models.CharField(
        max_length=255,
        default="PRODUCT LABEL / STICKER"
    )

    product_name = models.CharField(max_length=255, blank=True)
    hsn_code = models.CharField(max_length=50, blank=True)
    qty_per_case = models.CharField(max_length=100, blank=True)

    batch_no = models.CharField(max_length=100, blank=True)
    mfg_date = models.CharField(max_length=100, blank=True)
    exp_date = models.CharField(max_length=100, blank=True)

    usp_text = models.CharField(max_length=150, blank=True)
    unit_mrp = models.CharField(max_length=100, blank=True)
    case_mrp = models.CharField(max_length=100, blank=True)

    barcode_value = models.CharField(max_length=100, blank=True)

    manufactured_by = models.CharField(
        max_length=255,
        blank=True,
        default="ARVIS FERTILIZERS & CHEMICALS PVT. LTD."
    )
    marketed_by = models.CharField(
        max_length=255,
        blank=True,
        default="ARVIS FERTILIZERS & CHEMICALS PVT. LTD."
    )

    footer_text = models.CharField(
        max_length=255,
        default="Scan QR for product details."
    )

    show_barcode = models.BooleanField(default=True)
    show_qr = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sticker Setting - {self.product.name}"

class ProductScheme(models.Model):
    SCHEME_TYPE_CHOICES = (
        ("DISCOUNT", "Discount"),
        ("FREE_QTY", "Free Quantity"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="schemes"
    )

    pack_size = models.ForeignKey(
        ProductPackSize,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="schemes",
        help_text="Leave empty if scheme applies to all pack sizes"
    )

    scheme_name = models.CharField(max_length=160)

    scheme_type = models.CharField(
        max_length=20,
        choices=SCHEME_TYPE_CHOICES,
        default="DISCOUNT"
    )

    min_boxes = models.PositiveIntegerField(default=1)

    discount_percent = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00")
    )

    free_boxes = models.PositiveIntegerField(
        default=0,
        help_text="Example: Buy 10 boxes, get 1 box free"
    )

    valid_from = models.DateField(default=timezone.now)
    valid_to = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["product", "min_boxes"]

    def is_valid_today(self):
        today = timezone.localdate()

        if not self.is_active:
            return False

        if self.valid_from and today < self.valid_from:
            return False

        if self.valid_to and today > self.valid_to:
            return False

        return True

    def __str__(self):
        return f"{self.product.name} - {self.scheme_name}"


class DealerCart(models.Model):
    dealer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dealer_cart"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        total = Decimal("0.00")

        for item in self.items.all():
            total += item.total_amount

        return total

    def __str__(self):
        return f"Cart - {self.dealer.username}"


class DealerCartItem(models.Model):
    cart = models.ForeignKey(
        DealerCart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product_pack = models.ForeignKey(
        ProductPackSize,
        on_delete=models.PROTECT,
        related_name="cart_items"
    )

    quantity_boxes = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "product_pack")

    @property
    def total_amount(self):
        return self.product_pack.box_sale_price * self.quantity_boxes

    @property
    def total_units(self):
        return self.product_pack.units_per_box * self.quantity_boxes

    def __str__(self):
        return f"{self.product_pack.product.name} - {self.quantity_boxes} boxes"




from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone


class DealerOrder(models.Model):
    DEALER_FLAG_CHOICES = (
        ("GREEN", "Green"),
        ("ORANGE", "Orange"),
        ("RED", "Red"),
    )

    STATUS_CHOICES = (
        ("PLACED", "Order Placed"),
        ("REJECTED", "Rejected"),
        ("SALES_APPROVAL", "Sales Officer Approval Pending"),
        ("ASM_APPROVAL", "ASM Approval Pending"),
        ("RSM_APPROVAL", "Regional Manager Approval Pending"),
        ("ACCOUNTANT_ORDER_APPROVAL", "Accountant Order Approval Pending"),
        ("WAREHOUSE_REVIEW", "Warehouse Review Pending"),
        ("ACCOUNTANT_INVOICE_REVIEW", "Accountant Invoice Review Pending"),
        ("INVOICE_RELEASED", "Invoice Released"),
        ("DISPATCH_PENDING", "Dispatch Pending"),
        ("DISPATCHED", "Dispatched"),
        ("DELIVERED", "Delivered"),
    )

    dealer = models.ForeignKey(
        "Dealer",
        on_delete=models.PROTECT,
        related_name="orders"
    )

    dealer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="dealer_orders"
    )

    dealer_flag = models.CharField(
        max_length=20,
        choices=DEALER_FLAG_CHOICES
    )

    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default="PLACED"
    )

    concerned_sales_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales_orders"
    )

    concerned_asm = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asm_orders"
    )

    concerned_rsm = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rsm_orders"
    )

    warehouse_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="warehouse_orders"
    )

    subtotal_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    gst_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    rejection_reason = models.TextField(blank=True, null=True)
    rejected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rejected_dealer_orders"
    )
    rejected_at = models.DateTimeField(null=True, blank=True)

    placed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sales_approved_at = models.DateTimeField(null=True, blank=True)
    asm_approved_at = models.DateTimeField(null=True, blank=True)
    rsm_approved_at = models.DateTimeField(null=True, blank=True)
    accountant_order_approved_at = models.DateTimeField(null=True, blank=True)
    warehouse_reviewed_at = models.DateTimeField(null=True, blank=True)
    invoice_released_at = models.DateTimeField(null=True, blank=True)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-placed_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.dealer.firm_name}"

    @property
    def is_rejected(self):
        return self.status == "REJECTED"

    @property
    def can_show_order_placed(self):
        return self.status != "REJECTED"

    def reject_order(self, user, reason):
        self.status = "REJECTED"
        self.rejected_by = user
        self.rejected_at = timezone.now()
        self.rejection_reason = reason
        self.save()


class DealerOrderItem(models.Model):
    order = models.ForeignKey(
        DealerOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product_pack = models.ForeignKey(
        "ProductPackSize",
        on_delete=models.PROTECT,
        related_name="order_items"
    )

    product_name = models.CharField(max_length=180)
    pack_label = models.CharField(max_length=80)

    quantity_boxes = models.PositiveIntegerField(default=1)
    units_per_box = models.PositiveIntegerField(default=1)

    total_units = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    unit_name = models.CharField(max_length=30, default="Pcs")

    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    box_price = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    taxable_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    gst_percent = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("5.00"))
    gst_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    # Warehouse/accountant editable invoice fields
    hsn_code = models.CharField(max_length=50, blank=True, null=True)
    batch_no = models.CharField(max_length=80, blank=True, null=True)
    mfg_date = models.CharField(max_length=20, blank=True, null=True)
    expiry_date = models.CharField(max_length=20, blank=True, null=True)

    warehouse_checked = models.BooleanField(default=False)
    accountant_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product_name} - {self.pack_label}"

    def calculate(self):
        gst_percent = self.gst_percent or Decimal("5.00")

        self.units_per_box = self.product_pack.units_per_box
        self.unit_name = self.product_pack.get_unit_display()

        self.total_units = (
            Decimal(str(self.product_pack.pack_size))
            * Decimal(self.product_pack.units_per_box)
            * Decimal(self.quantity_boxes)
        )

        self.price_per_unit = self.product_pack.sale_price_per_unit
        self.box_price = self.product_pack.box_sale_price

        # box_sale_price treated as GST included amount
        gross_amount = self.box_price * Decimal(self.quantity_boxes)

        self.taxable_amount = (gross_amount * Decimal("100.00")) / (Decimal("100.00") + gst_percent)
        self.gst_amount = gross_amount - self.taxable_amount
        self.total_amount = gross_amount


class DealerOrderApprovalLog(models.Model):
    ACTION_CHOICES = (
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("FORWARDED", "Forwarded"),
        ("CREATED", "Created"),
        ("INVOICE_RELEASED", "Invoice Released"),
        ("DISPATCHED", "Dispatched"),
        ("DELIVERED", "Delivered"),
    )

    order = models.ForeignKey(
        DealerOrder,
        on_delete=models.CASCADE,
        related_name="approval_logs"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    role = models.CharField(max_length=50, blank=True, null=True)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class InvoiceNumberSequence(models.Model):
    financial_year = models.CharField(max_length=10, unique=True)
    last_number = models.PositiveIntegerField(default=0)

    def next_invoice_number(self):
        self.last_number += 1
        self.save(update_fields=["last_number"])

        return f"AFCL/{self.financial_year}/{self.last_number:02d}"

    def __str__(self):
        return f"{self.financial_year} - {self.last_number}"


class DealerInvoice(models.Model):
    COPY_TYPE_CHOICES = (
        ("COMPANY", "Company Copy"),
        ("DEALER", "Dealer Copy"),
        ("TRANSPORTER", "Transporter Copy"),
    )

    order = models.OneToOneField(
        DealerOrder,
        on_delete=models.CASCADE,
        related_name="invoice"
    )

    financial_year = models.CharField(max_length=10)
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField(default=timezone.localdate)

    place_of_supply = models.CharField(max_length=120, blank=True, null=True)

    subtotal_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    gst_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    pending_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    paid_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    released_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    released_at = models.DateTimeField(auto_now_add=True)

    is_converted_to_sales = models.BooleanField(default=False)

    sales_converted_at = models.DateTimeField(null=True, blank=True)

    sales_converted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="converted_sales_invoices"
    )

    discount_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    final_payable_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )
    return_credit_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Total sales return / credit note amount adjusted against this invoice"
    )

    net_payable_after_return = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Final payable amount after reducing sales return credit notes"
    )

    last_payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.invoice_number

    @property
    def balance_amount(self):
        if self.net_payable_after_return and self.net_payable_after_return > 0:
            base_amount = self.net_payable_after_return
        else:
            base_amount = self.final_payable_amount or self.total_amount

        balance = base_amount - self.paid_amount
        return balance if balance > 0 else Decimal("0.00")


from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone


class DealerInvoicePayment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ("FULL", "Full Payment"),
        ("PARTIAL", "Partial Payment"),
    )

    PAYMENT_MODE_CHOICES = (
        ("UPI", "UPI"),
        ("BANK", "Bank Transfer"),
        ("CHEQUE", "Cheque"),
    )

    DISCOUNT_TYPE_CHOICES = (
        ("NONE", "No Discount"),
        ("CATEGORY_RULE", "Category Payment Rule"),
        ("MANUAL", "Manual Discount"),
    )

    invoice = models.ForeignKey(
        "DealerInvoice",
        on_delete=models.CASCADE,
        related_name="payments"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES
    )

    payment_date = models.DateField(default=timezone.localdate)

    gross_invoice_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    payment_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    discount_type = models.CharField(
        max_length=30,
        choices=DISCOUNT_TYPE_CHOICES,
        default="NONE"
    )

    discount_percent = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00")
    )

    discount_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    net_received_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    balance_after_payment = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    category_rule_note = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    upi_reference_number = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    bank_transaction_number = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    cheque_number = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    payment_screenshot = models.ImageField(
        upload_to="invoice_payments/",
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_invoice_payments"
    )
    selected_category_rule_key = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    selected_category_rule_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    selected_category_rule_order_date = models.DateField(
        null=True,
        blank=True
    )

    selected_category_rule_due_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-payment_date", "-created_at"]

    def __str__(self):
        return f"{self.invoice.invoice_number} - ₹{self.payment_amount}"


class DealerInvoiceEditHistory(models.Model):
    invoice = models.ForeignKey(
        "DealerInvoice",
        on_delete=models.CASCADE,
        related_name="edit_history"
    )

    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(max_length=120)

    old_values = models.JSONField(default=dict, blank=True)
    new_values = models.JSONField(default=dict, blank=True)

    note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.action}"



class DealerDispatch(models.Model):
    TRANSPORT_TYPE_CHOICES = (
        ("OWN", "Own Transport"),
        ("OTHER", "Other Transport"),
    )

    order = models.OneToOneField(
        DealerOrder,
        on_delete=models.CASCADE,
        related_name="dispatch"
    )

    transport_type = models.CharField(max_length=20, choices=TRANSPORT_TYPE_CHOICES)

    vehicle_name = models.CharField(max_length=120, blank=True, null=True)
    vehicle_number = models.CharField(max_length=80, blank=True, null=True)
    driver_name = models.CharField(max_length=120, blank=True, null=True)
    driver_phone = models.CharField(max_length=20, blank=True, null=True)

    other_transport_tracking_id = models.CharField(max_length=120, blank=True, null=True)

    dispatch_date = models.DateField(default=timezone.localdate)
    note = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.transport_type == "OWN":
            if not self.vehicle_number or not self.driver_name or not self.driver_phone:
                raise ValidationError("Vehicle number, driver name, and driver phone are required for own transport.")

        if self.transport_type == "OTHER":
            if not self.other_transport_tracking_id:
                raise ValidationError("Tracking ID is required for other transport.")

    def __str__(self):
        return f"Dispatch - Order #{self.order.id}"



    
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class CompanyAccount(models.Model):
    account_name = models.CharField(
        max_length=150,
        help_text="Example: Axis Bank Main Account"
    )

    bank_name = models.CharField(max_length=150)
    branch_name = models.CharField(max_length=150, blank=True, null=True)
    account_number = models.CharField(max_length=80)
    ifsc_code = models.CharField(max_length=30)
    account_holder_name = models.CharField(max_length=180)

    bank_address = models.TextField(
        blank=True,
        null=True,
        help_text="Bank branch address"
    )

    opening_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    current_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["account_name"]

    def __str__(self):
        return f"{self.account_name} - {self.bank_name}"


class CompanyPaymentIn(models.Model):
    SOURCE_CHOICES = (
        ("DEALER", "Dealer Payment"),
        ("CASH_TO_BANK", "Cash to Bank"),
        ("OWNER_DEPOSIT", "Owner Deposit"),
        ("OTHER", "Other"),
    )

    PAYMENT_MODE_CHOICES = (
        ("UPI", "UPI"),
        ("BANK", "Bank Transfer"),
        ("CHEQUE", "Cheque"),
        ("CASH", "Cash"),
    )

    account = models.ForeignKey(
        CompanyAccount,
        on_delete=models.PROTECT,
        related_name="payment_ins"
    )

    source_type = models.CharField(
        max_length=30,
        choices=SOURCE_CHOICES
    )

    dealer = models.ForeignKey(
        "Dealer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="company_payment_ins"
    )

    amount = models.DecimalField(max_digits=14, decimal_places=2)

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES
    )

    payment_date = models.DateField(default=timezone.localdate)

    reference_number = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="UPI reference / bank transaction number"
    )

    cheque_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    payment_screenshot = models.ImageField(
        upload_to="company_payment_in/",
        blank=True,
        null=True
    )

    reason = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-payment_date", "-created_at"]

    def clean(self):
        if self.amount and self.amount <= 0:
            raise ValidationError("Amount must be greater than zero.")

        if self.source_type == "DEALER" and not self.dealer:
            raise ValidationError("Please select dealer for dealer payment.")

        if self.payment_mode == "UPI" and not self.reference_number:
            raise ValidationError("UPI reference number is required.")

        if self.payment_mode == "BANK" and not self.reference_number:
            raise ValidationError("Bank transaction number is required.")

        if self.payment_mode == "CHEQUE" and not self.cheque_number:
            raise ValidationError("Cheque number is required.")

        if not self.reason:
            raise ValidationError("Reason is required.")

    def __str__(self):
        return f"Payment In ₹{self.amount} - {self.get_source_type_display()}"


class CompanyPaymentOut(models.Model):
    EXPENSE_TYPE_CHOICES = (
        ("TRANSPORT", "Transport"),
        ("PURCHASE", "Purchase"),
        ("RENT", "Rent"),
        ("BANK_CHARGES", "Bank Charges"),
        ("SALARY", "Salary"),
        ("OFFICE_EXPENSES", "Office Expenses"),
        ("OTHER", "Other"),
    )

    PAYMENT_MODE_CHOICES = (
        ("UPI", "UPI"),
        ("BANK", "Bank Transfer"),
        ("CHEQUE", "Cheque"),
        ("CASH", "Cash"),
    )

    account = models.ForeignKey(
        CompanyAccount,
        on_delete=models.PROTECT,
        related_name="payment_outs"
    )

    expense_type = models.CharField(
        max_length=40,
        choices=EXPENSE_TYPE_CHOICES
    )

    payee_name = models.CharField(
        max_length=180,
        blank=True,
        null=True,
        help_text="Person/vendor/company name"
    )

    amount = models.DecimalField(max_digits=14, decimal_places=2)

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES
    )

    payment_date = models.DateField(default=timezone.localdate)

    reference_number = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="UPI reference / bank transaction number"
    )

    cheque_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    payment_screenshot = models.ImageField(
        upload_to="company_payment_out/",
        blank=True,
        null=True
    )

    reason = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-payment_date", "-created_at"]

    def clean(self):
        if self.amount and self.amount <= 0:
            raise ValidationError("Amount must be greater than zero.")

        if self.payment_mode == "UPI" and not self.reference_number:
            raise ValidationError("UPI reference number is required.")

        if self.payment_mode == "BANK" and not self.reference_number:
            raise ValidationError("Bank transaction number is required.")

        if self.payment_mode == "CHEQUE" and not self.cheque_number:
            raise ValidationError("Cheque number is required.")

        if not self.reason:
            raise ValidationError("Reason is required.")

    def __str__(self):
        return f"Payment Out ₹{self.amount} - {self.get_expense_type_display()}"


class CreditNoteNumberSequence(models.Model):
    financial_year = models.CharField(max_length=10, unique=True)
    last_number = models.PositiveIntegerField(default=0)

    def next_credit_note_number(self):
        self.last_number += 1
        self.save(update_fields=["last_number"])
        return f"CN/{self.financial_year}/{self.last_number:04d}"

    def __str__(self):
        return f"{self.financial_year} - {self.last_number}"


class SalesReturnCreditNote(models.Model):
    STATUS_CHOICES = (
        ("RELEASED", "Released"),
        ("CANCELLED", "Cancelled"),
    )

    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.PROTECT,
        related_name="sales_return_credit_notes"
    )

    invoice = models.ForeignKey(
        DealerInvoice,
        on_delete=models.PROTECT,
        related_name="sales_return_credit_notes"
    )

    order = models.ForeignKey(
        DealerOrder,
        on_delete=models.PROTECT,
        related_name="sales_return_credit_notes"
    )

    credit_note_number = models.CharField(
        max_length=100,
        unique=True,
        blank=True
    )

    return_date = models.DateField(default=timezone.localdate)

    reason = models.TextField()

    subtotal_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    gst_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    grand_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="RELEASED"
    )
    show_to_dealer = models.BooleanField(
        default=False,
        help_text="Only if enabled, dealer can see this credit note"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_credit_notes"
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_credit_notes"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-return_date", "-id"]

    def __str__(self):
        return self.credit_note_number or f"Credit Note #{self.id}"

    def save(self, *args, **kwargs):
        if not self.credit_note_number:
            today = timezone.localdate()

            if today.month >= 4:
                fy_start = today.year
                fy_end = today.year + 1
            else:
                fy_start = today.year - 1
                fy_end = today.year

            fy_text = f"{str(fy_start)[-2:]}-{str(fy_end)[-2:]}"

            sequence, created = CreditNoteNumberSequence.objects.get_or_create(
                financial_year=fy_text
            )

            self.credit_note_number = sequence.next_credit_note_number()

        super().save(*args, **kwargs)

    def recalculate_totals(self, save=True):
        subtotal = Decimal("0.00")
        gst_total = Decimal("0.00")
        grand_total = Decimal("0.00")

        for item in self.items.all():
            subtotal += item.taxable_amount or Decimal("0.00")
            gst_total += item.gst_amount or Decimal("0.00")
            grand_total += item.total_amount or Decimal("0.00")

        self.subtotal_amount = subtotal
        self.gst_amount = gst_total
        self.grand_total = grand_total

        if save:
            self.save(update_fields=[
                "subtotal_amount",
                "gst_amount",
                "grand_total",
                "updated_at",
            ])


class SalesReturnCreditNoteItem(models.Model):
    credit_note = models.ForeignKey(
        SalesReturnCreditNote,
        on_delete=models.CASCADE,
        related_name="items"
    )

    order_item = models.ForeignKey(
        DealerOrderItem,
        on_delete=models.PROTECT,
        related_name="sales_return_items"
    )

    product_pack = models.ForeignKey(
        ProductPackSize,
        on_delete=models.PROTECT,
        related_name="sales_return_items"
    )

    product_name_snapshot = models.CharField(max_length=180)
    pack_label_snapshot = models.CharField(max_length=80)

    sold_quantity_boxes = models.PositiveIntegerField(default=0)
    return_quantity_boxes = models.PositiveIntegerField(default=1)

    units_per_box = models.PositiveIntegerField(default=1)
    total_return_units = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    unit_name = models.CharField(max_length=30, default="Pcs")

    price_per_box = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    gst_percent = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00")
    )

    taxable_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    gst_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )

    hsn_code = models.CharField(max_length=50, blank=True, null=True)
    batch_no = models.CharField(max_length=80, blank=True, null=True)
    mfg_date = models.CharField(max_length=20, blank=True, null=True)
    expiry_date = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ["id"]

    def clean(self):
        if self.return_quantity_boxes <= 0:
            raise ValidationError("Return quantity must be greater than zero.")

        if self.sold_quantity_boxes and self.return_quantity_boxes > self.sold_quantity_boxes:
            raise ValidationError("Return quantity cannot be greater than sold quantity.")

        if self.price_per_box < 0:
            raise ValidationError("Taking price cannot be negative.")

    def save(self, *args, **kwargs):
        self.full_clean()

        self.units_per_box = self.order_item.units_per_box
        self.unit_name = self.order_item.unit_name

        self.total_return_units = (
            Decimal(str(self.product_pack.pack_size))
            * Decimal(self.units_per_box)
            * Decimal(self.return_quantity_boxes)
        )

        gross_amount = self.price_per_box * Decimal(self.return_quantity_boxes)
        gst_percent = self.gst_percent or Decimal("0.00")

        if gst_percent > 0:
            self.taxable_amount = (gross_amount * Decimal("100.00")) / (Decimal("100.00") + gst_percent)
            self.gst_amount = gross_amount - self.taxable_amount
        else:
            self.taxable_amount = gross_amount
            self.gst_amount = Decimal("0.00")

        self.total_amount = gross_amount

        super().save(*args, **kwargs)


class EmployeeAttendance(models.Model):
    VEHICLE_CHOICES = (
        ("BIKE", "Bike"),
        ("CAR", "Car"),
        ("PUBLIC", "Public Vehicle"),
        ("COMPANY", "Company Vehicle"),
    )

    STATUS_CHOICES = (
        ("CLOCKED_IN", "Clocked In"),
        ("PENDING_MANAGER", "Pending Manager Approval"),
        ("MANAGER_APPROVED", "Manager Approved"),
        ("HR_APPROVED", "HR Approved"),
        ("RELEASED", "Released"),
        ("REJECTED", "Rejected"),
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    attendance_date = models.DateField(default=timezone.localdate)

    clock_in_at = models.DateTimeField(null=True, blank=True)
    clock_in_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    clock_in_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    clock_out_at = models.DateTimeField(null=True, blank=True)
    clock_out_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    clock_out_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    clock_in_odometer_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Odometer reading entered by employee during clock-in"
    )

    clock_out_odometer_reading = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Odometer reading entered by employee during clock-out"
    )

    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES, null=True, blank=True)

    dealers_connected_count = models.PositiveIntegerField(default=0)
    dealer_visit_image_1 = models.ImageField(upload_to="attendance/dealer_visits/", null=True, blank=True)
    dealer_visit_image_2 = models.ImageField(upload_to="attendance/dealer_visits/", null=True, blank=True)

    public_vehicle_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    public_vehicle_bill = models.FileField(upload_to="attendance/public_vehicle_bills/", null=True, blank=True)

    system_distance_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    manager_approved_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    ta_rate_per_km = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    ta_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    da_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_claim_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="CLOCKED_IN")

    manager_approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="manager_approved_attendance"
    )
    manager_approved_at = models.DateTimeField(null=True, blank=True)
    manager_remarks = models.TextField(blank=True)

    hr_approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hr_approved_attendance"
    )
    hr_approved_at = models.DateTimeField(null=True, blank=True)
    hr_remarks = models.TextField(blank=True)

    released_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="released_attendance_claims"
    )
    released_at = models.DateTimeField(null=True, blank=True)
    release_remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-attendance_date", "-clock_in_at"]

    def __str__(self):
        return f"{self.employee.username} - {self.attendance_date}"

    @property
    def is_clocked_out(self):
        return self.clock_out_at is not None


class EmployeeGPSTrack(models.Model):
    attendance = models.ForeignKey(
        EmployeeAttendance,
        on_delete=models.CASCADE,
        related_name="gps_points"
    )
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["recorded_at"]


class EmployeeLeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = (
        ("PAID", "Paid Leave"),
        ("SICK", "Sick Leave"),
        ("OTHER", "Other Leave"),
        ("UNPAID", "Unpaid Leave"),
    )

    DAY_TYPE_CHOICES = (
        ("FULL_DAY", "Full Day"),
        ("HALF_DAY", "Half Day"),
    )

    STATUS_CHOICES = (
        ("PENDING", "Pending Manager Approval"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="leave_requests"
    )

    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    day_type = models.CharField(max_length=20, choices=DAY_TYPE_CHOICES, default="FULL_DAY")

    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_leave_requests"
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    manager_remarks = models.TextField(blank=True)

    salary_deduction_required = models.BooleanField(default=False)
    deduction_days = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def calculate_days(self):
        total_days = (self.to_date - self.from_date).days + 1

        if self.day_type == "HALF_DAY":
            return Decimal("0.5")

        return Decimal(str(total_days))

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type}"



class EmployeePayslip(models.Model):
    STATUS_CHOICES = (
        ("DRAFT", "Draft / Review Pending"),
        ("RELEASED", "Released"),
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payslips"
    )

    payslip_number = models.CharField(max_length=80, unique=True)

    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    allowance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    leave_deduction_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_deduction_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pf_deduction_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    insurance_deduction_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    employee_dob = models.DateField(null=True, blank=True)
    employee_pan_number = models.CharField(max_length=10, blank=True, null=True)

    employee_bank_name = models.CharField(max_length=120, blank=True, null=True)
    employee_bank_account_number = models.CharField(max_length=40, blank=True, null=True)
    employee_bank_ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    employee_bank_account_holder_name = models.CharField(max_length=150, blank=True, null=True)

    employee_pf_uan_number = models.CharField(max_length=30, blank=True, null=True)
    employee_pf_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00")
    )

    employee_insurance_provider_name = models.CharField(max_length=150, blank=True, null=True)
    employee_insurance_policy_number = models.CharField(max_length=80, blank=True, null=True)

    gross_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    remarks = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")

    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_payslips"
    )
    generated_at = models.DateTimeField(auto_now_add=True)

    released_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="released_payslips"
    )
    released_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("employee", "month", "year")
        ordering = ["-year", "-month", "employee__first_name"]

    def __str__(self):
        return f"{self.employee.username} - {self.month}/{self.year}"

    @property
    def month_name(self):
        return calendar.month_name[self.month]

    def calculate_totals(self):
        self.gross_salary = (
            (self.basic_salary or Decimal("0.00"))
            + (self.allowance_amount or Decimal("0.00"))
        )

        self.total_deductions = (
            (self.leave_deduction_amount or Decimal("0.00"))
            + (self.other_deduction_amount or Decimal("0.00"))
            + (self.pf_deduction_amount or Decimal("0.00"))
            + (self.insurance_deduction_amount or Decimal("0.00"))
        )

        self.net_salary = self.gross_salary - self.total_deductions

        if self.net_salary < 0:
            self.net_salary = Decimal("0.00")

    def save(self, *args, **kwargs):
        self.calculate_totals()
        super().save(*args, **kwargs)



class EmployeeExtraWorkDayRequest(models.Model):
    STATUS_CHOICES = (
        ("PENDING_MANAGER", "Pending Manager Approval"),
        ("MANAGER_APPROVED_PENDING_HR", "Manager Approved - Pending HR"),
        ("HR_APPROVED", "HR Approved / Extra Leave Added"),
        ("REJECTED", "Rejected"),
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="extra_work_day_requests"
    )

    work_date = models.DateField()
    reason = models.TextField()

    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default="PENDING_MANAGER"
    )

    manager_approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="manager_approved_extra_work_days"
    )
    manager_approved_at = models.DateTimeField(null=True, blank=True)
    manager_remarks = models.TextField(blank=True)

    hr_approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hr_approved_extra_work_days"
    )
    hr_approved_at = models.DateTimeField(null=True, blank=True)
    hr_remarks = models.TextField(blank=True)

    extra_leave_added = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-work_date", "-created_at"]
        unique_together = ("employee", "work_date")

    def __str__(self):
        return f"{self.employee.username} - {self.work_date}"


class AssetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code_prefix = models.CharField(
        max_length=10,
        unique=True,
        help_text="Example: LAP for Laptop, MOB for Mobile, UNI for Uniform"
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.code_prefix = str(self.code_prefix or "").upper().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code_prefix})"


class AssetItem(models.Model):
    STATUS_CHOICES = (
        ("AVAILABLE", "Available"),
        ("ASSIGNED", "Assigned"),
        ("DAMAGED", "Damaged"),
        ("LOST", "Lost"),
        ("RETIRED", "Retired"),
    )

    category = models.ForeignKey(
        AssetCategory,
        on_delete=models.PROTECT,
        related_name="assets"
    )

    asset_code = models.CharField(max_length=50, unique=True)

    name = models.CharField(max_length=150)
    brand = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=120, blank=True)

    description = models.TextField(blank=True)

    purchase_date = models.DateField(null=True, blank=True)
    purchase_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE"
    )

    current_employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_assets"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_assets"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category__name", "asset_code"]

    def __str__(self):
        return f"{self.asset_code} - {self.name}"


class AssetAssignment(models.Model):
    asset = models.ForeignKey(
        AssetItem,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="asset_assignments"
    )

    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asset_given_by"
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    handover_image = models.ImageField(
        upload_to="asset_handover_images/",
        help_text="Photo captured while giving asset"
    )

    handover_note = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    returned_at = models.DateTimeField(null=True, blank=True)
    returned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asset_returns"
    )
    return_note = models.TextField(blank=True)

    class Meta:
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.asset.asset_code} assigned to {self.employee}"




import re
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.utils import timezone


def normalize_indian_mobile(value):
    digits = re.sub(r"\D", "", str(value or ""))

    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[-10:]

    if len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]

    if not re.fullmatch(r"[6-9]\d{9}", digits):
        raise ValidationError("Enter valid Indian 10 digit mobile number.")

    return digits


class DealerPointSetting(models.Model):
    farmer_points = models.PositiveIntegerField(default=5)
    rupees_per_point = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("1.00"))

    minimum_money_redemption_points = models.PositiveIntegerField(default=100)
    minimum_product_redemption_points = models.PositiveIntegerField(default=100)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dealer Point Setting"
        verbose_name_plural = "Dealer Point Settings"

    def __str__(self):
        return f"{self.farmer_points} points per farmer | ₹{self.rupees_per_point} per point"

    @classmethod
    def get_settings(cls):
        setting = cls.objects.filter(is_active=True).first()
        if not setting:
            setting = cls.objects.create(
                farmer_points=5,
                rupees_per_point=Decimal("1.00"),
                minimum_money_redemption_points=100,
                minimum_product_redemption_points=100,
                is_active=True,
            )
        return setting


class FarmerData(models.Model):
    dealer = models.ForeignKey(
        "Dealer",
        on_delete=models.CASCADE,
        related_name="farmer_data"
    )

    farmer_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=10, unique=True)
    place = models.CharField(max_length=255)

    points_awarded = models.PositiveIntegerField(default=5)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_farmer_data"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        self.mobile_number = normalize_indian_mobile(self.mobile_number)

    def save(self, *args, **kwargs):
        self.mobile_number = normalize_indian_mobile(self.mobile_number)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.farmer_name} - {self.mobile_number}"


class DealerPointLedger(models.Model):
    TRANSACTION_CHOICES = (
        ("CREDIT", "Credit"),
        ("DEBIT", "Debit"),
    )

    dealer = models.ForeignKey(
        "Dealer",
        on_delete=models.CASCADE,
        related_name="point_ledger"
    )

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    points = models.PositiveIntegerField()

    farmer_data = models.ForeignKey(
        FarmerData,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="point_entries"
    )

    redemption_request = models.ForeignKey(
        "DealerPointRedemptionRequest",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="point_entries"
    )

    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.dealer.firm_name} - {self.transaction_type} - {self.points}"


class DealerPointProductRule(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="point_redemption_rules"
    )

    pack_size = models.ForeignKey(
        "ProductPackSize",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="point_redemption_rules"
    )

    title = models.CharField(max_length=150, blank=True)
    points_required = models.PositiveIntegerField()
    free_quantity = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["product__name", "points_required"]

    def __str__(self):
        return f"{self.product.name} - {self.points_required} points"


class DealerPointRedemptionRequest(models.Model):
    REDEMPTION_TYPE_CHOICES = (
        ("MONEY", "Money"),
        ("PRODUCT", "Product / Free Quantity"),
    )

    STATUS_CHOICES = (
        ("PENDING_SALES_OFFICER", "Pending Sales Officer"),
        ("PENDING_ASM", "Pending ASM"),
        ("PENDING_ACCOUNTANT", "Pending Accountant"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    dealer = models.ForeignKey(
        "Dealer",
        on_delete=models.CASCADE,
        related_name="point_redemption_requests"
    )

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dealer_point_redemptions_created"
    )

    redemption_type = models.CharField(max_length=20, choices=REDEMPTION_TYPE_CHOICES)

    points_requested = models.PositiveIntegerField()
    money_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    product_rule = models.ForeignKey(
        DealerPointProductRule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="redemption_requests"
    )

    request_quantity = models.PositiveIntegerField(default=1)
    requested_free_quantity = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default="PENDING_SALES_OFFICER"
    )

    sales_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales_officer_point_redemptions"
    )

    asm = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asm_point_redemptions"
    )

    accountant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accountant_point_redemptions"
    )

    sales_officer_approved_at = models.DateTimeField(null=True, blank=True)
    asm_approved_at = models.DateTimeField(null=True, blank=True)
    accountant_approved_at = models.DateTimeField(null=True, blank=True)

    rejected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rejected_point_redemptions"
    )

    rejected_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.dealer.firm_name} - {self.redemption_type} - {self.points_requested} points"




# ==========================================================
# PURCHASE + INVENTORY + PRODUCTION MODULE
# ==========================================================

PURCHASE_UNIT_CHOICES = (
    ("GRAM", "Gram"),
    ("KG", "Kg"),
    ("ML", "ML"),
    ("LITRE", "Litre"),
    ("PIECE", "Piece"),
    ("BAG", "Bag"),
    ("BOX", "Box"),
    ("BOTTLE", "Bottle"),
    ("PACKET", "Packet"),
    ("CARTON", "Carton"),
)

CONVERTIBLE_UNITS = {
    "GRAM": ("WEIGHT", Decimal("0.001")),
    "KG": ("WEIGHT", Decimal("1")),
    "ML": ("VOLUME", Decimal("0.001")),
    "LITRE": ("VOLUME", Decimal("1")),
}


def convert_purchase_quantity(quantity, from_unit, to_unit):
    quantity = Decimal(str(quantity or "0"))

    if from_unit == to_unit:
        return quantity

    from_data = CONVERTIBLE_UNITS.get(from_unit)
    to_data = CONVERTIBLE_UNITS.get(to_unit)

    if not from_data or not to_data:
        raise ValidationError(f"Cannot convert {from_unit} to {to_unit}.")

    if from_data[0] != to_data[0]:
        raise ValidationError(f"Cannot convert {from_unit} to {to_unit}.")

    return (quantity * from_data[1]) / to_data[1]


class PurchaseType(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PurchaseParty(models.Model):
    PARTY_TYPE_CHOICES = (
        ("SUPPLIER", "Supplier"),
        ("MANUFACTURER", "Manufacturer"),
        ("DISTRIBUTOR", "Distributor"),
        ("OTHER", "Other"),
    )

    party_name = models.CharField(max_length=180)
    party_type = models.CharField(max_length=30, choices=PARTY_TYPE_CHOICES, default="SUPPLIER")

    contact_person = models.CharField(max_length=120, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    gst_number = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    opening_balance = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["party_name"]

    @property
    def purchase_total(self):
        total = Decimal("0.00")
        for bill in self.purchase_bills.all():
            total += bill.total_amount or Decimal("0.00")
        return total

    @property
    def paid_total(self):
        total = Decimal("0.00")
        for payment in self.purchase_payments.all():
            total += payment.amount or Decimal("0.00")
        return total

    @property
    def debit_note_total(self):
        total = Decimal("0.00")
        for debit_note in self.purchase_returns.filter(status="POSTED"):
            total += debit_note.total_amount or Decimal("0.00")
        return total

    @property
    def outstanding_amount(self):
        return self.opening_balance + self.purchase_total - self.paid_total - self.debit_note_total

    def __str__(self):
        return self.party_name


class InventoryItem(models.Model):
    ITEM_TYPE_CHOICES = (
        ("RAW_MATERIAL", "Raw Material"),
        ("PACKING_MATERIAL", "Packing Material"),
        ("SEMI_FINISHED", "Semi Finished"),
        ("FINISHED", "Finished"),
        ("OTHER", "Other"),
    )

    purchase_type = models.ForeignKey(
        PurchaseType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inventory_items"
    )

    item_type = models.CharField(max_length=40, choices=ITEM_TYPE_CHOICES, default="RAW_MATERIAL")

    name = models.CharField(max_length=180)
    sku_code = models.CharField(max_length=80, blank=True, null=True)

    stock_unit = models.CharField(max_length=20, choices=PURCHASE_UNIT_CHOICES, default="KG")

    stock_quantity = models.DecimalField(max_digits=14, decimal_places=3, default=Decimal("0.000"))
    average_purchase_price = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    minimum_stock_alert = models.DecimalField(max_digits=14, decimal_places=3, default=Decimal("0.000"))

    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    @property
    def stock_value(self):
        return self.stock_quantity * self.average_purchase_price

    @property
    def is_low_stock(self):
        return self.minimum_stock_alert > 0 and self.stock_quantity <= self.minimum_stock_alert

    def add_stock(self, quantity, unit, value_without_gst=Decimal("0.00"), user=None, note=""):
        quantity_in_stock_unit = convert_purchase_quantity(quantity, unit, self.stock_unit)

        if quantity_in_stock_unit <= 0:
            raise ValidationError("Stock quantity must be greater than zero.")

        old_quantity = self.stock_quantity or Decimal("0.000")
        old_price = self.average_purchase_price or Decimal("0.00")

        old_value = old_quantity * old_price
        new_value = Decimal(str(value_without_gst or "0.00"))

        final_quantity = old_quantity + quantity_in_stock_unit

        if final_quantity > 0:
            self.average_purchase_price = (old_value + new_value) / final_quantity

        self.stock_quantity = final_quantity
        self.save(update_fields=["stock_quantity", "average_purchase_price"])

        InventoryStockLedger.objects.create(
            inventory_item=self,
            transaction_type="IN",
            quantity=quantity_in_stock_unit,
            unit=self.stock_unit,
            balance_after=self.stock_quantity,
            created_by=user,
            note=note,
        )

    def reduce_stock(self, quantity, unit, user=None, note=""):
        quantity_in_stock_unit = convert_purchase_quantity(quantity, unit, self.stock_unit)

        if quantity_in_stock_unit <= 0:
            raise ValidationError("Stock quantity must be greater than zero.")

        if self.stock_quantity < quantity_in_stock_unit:
            raise ValidationError(
                f"Insufficient stock for {self.name}. Available {self.stock_quantity} {self.stock_unit}."
            )

        self.stock_quantity -= quantity_in_stock_unit
        self.save(update_fields=["stock_quantity"])

        InventoryStockLedger.objects.create(
            inventory_item=self,
            transaction_type="OUT",
            quantity=quantity_in_stock_unit,
            unit=self.stock_unit,
            balance_after=self.stock_quantity,
            created_by=user,
            note=note,
        )

    def __str__(self):
        return f"{self.name} - {self.stock_quantity} {self.get_stock_unit_display()}"


class InventoryStockLedger(models.Model):
    TRANSACTION_CHOICES = (
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
        ("PURCHASE", "Purchase"),
        ("PURCHASE_RETURN", "Purchase Return"),
        ("PRODUCTION_USE", "Production Use"),
        ("REPACK_USE", "Repack Use"),
        ("ADJUSTMENT", "Adjustment"),
    )

    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name="stock_ledger"
    )

    transaction_type = models.CharField(max_length=40, choices=TRANSACTION_CHOICES)

    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    unit = models.CharField(max_length=20, choices=PURCHASE_UNIT_CHOICES)

    balance_after = models.DecimalField(max_digits=14, decimal_places=3, default=Decimal("0.000"))

    reference_model = models.CharField(max_length=80, blank=True, null=True)
    reference_id = models.PositiveIntegerField(blank=True, null=True)

    note = models.CharField(max_length=255, blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ("DRAFT", "Draft"),
        ("ORDERED", "Ordered"),
        ("BILLED", "Billed"),
        ("CANCELLED", "Cancelled"),
    )

    order_number = models.CharField(max_length=50, unique=True, blank=True, null=True)

    party = models.ForeignKey(
        PurchaseParty,
        on_delete=models.PROTECT,
        related_name="purchase_orders"
    )

    purchase_type = models.ForeignKey(
        PurchaseType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchase_orders"
    )

    order_date = models.DateField(default=timezone.localdate)
    expected_delivery_date = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")

    subtotal_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    gst_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    note = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_purchase_orders"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_id = PurchaseOrder.objects.count() + 1
            self.order_number = f"PO{last_id:05d}"
        super().save(*args, **kwargs)

    def recalculate_totals(self):
        subtotal = Decimal("0.00")
        gst_total = Decimal("0.00")
        grand_total = Decimal("0.00")

        for item in self.items.all():
            item.calculate()
            item.save()
            subtotal += item.taxable_amount
            gst_total += item.gst_amount
            grand_total += item.total_amount

        self.subtotal_amount = subtotal
        self.gst_amount = gst_total
        self.total_amount = grand_total
        self.save(update_fields=["subtotal_amount", "gst_amount", "total_amount"])

    def __str__(self):
        return self.order_number or f"Purchase Order {self.id}"


class PurchaseOrderItem(models.Model):
    order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.PROTECT,
        related_name="purchase_order_items"
    )

    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    unit = models.CharField(max_length=20, choices=PURCHASE_UNIT_CHOICES)

    purchase_price = models.DecimalField(max_digits=14, decimal_places=2)
    gst_percent = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("0.00"))

    taxable_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    gst_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    def calculate(self):
        self.taxable_amount = (self.quantity or Decimal("0.000")) * (self.purchase_price or Decimal("0.00"))
        self.gst_amount = (self.taxable_amount * (self.gst_percent or Decimal("0.00"))) / Decimal("100.00")
        self.total_amount = self.taxable_amount + self.gst_amount

    def save(self, *args, **kwargs):
        self.calculate()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventory_item.name} - {self.quantity} {self.unit}"


class PurchaseBill(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ("UNPAID", "Unpaid"),
        ("PARTIAL", "Partial Paid"),
        ("PAID", "Paid"),
    )

    bill_number = models.CharField(max_length=80)
    bill_date = models.DateField(default=timezone.localdate)

    party = models.ForeignKey(
        PurchaseParty,
        on_delete=models.PROTECT,
        related_name="purchase_bills"
    )

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchase_bills"
    )

    subtotal_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    gst_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    paid_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    return_credit_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    balance_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="UNPAID")

    stock_added = models.BooleanField(default=False)

    bill_file = models.FileField(upload_to="purchase_bills/", blank=True, null=True)

    note = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_purchase_bills"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
        unique_together = ("party", "bill_number")

    def recalculate_totals(self):
        subtotal = Decimal("0.00")
        gst_total = Decimal("0.00")
        grand_total = Decimal("0.00")

        for item in self.items.all():
            item.calculate()
            item.save()
            subtotal += item.taxable_amount
            gst_total += item.gst_amount
            grand_total += item.total_amount

        self.subtotal_amount = subtotal
        self.gst_amount = gst_total
        self.total_amount = grand_total
        self.update_payment_status(save=False)

        self.save(update_fields=[
            "subtotal_amount",
            "gst_amount",
            "total_amount",
            "balance_amount",
            "payment_status",
        ])

    def update_payment_status(self, save=True):
        self.balance_amount = self.total_amount - self.paid_amount - self.return_credit_amount

        if self.balance_amount < 0:
            self.balance_amount = Decimal("0.00")

        if self.balance_amount <= 0:
            self.payment_status = "PAID"
        elif self.paid_amount > 0:
            self.payment_status = "PARTIAL"
        else:
            self.payment_status = "UNPAID"

        if save:
            self.save(update_fields=["paid_amount", "return_credit_amount", "balance_amount", "payment_status"])

    def recalculate_paid_amount(self):
        total_paid = Decimal("0.00")

        for payment in self.payments.all():
            total_paid += payment.amount or Decimal("0.00")

        self.paid_amount = total_paid
        self.update_payment_status(save=True)

    def apply_stock_in(self, user=None):
        if self.stock_added:
            raise ValidationError("Stock already added for this purchase bill.")

        for item in self.items.all():
            item.inventory_item.add_stock(
                quantity=item.quantity,
                unit=item.unit,
                value_without_gst=item.taxable_amount,
                user=user,
                note=f"Purchase Bill {self.bill_number}"
            )

        self.stock_added = True
        self.save(update_fields=["stock_added"])

        if self.purchase_order:
            self.purchase_order.status = "BILLED"
            self.purchase_order.save(update_fields=["status"])

    def __str__(self):
        return f"{self.bill_number} - {self.party.party_name}"


class PurchaseBillItem(models.Model):
    bill = models.ForeignKey(
        PurchaseBill,
        on_delete=models.CASCADE,
        related_name="items"
    )

    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.PROTECT,
        related_name="purchase_bill_items"
    )

    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    unit = models.CharField(max_length=20, choices=PURCHASE_UNIT_CHOICES)

    purchase_price = models.DecimalField(max_digits=14, decimal_places=2)
    gst_percent = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("0.00"))

    taxable_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    gst_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    def clean(self):
        convert_purchase_quantity(self.quantity, self.unit, self.inventory_item.stock_unit)

    def calculate(self):
        self.taxable_amount = (self.quantity or Decimal("0.000")) * (self.purchase_price or Decimal("0.00"))
        self.gst_amount = (self.taxable_amount * (self.gst_percent or Decimal("0.00"))) / Decimal("100.00")
        self.total_amount = self.taxable_amount + self.gst_amount

    def save(self, *args, **kwargs):
        self.calculate()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventory_item.name} - {self.quantity} {self.unit}"


class PurchasePaymentOut(models.Model):
    PAYMENT_MODE_CHOICES = (
        ("CASH", "Cash"),
        ("UPI", "UPI"),
        ("BANK", "Bank Transfer"),
        ("CHEQUE", "Cheque"),
    )

    party = models.ForeignKey(
        PurchaseParty,
        on_delete=models.PROTECT,
        related_name="purchase_payments"
    )

    bill = models.ForeignKey(
        PurchaseBill,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments"
    )

    payment_date = models.DateField(default=timezone.localdate)
    amount = models.DecimalField(max_digits=14, decimal_places=2)

    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES)

    reference_number = models.CharField(max_length=120, blank=True, null=True)
    cheque_number = models.CharField(max_length=80, blank=True, null=True)
    payment_screenshot = models.FileField(upload_to="purchase_payments/", blank=True, null=True)

    note = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_purchase_payments"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Payment amount must be greater than zero.")

        if self.bill and self.amount > self.bill.balance_amount:
            raise ValidationError("Payment amount cannot be greater than purchase bill pending balance.")

        if self.payment_mode in ["UPI", "BANK"] and not self.reference_number:
            raise ValidationError("Reference number is required.")

        if self.payment_mode == "CHEQUE" and not self.cheque_number:
            raise ValidationError("Cheque number is required.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.bill:
            self.bill.recalculate_paid_amount()

    def delete(self, *args, **kwargs):
        bill = self.bill
        super().delete(*args, **kwargs)

        if bill:
            bill.recalculate_paid_amount()

    def __str__(self):
        return f"{self.party.party_name} - ₹{self.amount}"


class PurchaseReturnOrder(models.Model):
    STATUS_CHOICES = (
        ("DRAFT", "Draft"),
        ("POSTED", "Posted"),
        ("CANCELLED", "Cancelled"),
    )

    debit_note_number = models.CharField(max_length=80, unique=True, blank=True, null=True)

    party = models.ForeignKey(
        PurchaseParty,
        on_delete=models.PROTECT,
        related_name="purchase_returns"
    )

    bill = models.ForeignKey(
        PurchaseBill,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchase_returns"
    )

    return_date = models.DateField(default=timezone.localdate)
    reason = models.TextField()

    subtotal_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    gst_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")
    stock_reduced = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_purchase_returns"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.debit_note_number:
            last_id = PurchaseReturnOrder.objects.count() + 1
            self.debit_note_number = f"DN{last_id:05d}"
        super().save(*args, **kwargs)

    def recalculate_totals(self):
        subtotal = Decimal("0.00")
        gst_total = Decimal("0.00")
        grand_total = Decimal("0.00")

        for item in self.items.all():
            item.calculate()
            item.save()
            subtotal += item.taxable_amount
            gst_total += item.gst_amount
            grand_total += item.total_amount

        self.subtotal_amount = subtotal
        self.gst_amount = gst_total
        self.total_amount = grand_total
        self.save(update_fields=["subtotal_amount", "gst_amount", "total_amount"])

    def apply_return_stock(self, user=None):
        if self.stock_reduced:
            raise ValidationError("Stock already reduced for this debit note.")

        for item in self.items.all():
            item.inventory_item.reduce_stock(
                quantity=item.quantity,
                unit=item.unit,
                user=user,
                note=f"Purchase Return / Debit Note {self.debit_note_number}"
            )

        self.status = "POSTED"
        self.stock_reduced = True
        self.save(update_fields=["status", "stock_reduced"])

        if self.bill:
            self.bill.return_credit_amount += self.total_amount
            self.bill.update_payment_status(save=True)

    def __str__(self):
        return self.debit_note_number or f"Debit Note {self.id}"


class PurchaseReturnItem(models.Model):
    purchase_return = models.ForeignKey(
        PurchaseReturnOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.PROTECT,
        related_name="purchase_return_items"
    )

    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    unit = models.CharField(max_length=20, choices=PURCHASE_UNIT_CHOICES)

    return_price = models.DecimalField(max_digits=14, decimal_places=2)
    gst_percent = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("0.00"))

    taxable_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    gst_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    def clean(self):
        convert_purchase_quantity(self.quantity, self.unit, self.inventory_item.stock_unit)

    def calculate(self):
        self.taxable_amount = (self.quantity or Decimal("0.000")) * (self.return_price or Decimal("0.00"))
        self.gst_amount = (self.taxable_amount * (self.gst_percent or Decimal("0.00"))) / Decimal("100.00")
        self.total_amount = self.taxable_amount + self.gst_amount

    def save(self, *args, **kwargs):
        self.calculate()
        super().save(*args, **kwargs)


class ProductionRecipe(models.Model):
    name = models.CharField(max_length=180)

    output_product_pack = models.ForeignKey(
        ProductPackSize,
        on_delete=models.PROTECT,
        related_name="production_recipes"
    )

    output_boxes = models.PositiveIntegerField(
        default=1,
        help_text="How many final product boxes this recipe creates"
    )

    note = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} → {self.output_product_pack}"


class ProductionRecipeItem(models.Model):
    recipe = models.ForeignKey(
        ProductionRecipe,
        on_delete=models.CASCADE,
        related_name="recipe_items"
    )

    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.PROTECT,
        related_name="used_in_recipes"
    )

    quantity_required = models.DecimalField(max_digits=14, decimal_places=3)
    unit = models.CharField(max_length=20, choices=PURCHASE_UNIT_CHOICES)

    def __str__(self):
        return f"{self.inventory_item.name} - {self.quantity_required} {self.unit}"


class ProductionBatch(models.Model):
    STATUS_CHOICES = (
        ("DRAFT", "Draft"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    batch_number = models.CharField(max_length=80, unique=True, blank=True, null=True)

    recipe = models.ForeignKey(
        ProductionRecipe,
        on_delete=models.PROTECT,
        related_name="production_batches"
    )

    production_date = models.DateField(default=timezone.localdate)

    output_product_pack = models.ForeignKey(
        ProductPackSize,
        on_delete=models.PROTECT,
        related_name="production_outputs"
    )

    output_boxes = models.PositiveIntegerField(default=1)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")
    stock_applied = models.BooleanField(default=False)

    note = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_production_batches"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.batch_number:
            last_id = ProductionBatch.objects.count() + 1
            self.batch_number = f"PB{last_id:05d}"

        if not self.output_product_pack_id and self.recipe_id:
            self.output_product_pack = self.recipe.output_product_pack

        super().save(*args, **kwargs)

    def apply_production(self, user=None):
        if self.stock_applied:
            raise ValidationError("Production stock already applied.")

        if self.output_boxes <= 0:
            raise ValidationError("Output boxes must be greater than zero.")

        recipe_output_boxes = Decimal(str(self.recipe.output_boxes or 1))
        multiplier = Decimal(str(self.output_boxes)) / recipe_output_boxes

        for recipe_item in self.recipe.recipe_items.all():
            needed_qty = recipe_item.quantity_required * multiplier

            recipe_item.inventory_item.reduce_stock(
                quantity=needed_qty,
                unit=recipe_item.unit,
                user=user,
                note=f"Production Batch {self.batch_number}"
            )

            InventoryStockLedger.objects.filter(
                inventory_item=recipe_item.inventory_item
            ).order_by("-id").update(
                transaction_type="PRODUCTION_USE",
                reference_model="ProductionBatch",
                reference_id=self.id
            )

        self.output_product_pack.stock_boxes += int(self.output_boxes)
        self.output_product_pack.save(update_fields=["stock_boxes"])

        self.status = "COMPLETED"
        self.stock_applied = True
        self.save(update_fields=["status", "stock_applied"])

    def __str__(self):
        return self.batch_number or f"Production Batch {self.id}"


class RepackingBatch(models.Model):
    STATUS_CHOICES = (
        ("DRAFT", "Draft"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    batch_number = models.CharField(max_length=80, unique=True, blank=True, null=True)

    repack_date = models.DateField(default=timezone.localdate)

    source_inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.PROTECT,
        related_name="repacking_sources"
    )

    source_quantity = models.DecimalField(max_digits=14, decimal_places=3)
    source_unit = models.CharField(max_length=20, choices=PURCHASE_UNIT_CHOICES)

    destination_product_pack = models.ForeignKey(
        ProductPackSize,
        on_delete=models.PROTECT,
        related_name="repacking_outputs"
    )

    destination_boxes = models.PositiveIntegerField(
        help_text="How many new sellable boxes/packs are created"
    )

    packing_material = models.ForeignKey(
        InventoryItem,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="repacking_packing_materials"
    )

    packing_material_quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        default=Decimal("0.000")
    )

    packing_material_unit = models.CharField(
        max_length=20,
        choices=PURCHASE_UNIT_CHOICES,
        default="PIECE"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")
    stock_applied = models.BooleanField(default=False)

    note = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_repacking_batches"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.batch_number:
            last_id = RepackingBatch.objects.count() + 1
            self.batch_number = f"RB{last_id:05d}"
        super().save(*args, **kwargs)

    def apply_repacking(self, user=None):
        if self.stock_applied:
            raise ValidationError("Repacking stock already applied.")

        self.source_inventory_item.reduce_stock(
            quantity=self.source_quantity,
            unit=self.source_unit,
            user=user,
            note=f"Repacking Batch {self.batch_number}"
        )

        InventoryStockLedger.objects.filter(
            inventory_item=self.source_inventory_item
        ).order_by("-id").update(
            transaction_type="REPACK_USE",
            reference_model="RepackingBatch",
            reference_id=self.id
        )

        if self.packing_material and self.packing_material_quantity > 0:
            self.packing_material.reduce_stock(
                quantity=self.packing_material_quantity,
                unit=self.packing_material_unit,
                user=user,
                note=f"Packing material used in Repacking Batch {self.batch_number}"
            )

        self.destination_product_pack.stock_boxes += int(self.destination_boxes)
        self.destination_product_pack.save(update_fields=["stock_boxes"])

        self.status = "COMPLETED"
        self.stock_applied = True
        self.save(update_fields=["status", "stock_applied"])

    def __str__(self):
        return self.batch_number or f"Repacking Batch {self.id}"



# ==========================================================
# MAIN WAREHOUSE STOCK TRANSFER - MODELS
# Paste this at the bottom of core/models.py
# Then run: python manage.py makemigrations && python manage.py migrate
# ==========================================================

from django.conf import settings
from django.db import models


class ProductStockTransfer(models.Model):
    product_pack = models.ForeignKey(
        "ProductPackSize",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_transfers",
    )

    product = models.ForeignKey(
        "Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_transfers",
    )

    from_warehouse = models.ForeignKey(
        "Warehouse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_transfers_out",
    )

    to_warehouse = models.ForeignKey(
        "Warehouse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_transfers_in",
    )

    quantity_boxes = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    before_main_stock = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    after_main_stock = models.DecimalField(max_digits=14, decimal_places=3, default=0)

    note = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_product_stock_transfers",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        product_name = self.product.name if self.product else "Product"
        from_name = self.from_warehouse.name if self.from_warehouse else "-"
        to_name = self.to_warehouse.name if self.to_warehouse else "-"
        return f"{product_name}: {self.quantity_boxes} from {from_name} to {to_name}"


