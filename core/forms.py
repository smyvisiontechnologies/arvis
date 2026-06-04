from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from decimal import Decimal
from django import forms
from django.contrib.auth import get_user_model
from .models import  *
import calendar
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.utils import timezone
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms import inlineformset_factory
from django import forms
from django.forms import inlineformset_factory
from calendar import monthrange
from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from .models import (
    DealerOrder,
    DealerOrderItem,
    DealerDispatch,
)


User = get_user_model()


def users_by_role(role):
    return User.objects.filter(profile__role=role).distinct()


def sales_officers():
    return User.objects.filter(
        Q(profile__role="SALES_OFFICER_SENIOR") |
        Q(profile__role="SALES_OFFICER_JUNIOR")
    ).distinct()


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email",
            "autocomplete": "email",
        })
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password",
            "autocomplete": "current-password",
        })
    )

class UserBasicProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

User = get_user_model()



class UserWithRoleChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        profile = getattr(obj, "profile", None)

        name = obj.get_full_name() or obj.email or obj.username

        if profile:
            role = profile.get_role_display()
            phone = profile.phone or ""
            if phone:
                return f"{name} ({role}) - {phone}"
            return f"{name} ({role})"

        return name


class EmployeeForm(forms.ModelForm):
    manager = UserWithRoleChoiceField(
        queryset=User.objects.none(),
        required=True,
        empty_label="Select reporting manager",
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "First name"
        })
    )

    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Last name"
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Employee login email"
        })
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter password"
        })
    )

    target_year = forms.IntegerField(
        required=True,
        initial=timezone.now().year,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Target year"
        })
    )

    target_amount = forms.DecimalField(
        required=True,
        max_digits=14,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Example: 2000000"
        })
    )

    achieved_amount = forms.DecimalField(
        required=False,
        max_digits=14,
        decimal_places=2,
        initial=0,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Achieved amount"
        })
    )

    manager_target_extra_percentage = forms.DecimalField(
        required=False,
        max_digits=6,
        decimal_places=2,
        initial=0,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Example: 50 for team target + 50%",
            "step": "0.01",
            "min": "0"
        })
    )

    class Meta:
        model = UserProfile

        fields = [
            "first_name",
            "last_name",
            "email",
            "password",

            "role",
            "manager",
            "phone",
            "address",
            "state",
            "district",
            "profile_image",

            # Salary and payroll details
            "salary_amount",
            "date_of_birth",
            "pan_number",

            # Bank details
            "bank_name",
            "bank_account_number",
            "bank_ifsc_code",
            "bank_account_holder_name",

            # PF details
            "pf_applicable",
            "pf_uan_number",
            "pf_deduction_percentage",

            # Insurance details
            "insurance_applicable",
            "insurance_provider_name",
            "insurance_policy_number",
            "insurance_deduction_amount",

            # Target details
            "manager_target_extra_percentage",
            "target_year",
            "target_amount",
            "achieved_amount",

            # Employee official details
            "employee_code",
            "duty_start_time",
            "duty_end_time",

            # Work week
            "work_monday",
            "work_tuesday",
            "work_wednesday",
            "work_thursday",
            "work_friday",
            "work_saturday",
            "work_sunday",

            # TA / DA
            "bike_ta_per_km",
            "car_ta_per_km",
            "daily_da_amount",

            # Leave settings
            "paid_leaves_per_year",
            "sick_leaves_per_year",
            "other_leaves_per_year",
            "unpaid_leaves_per_year",
        ]

        widgets = {
            "role": forms.Select(attrs={"class": "form-control"}),

            "manager": forms.Select(attrs={
                "class": "form-control"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Phone number"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Employee address"
            }),

            "state": forms.Select(attrs={"class": "form-control"}),

            "district": forms.Select(attrs={"class": "form-control"}),

            "profile_image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "salary_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Monthly gross salary",
                "step": "0.01",
                "min": "0"
            }),

            "date_of_birth": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "pan_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "PAN Number",
                "maxlength": "10",
                "style": "text-transform:uppercase;",
                "oninput": "this.value=this.value.toUpperCase();"
            }),

            "bank_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Bank Name"
            }),

            "bank_account_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Bank Account Number"
            }),

            "bank_ifsc_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "IFSC Code",
                "maxlength": "11",
                "style": "text-transform:uppercase;",
                "oninput": "this.value=this.value.toUpperCase();"
            }),

            "bank_account_holder_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Account Holder Name"
            }),

            "pf_applicable": forms.CheckboxInput(attrs={
                "class": "form-check-input",
                "id": "id_pf_applicable"
            }),

            "pf_uan_number": forms.TextInput(attrs={
                "class": "form-control pf-field",
                "placeholder": "12 digit PF UAN Number",
                "maxlength": "12",
                "inputmode": "numeric"
            }),

            "pf_deduction_percentage": forms.NumberInput(attrs={
                "class": "form-control pf-field",
                "step": "0.01",
                "min": "0",
                "max": "100",
                "placeholder": "Example: 12"
            }),

            "insurance_applicable": forms.CheckboxInput(attrs={
                "class": "form-check-input",
                "id": "id_insurance_applicable"
            }),

            "insurance_provider_name": forms.TextInput(attrs={
                "class": "form-control insurance-field",
                "placeholder": "Insurance Provider Name"
            }),

            "insurance_policy_number": forms.TextInput(attrs={
                "class": "form-control insurance-field",
                "placeholder": "Policy Number"
            }),

            "insurance_deduction_amount": forms.NumberInput(attrs={
                "class": "form-control insurance-field",
                "step": "0.01",
                "min": "0",
                "placeholder": "Monthly insurance deduction"
            }),

            "manager_target_extra_percentage": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Example: 50",
                "step": "0.01",
                "min": "0"
            }),

            "employee_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Employee ID"
            }),

            "duty_start_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time"
            }),

            "duty_end_time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time"
            }),

            "work_monday": forms.CheckboxInput(attrs={"class": "work-check"}),
            "work_tuesday": forms.CheckboxInput(attrs={"class": "work-check"}),
            "work_wednesday": forms.CheckboxInput(attrs={"class": "work-check"}),
            "work_thursday": forms.CheckboxInput(attrs={"class": "work-check"}),
            "work_friday": forms.CheckboxInput(attrs={"class": "work-check"}),
            "work_saturday": forms.CheckboxInput(attrs={"class": "work-check"}),
            "work_sunday": forms.CheckboxInput(attrs={"class": "work-check"}),

            "bike_ta_per_km": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Bike TA per KM"
            }),

            "car_ta_per_km": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Car TA per KM"
            }),

            "daily_da_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Daily DA amount"
            }),

            "paid_leaves_per_year": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Paid leaves per year"
            }),

            "sick_leaves_per_year": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Sick leaves per year"
            }),

            "other_leaves_per_year": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Other leaves per year"
            }),

            "unpaid_leaves_per_year": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Unpaid leaves per year"
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop("request_user", None)
        super().__init__(*args, **kwargs)

        self.fields["role"].choices = [
            choice for choice in UserProfile.ROLE_CHOICES
            if choice[0] != "DEALER"
        ]

        self.fields["manager"].required = True
        self.fields["manager"].empty_label = "Select reporting manager"

        self.fields["manager"].queryset = User.objects.filter(
            is_active=True
        ).exclude(
            profile__role="DEALER"
        ).distinct()

        # Professional labels
        self.fields["salary_amount"].label = "Monthly Gross Salary"
        self.fields["date_of_birth"].label = "Date of Birth"
        self.fields["pan_number"].label = "PAN Number"
        self.fields["bank_name"].label = "Bank Name"
        self.fields["bank_account_number"].label = "Bank Account Number"
        self.fields["bank_ifsc_code"].label = "IFSC Code"
        self.fields["bank_account_holder_name"].label = "Account Holder Name"
        self.fields["pf_applicable"].label = "PF Applicable?"
        self.fields["pf_uan_number"].label = "PF UAN Number"
        self.fields["pf_deduction_percentage"].label = "PF Deduction Percentage"
        self.fields["insurance_applicable"].label = "Insurance Applicable?"
        self.fields["insurance_provider_name"].label = "Insurance Provider Name"
        self.fields["insurance_policy_number"].label = "Insurance Policy Number"
        self.fields["insurance_deduction_amount"].label = "Monthly Insurance Deduction"

        if self.instance and self.instance.pk and self.instance.user:
            user = self.instance.user

            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email

            self.fields["manager"].queryset = self.fields["manager"].queryset.exclude(
                pk=user.pk
            )

            target = EmployeeYearlyTarget.objects.filter(
                employee=user,
                year=timezone.now().year
            ).first()

            if target:
                self.fields["target_year"].initial = target.year
                self.fields["target_amount"].initial = target.target_amount
                self.fields["achieved_amount"].initial = target.achieved_amount

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            raise forms.ValidationError("Email is required for login.")

        email = email.lower().strip()

        existing_user = User.objects.filter(email__iexact=email)

        if self.instance and self.instance.pk and self.instance.user:
            existing_user = existing_user.exclude(pk=self.instance.user.pk)

        if existing_user.exists():
            raise forms.ValidationError("This email is already registered.")

        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if not self.instance.pk and not password:
            raise forms.ValidationError("Password is required for new employee.")

        return password

    def clean_salary_amount(self):
        salary = self.cleaned_data.get("salary_amount") or Decimal("0.00")

        if salary < 0:
            raise forms.ValidationError("Salary amount cannot be negative.")

        return salary

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")

        if dob and dob >= timezone.localdate():
            raise forms.ValidationError("Date of birth must be a past date.")

        return dob

    def clean_pan_number(self):
        pan = self.cleaned_data.get("pan_number")

        if pan:
            pan = pan.upper().strip()

            if not re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", pan):
                raise forms.ValidationError("Enter valid PAN number. Example: ABCDE1234F")

        return pan

    def clean_bank_ifsc_code(self):
        ifsc = self.cleaned_data.get("bank_ifsc_code")

        if ifsc:
            ifsc = ifsc.upper().strip()

            if not re.fullmatch(r"[A-Z]{4}0[A-Z0-9]{6}", ifsc):
                raise forms.ValidationError("Enter valid IFSC code. Example: HDFC0001234")

        return ifsc

    def clean_pf_uan_number(self):
        uan = self.cleaned_data.get("pf_uan_number")

        if uan:
            uan = str(uan).strip()

            if not uan.isdigit() or len(uan) != 12:
                raise forms.ValidationError("PF UAN number must be 12 digits.")

        return uan

    def clean_target_amount(self):
        target_amount = self.cleaned_data.get("target_amount") or Decimal("0.00")
        role = self.cleaned_data.get("role")

        if target_amount < 0:
            raise forms.ValidationError("Target amount cannot be negative.")

        if role in ["SALES_OFFICER_SENIOR", "SALES_OFFICER_JUNIOR"]:
            if target_amount <= 0:
                raise forms.ValidationError("Sales Officer target is required.")

        return target_amount

    def clean_achieved_amount(self):
        achieved_amount = self.cleaned_data.get("achieved_amount") or Decimal("0.00")

        if achieved_amount < 0:
            raise forms.ValidationError("Achieved amount cannot be negative.")

        return achieved_amount

    def clean_manager_target_extra_percentage(self):
        value = self.cleaned_data.get("manager_target_extra_percentage") or Decimal("0.00")

        if value < 0:
            raise forms.ValidationError("Manager target percentage cannot be negative.")

        return value

    def clean(self):
        cleaned_data = super().clean()

        role = cleaned_data.get("role")
        manager = cleaned_data.get("manager")

        salary_amount = cleaned_data.get("salary_amount") or Decimal("0.00")

        bank_name = cleaned_data.get("bank_name")
        bank_account_number = cleaned_data.get("bank_account_number")
        bank_ifsc_code = cleaned_data.get("bank_ifsc_code")
        bank_account_holder_name = cleaned_data.get("bank_account_holder_name")

        pf_applicable = cleaned_data.get("pf_applicable")
        pf_uan_number = cleaned_data.get("pf_uan_number")
        pf_deduction_percentage = cleaned_data.get("pf_deduction_percentage") or Decimal("0.00")

        insurance_applicable = cleaned_data.get("insurance_applicable")
        insurance_provider_name = cleaned_data.get("insurance_provider_name")
        insurance_policy_number = cleaned_data.get("insurance_policy_number")
        insurance_deduction_amount = cleaned_data.get("insurance_deduction_amount") or Decimal("0.00")

        # -----------------------------
        # BANK DETAILS VALIDATION
        # -----------------------------
        any_bank_value = any([
            bank_name,
            bank_account_number,
            bank_ifsc_code,
            bank_account_holder_name,
        ])

        if any_bank_value:
            if not bank_name:
                self.add_error("bank_name", "Bank name is required when adding bank details.")

            if not bank_account_holder_name:
                self.add_error("bank_account_holder_name", "Account holder name is required.")

            if not bank_account_number:
                self.add_error("bank_account_number", "Bank account number is required.")

            if not bank_ifsc_code:
                self.add_error("bank_ifsc_code", "IFSC code is required.")

        if bank_account_number:
            bank_account_number = str(bank_account_number).strip()

            if len(bank_account_number) < 6:
                self.add_error("bank_account_number", "Enter valid bank account number.")

        # -----------------------------
        # PF DETAILS VALIDATION
        # -----------------------------
        if pf_applicable:
            if salary_amount <= 0:
                self.add_error("salary_amount", "Salary is required when PF is applicable.")

            if not pf_uan_number:
                self.add_error("pf_uan_number", "PF UAN number is required when PF is applicable.")

            if pf_deduction_percentage <= 0:
                self.add_error("pf_deduction_percentage", "PF deduction percentage must be greater than 0.")

            if pf_deduction_percentage > 100:
                self.add_error("pf_deduction_percentage", "PF deduction percentage cannot be more than 100.")
        else:
            cleaned_data["pf_uan_number"] = ""
            cleaned_data["pf_deduction_percentage"] = Decimal("0.00")

        # -----------------------------
        # INSURANCE DETAILS VALIDATION
        # -----------------------------
        if insurance_applicable:
            if not insurance_provider_name:
                self.add_error("insurance_provider_name", "Insurance provider name is required.")

            if not insurance_policy_number:
                self.add_error("insurance_policy_number", "Insurance policy number is required.")

            if insurance_deduction_amount <= 0:
                self.add_error("insurance_deduction_amount", "Monthly insurance deduction must be greater than 0.")
        else:
            cleaned_data["insurance_provider_name"] = ""
            cleaned_data["insurance_policy_number"] = ""
            cleaned_data["insurance_deduction_amount"] = Decimal("0.00")

        # -----------------------------
        # MANAGER / ROLE VALIDATION
        # -----------------------------
        if not manager:
            self.add_error("manager", "Reporting manager is required.")
            return cleaned_data

        manager_profile = getattr(manager, "profile", None)

        if not manager_profile:
            self.add_error("manager", "Selected manager does not have a profile.")
            return cleaned_data

        if role in ["SALES_OFFICER_SENIOR", "SALES_OFFICER_JUNIOR"]:
            if manager_profile.role != "ASM":
                self.add_error(
                    "manager",
                    "For Sales Officer, manager must be ASM because dealer approval goes to ASM automatically."
                )

        elif role == "ASM":
            if manager_profile.role not in ["REGIONAL_MANAGER", "STATE_HEAD", "ADMIN"]:
                self.add_error(
                    "manager",
                    "For ASM, manager should be Regional Manager, State Head, or Admin."
                )

        elif role == "REGIONAL_MANAGER":
            if manager_profile.role not in ["STATE_HEAD", "ADMIN"]:
                self.add_error(
                    "manager",
                    "For Regional Manager, manager should be State Head or Admin."
                )

        elif role == "STATE_HEAD":
            if manager_profile.role != "ADMIN":
                self.add_error(
                    "manager",
                    "For State Head, manager should be Admin."
                )

        elif role in [
            "ACCOUNTANT",
            "HR",
            "WAREHOUSE_MANAGER",
            "PRODUCTION_INCHARGE",
            "DEVELOPMENT_OFFICER",
            "INVENTORY_MANAGER",
            "ASSET_MANAGER",
        ]:
            if manager_profile.role not in [
                "ADMIN",
                "STATE_HEAD",
                "REGIONAL_MANAGER",
                "ASM",
                "ACCOUNTANT",
            ]:
                self.add_error(
                    "manager",
                    "Please select a valid reporting manager."
                )

        return cleaned_data


        
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_image", "phone", "address", "state", "district"]

        widgets = {
            "profile_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "state": forms.Select(attrs={"class": "form-control"}),
            "district": forms.Select(attrs={"class": "form-control"}),
        }

class ProfileImageUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_image"]

        widgets = {
            "profile_image": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            })
        }

        
class DealerCreateForm(forms.ModelForm):
    dealer_code = forms.CharField(
        required=False,
        label="Dealer ID",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Example: DLR00001 / leave empty for auto ID"
        })
    )

    created_by_sales_officer = UserWithRoleChoiceField(
        queryset=User.objects.none(),
        required=True,
        empty_label="Select dealer manager / sales officer",
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Create dealer password",
        })
    )

    class Meta:
        model = Dealer

        fields = [
            "dealer_code",
            "created_by_sales_officer",
            "dealer_image",
            "owner_name",
            "email",
            "phone",
            "owner_address",
            "firm_name",
            "latitude",
            "longitude",
            "location_accuracy_meters",
            "visit_radius_meters",
            "gst_number",
            "firm_address",
            "state",
            "district",
            "firm_type",
            "license_number",
            "deposit_amount",
            "deposit_mode",
            "cheque_number",
            "flag",
            "yearly_target_amount",
            "password",
        ]

        widgets = {
            "dealer_image": forms.ClearableFileInput(attrs={"class": "form-control"}),

            "owner_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Owner name"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Dealer login email"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Phone number"
            }),

            "owner_address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Owner address"
            }),

            "firm_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Firm name"
            }),

            "gst_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "GST number"
            }),

            "firm_address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Firm address"
            }),
            "latitude": forms.NumberInput(attrs={
                "class": "form-control",
                "readonly": "readonly",
                "id": "id_dealer_latitude",
                "step": "0.0000001",
            }),

            "longitude": forms.NumberInput(attrs={
                "class": "form-control",
                "readonly": "readonly",
                "id": "id_dealer_longitude",
                "step": "0.0000001",
            }),

            "location_accuracy_meters": forms.NumberInput(attrs={
                "class": "form-control",
                "readonly": "readonly",
                "id": "id_dealer_location_accuracy",
                "step": "0.01",
            }),

            "visit_radius_meters": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "10",
                "max": "25",
                "value": "15",
            }),

            "state": forms.Select(attrs={"class": "form-control"}),
            "district": forms.Select(attrs={"class": "form-control"}),

            "firm_type": forms.Select(attrs={"class": "form-control"}),

            "license_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "License number optional"
            }),

            "deposit_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "15000",
                "step": "0.01",
                "placeholder": "Minimum ₹15,000",
            }),

            "deposit_mode": forms.Select(attrs={
                "class": "form-control",
                "readonly": "readonly",
            }),

            "cheque_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Cheque number"
            }),

            "flag": forms.Select(attrs={"class": "form-control"}),

            "yearly_target_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Example: 1000000"
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop("request_user", None)
        super().__init__(*args, **kwargs)

        self.fields["created_by_sales_officer"].queryset = sales_officers().filter(
            is_active=True
        ).order_by("first_name", "email")

        self.fields["deposit_amount"].initial = Decimal("15000.00")
        self.fields["deposit_mode"].initial = "CHEQUE"
        self.fields["deposit_mode"].disabled = True

        user_profile = getattr(self.request_user, "profile", None)

        if user_profile and user_profile.role in ["SALES_OFFICER_SENIOR", "SALES_OFFICER_JUNIOR"]:
            self.fields["created_by_sales_officer"].queryset = User.objects.filter(
                pk=self.request_user.pk
            )
            self.fields["created_by_sales_officer"].initial = self.request_user
            self.fields["created_by_sales_officer"].disabled = True

    def clean_dealer_code(self):
        dealer_code = self.cleaned_data.get("dealer_code")

        if dealer_code:
            dealer_code = dealer_code.strip().upper()

            if Dealer.objects.filter(dealer_code__iexact=dealer_code).exists():
                raise forms.ValidationError("This dealer ID already exists.")

        return dealer_code

    def clean_deposit_amount(self):
        amount = self.cleaned_data.get("deposit_amount") or Decimal("0.00")

        if amount < Decimal("15000.00"):
            raise forms.ValidationError("Minimum cheque deposit amount is ₹15,000.")

        return amount

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            raise forms.ValidationError("Email is required for dealer login.")

        email = email.lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")

        return email

    def clean_cheque_number(self):
        cheque_number = self.cleaned_data.get("cheque_number")

        if not cheque_number:
            raise forms.ValidationError("Cheque number is required.")

        return cheque_number

    def clean(self):
        cleaned_data = super().clean()

        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")
        accuracy = cleaned_data.get("location_accuracy_meters")
        radius = cleaned_data.get("visit_radius_meters") or 15

        if latitude is None:
            self.add_error("latitude", "Dealer GPS latitude is required. Please capture GPS.")

        if longitude is None:
            self.add_error("longitude", "Dealer GPS longitude is required. Please capture GPS.")

        if accuracy is None:
            self.add_error("location_accuracy_meters", "Dealer GPS accuracy is required. Please capture GPS.")

        if accuracy is not None and accuracy > 25:
            self.add_error(
                "location_accuracy_meters",
                "GPS accuracy is weak. Please stand outside dealer shop and capture again."
            )

        if radius < 10 or radius > 25:
            self.add_error("visit_radius_meters", "Visit radius must be between 10 and 25 meters.")

        return cleaned_data


class DealerEditForm(forms.ModelForm):
    dealer_code = forms.CharField(
        required=False,
        label="Dealer ID",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Dealer ID"
        })
    )

    created_by_sales_officer = UserWithRoleChoiceField(
        queryset=User.objects.none(),
        required=True,
        empty_label="Select dealer manager / sales officer",
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = Dealer

        fields = [
            "dealer_code",
            "created_by_sales_officer",
            "dealer_image",
            "owner_name",
            "email",
            "phone",
            "owner_address",
            "firm_name",
            "gst_number",
            "firm_address",

            # GPS fields
            "latitude",
            "longitude",
            "location_accuracy_meters",
            "visit_radius_meters",

            "state",
            "district",
            "firm_type",
            "license_number",
            "deposit_amount",
            "deposit_mode",
            "cheque_number",
            "flag",
            "yearly_target_amount",
            "achieved_amount",
        ]

        widgets = {
            "dealer_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "owner_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "owner_address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "firm_name": forms.TextInput(attrs={"class": "form-control"}),
            "gst_number": forms.TextInput(attrs={"class": "form-control"}),
            "firm_address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),

            "latitude": forms.NumberInput(attrs={
                "class": "form-control",
                "readonly": "readonly",
                "id": "id_dealer_latitude",
                "step": "0.0000001",
            }),

            "longitude": forms.NumberInput(attrs={
                "class": "form-control",
                "readonly": "readonly",
                "id": "id_dealer_longitude",
                "step": "0.0000001",
            }),

            "location_accuracy_meters": forms.NumberInput(attrs={
                "class": "form-control",
                "readonly": "readonly",
                "id": "id_dealer_location_accuracy",
                "step": "0.01",
            }),

            "visit_radius_meters": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "10",
                "max": "25",
            }),

            "state": forms.Select(attrs={"class": "form-control"}),
            "district": forms.Select(attrs={"class": "form-control"}),
            "firm_type": forms.Select(attrs={"class": "form-control"}),
            "license_number": forms.TextInput(attrs={"class": "form-control"}),
            "deposit_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "deposit_mode": forms.Select(attrs={"class": "form-control"}),
            "cheque_number": forms.TextInput(attrs={"class": "form-control"}),
            "flag": forms.Select(attrs={"class": "form-control"}),
            "yearly_target_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "achieved_amount": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop("request_user", None)
        super().__init__(*args, **kwargs)

        self.fields["created_by_sales_officer"].queryset = sales_officers().filter(
            is_active=True
        ).order_by("first_name", "email")

        if not self.fields["visit_radius_meters"].initial:
            self.fields["visit_radius_meters"].initial = 15

        role = None

        if self.request_user and hasattr(self.request_user, "profile"):
            role = self.request_user.profile.role

        can_edit_cheque = (
            self.request_user
            and (
                self.request_user.is_superuser
                or role in ["ADMIN", "ACCOUNTANT"]
            )
        )

        if not can_edit_cheque:
            self.fields["deposit_amount"].disabled = True
            self.fields["deposit_mode"].disabled = True
            self.fields["cheque_number"].disabled = True

    def clean_dealer_code(self):
        dealer_code = self.cleaned_data.get("dealer_code")

        if dealer_code:
            dealer_code = dealer_code.strip().upper()

            qs = Dealer.objects.filter(dealer_code__iexact=dealer_code)

            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("This dealer ID already exists.")

        return dealer_code

    def clean(self):
        cleaned_data = super().clean()

        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")
        accuracy = cleaned_data.get("location_accuracy_meters")
        radius = cleaned_data.get("visit_radius_meters") or 15

        if latitude is None:
            self.add_error("latitude", "Dealer GPS latitude is required. Please capture GPS.")

        if longitude is None:
            self.add_error("longitude", "Dealer GPS longitude is required. Please capture GPS.")

        if accuracy is None:
            self.add_error("location_accuracy_meters", "Dealer GPS accuracy is required. Please capture GPS.")

        if accuracy is not None and accuracy > 25:
            self.add_error(
                "location_accuracy_meters",
                "GPS accuracy is weak. Please stand outside dealer shop and capture again."
            )

        if radius < 10 or radius > 25:
            self.add_error("visit_radius_meters", "Visit radius must be between 10 and 25 meters.")

        return cleaned_data

        
        
class DealerRejectForm(forms.Form):
    rejection_reason = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Enter rejection reason"
        }),
        required=True
    )


class ForwardToRegionalManagerForm(forms.Form):
    regional_manager = forms.ModelChoiceField(
        queryset=User.objects.none(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["regional_manager"].queryset = users_by_role("REGIONAL_MANAGER").filter(is_active=True)


class ForwardToStateHeadForm(forms.Form):
    state_head = forms.ModelChoiceField(
        queryset=User.objects.none(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["state_head"].queryset = users_by_role("STATE_HEAD").filter(is_active=True)


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse

        fields = [
            "state",
            "district",
            "name",
            "warehouse_manager",
            "is_active",
        ]

        widgets = {
            "state": forms.Select(attrs={"class": "form-control"}),
            "district": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Warehouse name"
            }),
            "warehouse_manager": forms.Select(attrs={
                "class": "form-control"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["warehouse_manager"].required = True
        self.fields["warehouse_manager"].empty_label = "Select Warehouse Manager"

        self.fields["warehouse_manager"].queryset = users_by_role(
            "WAREHOUSE_MANAGER"
        ).filter(
            is_active=True
        ).select_related(
            "profile"
        ).order_by(
            "first_name",
            "last_name",
            "email",
            "username"
        )

        self.fields["warehouse_manager"].label_from_instance = self.warehouse_manager_label

    def warehouse_manager_label(self, user):
        full_name = user.get_full_name().strip()
        name = full_name or user.email or user.username

        profile = getattr(user, "profile", None)

        employee_code = ""
        phone = ""

        if profile:
            employee_code = profile.employee_code or ""
            phone = profile.phone or ""

        label_parts = [name]

        if employee_code:
            label_parts.append(f"ID: {employee_code}")

        if user.email:
            label_parts.append(user.email)

        if phone:
            label_parts.append(f"Phone: {phone}")

        return " - ".join(label_parts)

    def clean_warehouse_manager(self):
        warehouse_manager = self.cleaned_data.get("warehouse_manager")

        if not warehouse_manager:
            raise forms.ValidationError("Please select warehouse manager.")

        profile = getattr(warehouse_manager, "profile", None)

        if not profile or profile.role != "WAREHOUSE_MANAGER":
            raise forms.ValidationError("Selected user is not a Warehouse Manager.")

        return warehouse_manager

        
class FarmerMeetCreateForm(forms.ModelForm):
    class Meta:
        model = FarmerMeetRequest

        fields = [
            "title",
            "location",
            "meeting_date",
            "expected_farmer_count",
            "description",
            "sales_officer",
            "asm",
            "regional_manager",
            "state_head",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "meeting_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "expected_farmer_count": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "sales_officer": forms.Select(attrs={"class": "form-control"}),
            "asm": forms.Select(attrs={"class": "form-control"}),
            "regional_manager": forms.Select(attrs={"class": "form-control"}),
            "state_head": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["sales_officer"].queryset = sales_officers().filter(is_active=True)
        self.fields["asm"].queryset = users_by_role("ASM").filter(is_active=True)
        self.fields["regional_manager"].queryset = users_by_role("REGIONAL_MANAGER").filter(is_active=True)
        self.fields["state_head"].queryset = users_by_role("STATE_HEAD").filter(is_active=True)

        self.fields["regional_manager"].required = False
        self.fields["state_head"].required = False

    def clean(self):
        cleaned_data = super().clean()

        count = cleaned_data.get("expected_farmer_count") or 0
        regional_manager = cleaned_data.get("regional_manager")
        state_head = cleaned_data.get("state_head")

        if count > 50 and not regional_manager:
            self.add_error("regional_manager", "Regional Manager is required when farmers are more than 50.")

        if count > 100 and not state_head:
            self.add_error("state_head", "State Head is required when farmers are more than 100.")

        return cleaned_data


class FarmerMeetRejectForm(forms.Form):
    rejection_reason = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Enter rejection reason"
        }),
        required=True
    )


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = [
            "name",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: Fertilizers"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Category description"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }


class CategoryPaymentRuleForm(forms.ModelForm):
    class Meta:
        model = CategoryPaymentRule
        fields = [
            "rule_type",
            "title",
            "discount_percent",
            "from_day",
            "to_day",
            "is_active",
        ]

        widgets = {
            "rule_type": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: 1 to 20 days discount"
            }),
            "discount_percent": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Discount %"
            }),
            "from_day": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "From day"
            }),
            "to_day": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "To day"
            }),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


CategoryPaymentRuleFormSet = inlineformset_factory(
    ProductCategory,
    CategoryPaymentRule,
    form=CategoryPaymentRuleForm,
    extra=1,
    can_delete=True
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "image",
            "hsn_number",
            "description",
            "is_active",
        ]

        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: Crystal Topper 77"
            }),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "hsn_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "HSN Number"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Product description"
            }),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProductPackSizeForm(forms.ModelForm):
    class Meta:
        model = ProductPackSize
        fields = [
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
        ]

        widgets = {
            "warehouse": forms.Select(attrs={"class": "form-control"}),
            "pack_size": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "1 / 5 / 25"
            }),
            "unit": forms.Select(attrs={"class": "form-control"}),
            "packing_type": forms.Select(attrs={"class": "form-control"}),
            "units_per_box": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Example: 25"
            }),
            "mrp_per_unit": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),
            "sale_price_per_unit": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),
            "purchase_price_per_unit": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),
            "box_sale_price": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Leave 0 to auto calculate"
            }),
            "stock_boxes": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


ProductPackSizeFormSet = inlineformset_factory(
    Product,
    ProductPackSize,
    form=ProductPackSizeForm,
    extra=1,
    can_delete=True
)


class ProductSchemeForm(forms.ModelForm):
    class Meta:
        model = ProductScheme
        fields = [
            "scheme_name",
            "scheme_type",
            "min_boxes",
            "discount_percent",
            "free_boxes",
            "valid_from",
            "valid_to",
            "is_active",
        ]

        widgets = {
            "scheme_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: Buy 10 boxes get 1 free"
            }),
            "scheme_type": forms.Select(attrs={"class": "form-control"}),
            "min_boxes": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Minimum boxes"
            }),
            "discount_percent": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Discount %"
            }),
            "free_boxes": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Free boxes"
            }),
            "valid_from": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "valid_to": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Scheme is optional, so fields should not force product save failure
        for field_name in self.fields:
            self.fields[field_name].required = False

    def has_changed(self):
        """
        Empty scheme row should be ignored.
        This prevents validation errors when admin does not want scheme.
        """
        if self.instance and self.instance.pk:
            return super().has_changed()

        if not self.data:
            return super().has_changed()

        scheme_name = self.data.get(f"{self.prefix}-scheme_name", "").strip()
        discount_percent = self.data.get(f"{self.prefix}-discount_percent", "").strip()
        free_boxes = self.data.get(f"{self.prefix}-free_boxes", "").strip()

        # If scheme name is empty and no real scheme value entered, ignore this form
        if not scheme_name and discount_percent in ["", "0", "0.00"] and free_boxes in ["", "0"]:
            return False

        return super().has_changed()

    def clean(self):
        cleaned_data = super().clean()

        scheme_name = cleaned_data.get("scheme_name")
        discount_percent = cleaned_data.get("discount_percent") or 0
        free_boxes = cleaned_data.get("free_boxes") or 0

        # Empty optional scheme row
        if not scheme_name and not discount_percent and not free_boxes:
            return cleaned_data

        # If admin starts entering scheme, scheme name is required
        if not scheme_name:
            raise forms.ValidationError("Scheme name is required if you are adding a scheme.")

        return cleaned_data


ProductSchemeFormSet = inlineformset_factory(
    Product,
    ProductScheme,
    form=ProductSchemeForm,
    extra=1,
    can_delete=True,
    validate_min=False,
)


class OrderRejectForm(forms.Form):
    reason = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "Enter rejection reason"
        })
    )




class WarehouseOrderItemForm(forms.ModelForm):
    mfg_date = forms.DateField(
        required=False,
        input_formats=["%Y-%m", "%Y-%m-%d", "%m/%Y"],
        widget=forms.DateInput(
            format="%Y-%m",
            attrs={
                "class": "form-control",
                "type": "month",
                "placeholder": "Select MFG Month & Year",
            }
        )
    )

    expiry_date = forms.DateField(
        required=False,
        input_formats=["%Y-%m", "%Y-%m-%d", "%m/%Y"],
        widget=forms.DateInput(
            format="%Y-%m",
            attrs={
                "class": "form-control",
                "type": "month",
                "placeholder": "Select EXP Month & Year",
            }
        )
    )

    class Meta:
        model = DealerOrderItem
        fields = [
            "hsn_code",
            "batch_no",
            "mfg_date",
            "expiry_date",
        ]

        widgets = {
            "hsn_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "HSN/SAC"
            }),
            "batch_no": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Batch No."
            }),
        }

    def clean_mfg_date(self):
        value = self.cleaned_data.get("mfg_date")

        if value:
            return value.replace(day=1)

        return value

    def clean_expiry_date(self):
        value = self.cleaned_data.get("expiry_date")

        if value:
            last_day = monthrange(value.year, value.month)[1]
            return value.replace(day=last_day)

        return value


WarehouseOrderItemFormSet = inlineformset_factory(
    DealerOrder,
    DealerOrderItem,
    form=WarehouseOrderItemForm,
    extra=0,
    can_delete=False
)

class AccountantOrderItemForm(forms.ModelForm):
    class Meta:
        model = DealerOrderItem
        fields = [
            "hsn_code",
            "batch_no",
            "mfg_date",
            "expiry_date",
            "quantity_boxes",
            "gst_percent",
        ]

        widgets = {
            "hsn_code": forms.TextInput(attrs={"class": "form-control"}),
            "batch_no": forms.TextInput(attrs={"class": "form-control"}),
            "mfg_date": forms.TextInput(attrs={"class": "form-control"}),
            "expiry_date": forms.TextInput(attrs={"class": "form-control"}),
            "quantity_boxes": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1
            }),
            "gst_percent": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),
        }


AccountantOrderItemFormSet = inlineformset_factory(
    DealerOrder,
    DealerOrderItem,
    form=AccountantOrderItemForm,
    extra=0,
    can_delete=False
)


def get_financial_year_choices():
    today = timezone.localdate()
    year = today.year

    if today.month >= 4:
        current_start = year
    else:
        current_start = year - 1

    current_fy = f"{str(current_start)[-2:]}-{str(current_start + 1)[-2:]}"
    previous_fy = f"{str(current_start - 1)[-2:]}-{str(current_start)[-2:]}"

    return [
        (current_fy, current_fy),
        (previous_fy, previous_fy),
    ]


class AccountantInvoiceReleaseForm(forms.Form):
    financial_year = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"})
    )

    invoice_date = forms.DateField(
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={
            "class": "form-control",
            "type": "date"
        })
    )

    place_of_supply = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Example: 29-Karnataka"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["financial_year"].choices = get_financial_year_choices()


class DealerDispatchForm(forms.ModelForm):
    class Meta:
        model = DealerDispatch
        fields = [
            "transport_type",
            "vehicle_name",
            "vehicle_number",
            "driver_name",
            "driver_phone",
            "other_transport_tracking_id",
            "dispatch_date",
            "note",
        ]

        widgets = {
            "transport_type": forms.Select(attrs={
                "class": "form-control",
                "id": "id_transport_type"
            }),
            "vehicle_name": forms.TextInput(attrs={
                "class": "form-control own-field",
                "placeholder": "Vehicle Name"
            }),
            "vehicle_number": forms.TextInput(attrs={
                "class": "form-control own-field",
                "placeholder": "Vehicle Number"
            }),
            "driver_name": forms.TextInput(attrs={
                "class": "form-control own-field",
                "placeholder": "Driver Name"
            }),
            "driver_phone": forms.TextInput(attrs={
                "class": "form-control own-field",
                "placeholder": "Driver Phone"
            }),
            "other_transport_tracking_id": forms.TextInput(attrs={
                "class": "form-control other-field",
                "placeholder": "Transport Tracking ID"
            }),
            "dispatch_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "note": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Dispatch note"
            }),
        }


from decimal import Decimal
from django import forms
from django.utils import timezone

from .models import DealerInvoicePayment


class DealerInvoicePaymentForm(forms.ModelForm):
    category_rule_choice = forms.ChoiceField(
        required=False,
        choices=[("", "No category payment rule")],
        widget=forms.Select(attrs={
            "class": "form-control",
            "id": "id_category_rule_choice"
        })
    )

    manual_discount_percent = forms.DecimalField(
        required=False,
        max_digits=6,
        decimal_places=2,
        min_value=Decimal("0.00"),
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.01",
            "placeholder": "Manual discount %"
        })
    )

    class Meta:
        model = DealerInvoicePayment
        fields = [
            "payment_status",
            "payment_mode",
            "payment_date",
            "payment_amount",
            "category_rule_choice",
            "manual_discount_percent",
            "upi_reference_number",
            "bank_transaction_number",
            "cheque_number",
            "payment_screenshot",
        ]

        widgets = {
            "payment_status": forms.Select(attrs={
                "class": "form-control",
                "id": "id_payment_status"
            }),
            "payment_mode": forms.Select(attrs={
                "class": "form-control",
                "id": "id_payment_mode"
            }),
            "payment_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
                "id": "id_payment_date",
            }),
            "payment_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Enter amount to settle",
                "id": "id_payment_amount",
            }),
            "upi_reference_number": forms.TextInput(attrs={
                "class": "form-control upi-field",
                "placeholder": "UPI reference number"
            }),
            "bank_transaction_number": forms.TextInput(attrs={
                "class": "form-control bank-field",
                "placeholder": "Bank transaction number"
            }),
            "cheque_number": forms.TextInput(attrs={
                "class": "form-control cheque-field",
                "placeholder": "Cheque number"
            }),
            "payment_screenshot": forms.ClearableFileInput(attrs={
                "class": "form-control upi-field bank-field"
            }),
        }

    def __init__(self, *args, **kwargs):
        self.invoice = kwargs.pop("invoice", None)
        self.category_rule_choices = kwargs.pop("category_rule_choices", None)

        super().__init__(*args, **kwargs)

        if self.invoice:
            self.fields["payment_amount"].initial = self.invoice.balance_amount

        self.fields["payment_date"].initial = timezone.localdate()

        if self.category_rule_choices:
            self.fields["category_rule_choice"].choices = self.category_rule_choices

    def clean(self):
        cleaned_data = super().clean()

        payment_status = cleaned_data.get("payment_status")
        payment_mode = cleaned_data.get("payment_mode")
        payment_amount = cleaned_data.get("payment_amount") or Decimal("0.00")
        manual_discount_percent = cleaned_data.get("manual_discount_percent") or Decimal("0.00")

        if payment_amount <= 0:
            raise forms.ValidationError("Payment amount must be greater than zero.")

        if self.invoice and payment_amount > self.invoice.balance_amount:
            raise forms.ValidationError("Payment amount cannot be greater than pending balance.")

        if payment_status == "PARTIAL":
            if manual_discount_percent < 0:
                raise forms.ValidationError("Manual discount cannot be negative.")

        if payment_mode == "UPI":
            if not cleaned_data.get("upi_reference_number"):
                raise forms.ValidationError("UPI reference number is required.")

        if payment_mode == "BANK":
            if not cleaned_data.get("bank_transaction_number"):
                raise forms.ValidationError("Bank transaction number is required.")

        if payment_mode == "CHEQUE":
            if not cleaned_data.get("cheque_number"):
                raise forms.ValidationError("Cheque number is required.")

        return cleaned_data




from django import forms
from django.utils import timezone

from .models import (
    CompanyAccount,
    CompanyPaymentIn,
    CompanyPaymentOut,
    Dealer,
)


class CompanyAccountForm(forms.ModelForm):
    class Meta:
        model = CompanyAccount

        fields = [
            "account_name",
            "bank_name",
            "branch_name",
            "account_number",
            "ifsc_code",
            "account_holder_name",
            "bank_address",
            "opening_balance",
            "current_balance",
            "is_active",
        ]

        widgets = {
            "account_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: Axis Bank Main Account"
            }),
            "bank_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Bank name"
            }),
            "branch_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Branch name"
            }),
            "account_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Account number"
            }),
            "ifsc_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "IFSC code"
            }),
            "account_holder_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Account holder name"
            }),
            "bank_address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Bank address"
            }),
            "opening_balance": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),
            "current_balance": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

class DealerSearchChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        dealer_code = getattr(obj, "dealer_code", "") or f"DLR{obj.id:05d}"
        firm_name = getattr(obj, "firm_name", "") or "-"
        owner_name = getattr(obj, "owner_name", "") or "-"
        phone = (
            getattr(obj, "owner_phone", None)
            or getattr(obj, "phone", None)
            or "-"
        )

        return f"{dealer_code} | {firm_name} | {owner_name} | {phone}"


class CompanyPaymentInForm(forms.ModelForm):
    dealer = DealerSearchChoiceField(
        queryset=Dealer.objects.none(),
        required=False,
        empty_label="Select dealer",
        widget=forms.Select(attrs={
            "class": "form-control dealer-hidden-select",
            "id": "id_dealer",
        })
    )

    class Meta:
        model = CompanyPaymentIn

        fields = [
            "account",
            "source_type",
            "dealer",
            "amount",
            "payment_mode",
            "payment_date",
            "reference_number",
            "cheque_number",
            "payment_screenshot",
            "reason",
        ]

        widgets = {
            "account": forms.Select(attrs={
                "class": "form-control"
            }),

            "source_type": forms.Select(attrs={
                "class": "form-control",
                "id": "id_source_type"
            }),

            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Enter amount"
            }),

            "payment_mode": forms.Select(attrs={
                "class": "form-control",
                "id": "id_payment_mode"
            }),

            "payment_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "reference_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Reference / transaction number"
            }),

            "cheque_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Cheque number"
            }),

            "payment_screenshot": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "reason": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Reason is compulsory"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["account"].queryset = CompanyAccount.objects.filter(
            is_active=True
        ).order_by("account_name")

        self.fields["dealer"].queryset = Dealer.objects.all().order_by(
            "dealer_code",
            "firm_name"
        )

        self.fields["dealer"].required = False
        self.fields["payment_date"].initial = timezone.localdate()

class CompanyPaymentOutForm(forms.ModelForm):
    class Meta:
        model = CompanyPaymentOut

        fields = [
            "account",
            "expense_type",
            "payee_name",
            "amount",
            "payment_mode",
            "payment_date",
            "reference_number",
            "cheque_number",
            "payment_screenshot",
            "reason",
        ]

        widgets = {
            "account": forms.Select(attrs={
                "class": "form-control"
            }),
            "expense_type": forms.Select(attrs={
                "class": "form-control"
            }),
            "payee_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Vendor / person / company name"
            }),
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Enter amount"
            }),
            "payment_mode": forms.Select(attrs={
                "class": "form-control",
                "id": "id_payment_mode"
            }),
            "payment_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "reference_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Reference / transaction number"
            }),
            "cheque_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Cheque number"
            }),
            "payment_screenshot": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "reason": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Reason is compulsory"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["account"].queryset = CompanyAccount.objects.filter(
            is_active=True
        ).order_by("account_name")

        self.fields["payment_date"].initial = timezone.localdate()




from django import forms
from django.utils import timezone




class SalesReturnDealerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        dealer_code = getattr(obj, "dealer_code", "") or f"DLR{obj.id:05d}"
        firm_name = obj.firm_name or "-"
        owner_name = obj.owner_name or "-"
        phone = obj.phone or "-"

        return f"{dealer_code} | {firm_name} | {owner_name} | {phone}"


class SalesReturnCreditNoteForm(forms.ModelForm):
    dealer = SalesReturnDealerChoiceField(
        queryset=Dealer.objects.none(),
        required=True,
        empty_label="Select dealer",
        widget=forms.Select(attrs={
            "class": "form-control dealer-hidden-select",
            "id": "id_dealer",
        })
    )

    invoice = forms.ModelChoiceField(
        queryset=DealerInvoice.objects.none(),
        required=True,
        widget=forms.HiddenInput(attrs={
            "id": "id_invoice"
        })
    )

    class Meta:
        model = SalesReturnCreditNote

        fields = [
            "dealer",
            "invoice",
            "return_date",
            "reason",
        ]

        widgets = {
            "return_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "reason": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Reason is compulsory. Example: damaged stock / expired stock / dealer returned goods"
            }),
        }

    def __init__(self, *args, **kwargs):
        selected_dealer = kwargs.pop("selected_dealer", None)
        super().__init__(*args, **kwargs)

        self.fields["dealer"].queryset = Dealer.objects.all().order_by("firm_name")

        if selected_dealer:
            self.fields["invoice"].queryset = DealerInvoice.objects.filter(
                order__dealer=selected_dealer
            ).order_by("-invoice_date", "-id")
        else:
            self.fields["invoice"].queryset = DealerInvoice.objects.all().order_by("-invoice_date", "-id")

        self.fields["return_date"].initial = timezone.localdate()

class EmployeeClockOutForm(forms.ModelForm):
    class Meta:
        model = EmployeeAttendance
        fields = [
            "vehicle_type",
            "clock_out_odometer_reading",
            "public_vehicle_amount",
            "public_vehicle_bill",
        ]

        widgets = {
            "vehicle_type": forms.Select(attrs={
                "class": "form-control",
                "id": "id_vehicle_type"
            }),
            "clock_out_odometer_reading": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
                "placeholder": "Enter ending odometer reading"
            }),
            "public_vehicle_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
                "placeholder": "Public vehicle amount"
            }),
            "public_vehicle_bill": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*,.pdf",
            }),
        }

    def clean(self):
        cleaned = super().clean()

        vehicle_type = cleaned.get("vehicle_type")
        clock_out_odometer = cleaned.get("clock_out_odometer_reading")
        public_amount = cleaned.get("public_vehicle_amount")
        public_bill = cleaned.get("public_vehicle_bill")

        if not vehicle_type:
            self.add_error("vehicle_type", "Please select vehicle type.")

        if vehicle_type in ["BIKE", "CAR", "COMPANY"]:
            if clock_out_odometer is None:
                self.add_error(
                    "clock_out_odometer_reading",
                    "Please enter ending odometer reading."
                )

        if vehicle_type == "PUBLIC":
            if not public_amount or public_amount <= 0:
                self.add_error(
                    "public_vehicle_amount",
                    "Please enter public vehicle amount."
                )

            if not public_bill:
                self.add_error(
                    "public_vehicle_bill",
                    "Please upload public vehicle bill."
                )

        return cleaned
        


class ManagerAttendanceApprovalForm(forms.ModelForm):
    class Meta:
        model = EmployeeAttendance
        fields = ["manager_approved_km", "manager_remarks"]

        widgets = {
            "manager_approved_km": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Approved KM"
            }),
            "manager_remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Manager remarks"
            }),
        }


class HRClaimApprovalForm(forms.ModelForm):
    class Meta:
        model = EmployeeAttendance
        fields = ["hr_remarks"]

        widgets = {
            "hr_remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "HR remarks"
            }),
        }


class EmployeeLeaveRequestForm(forms.ModelForm):
    class Meta:
        model = EmployeeLeaveRequest
        fields = [
            "leave_type",
            "day_type",
            "from_date",
            "to_date",
            "reason",
        ]

        widgets = {
            "leave_type": forms.Select(attrs={"class": "form-control"}),
            "day_type": forms.Select(attrs={"class": "form-control"}),
            "from_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "to_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "reason": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Reason for leave"
            }),
        }



class PayslipGenerateForm(forms.Form):
    GENERATE_TYPE_CHOICES = (
        ("INDIVIDUAL", "Individual Employee"),
        ("ALL", "All Employees"),
    )

    generate_type = forms.ChoiceField(
        choices=GENERATE_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control", "id": "id_generate_type"})
    )

    employee = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    month = forms.ChoiceField(
        choices=[(i, calendar.month_name[i]) for i in range(1, 13)],
        widget=forms.Select(attrs={"class": "form-control"})
    )

    year = forms.IntegerField(
        initial=timezone.localdate().year,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "min": "2024",
            "max": "2100"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["employee"].queryset = User.objects.filter(
            is_active=True,
            profile__isnull=False
        ).exclude(
            profile__role="DEALER"
        ).order_by("first_name", "username")

        self.fields["employee"].empty_label = "Select employee"

    def clean(self):
        cleaned = super().clean()

        generate_type = cleaned.get("generate_type")
        employee = cleaned.get("employee")

        if generate_type == "INDIVIDUAL" and not employee:
            self.add_error("employee", "Please select employee.")

        return cleaned


class PayslipEditForm(forms.ModelForm):
    class Meta:
        model = EmployeePayslip

        fields = [
            "basic_salary",
            "allowance_amount",
            "leave_deduction_amount",
            "pf_deduction_amount",
            "insurance_deduction_amount",
            "other_deduction_amount",
            "remarks",
        ]

        widgets = {
            "basic_salary": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),

            "allowance_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),

            "leave_deduction_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),

            "pf_deduction_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
                "placeholder": "PF deduction amount"
            }),

            "insurance_deduction_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
                "placeholder": "Insurance deduction amount"
            }),

            "other_deduction_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),

            "remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Payslip remarks"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        for field in [
            "basic_salary",
            "allowance_amount",
            "leave_deduction_amount",
            "pf_deduction_amount",
            "insurance_deduction_amount",
            "other_deduction_amount",
        ]:
            value = cleaned_data.get(field) or Decimal("0.00")

            if value < 0:
                self.add_error(field, "Amount cannot be negative.")

        return cleaned_data

    
class EmployeeExtraWorkDayRequestForm(forms.ModelForm):
    class Meta:
        model = EmployeeExtraWorkDayRequest
        fields = ["work_date", "reason"]

        widgets = {
            "work_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "reason": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Why do you want to work on this non-working day?"
            }),
        }


class ExtraWorkDayManagerApprovalForm(forms.ModelForm):
    class Meta:
        model = EmployeeExtraWorkDayRequest
        fields = ["manager_remarks"]

        widgets = {
            "manager_remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Manager remarks"
            }),
        }


class ExtraWorkDayHRApprovalForm(forms.ModelForm):
    class Meta:
        model = EmployeeExtraWorkDayRequest
        fields = ["hr_remarks"]

        widgets = {
            "hr_remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "HR remarks"
            }),
        }


class DealerVisitForm(forms.ModelForm):
    class Meta:
        model = DealerVisit
        fields = [
            "dealer",
            "visit_date",
            "reason",
            "note",
        ]

        widgets = {
            "dealer": forms.Select(attrs={
                "class": "form-control",
                "id": "id_dealer"
            }),
            "visit_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
                "id": "id_visit_date"
            }),
            "reason": forms.Select(attrs={
                "class": "form-control",
                "id": "id_reason"
            }),
            "note": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter visit notes"
            }),
        }

    def __init__(self, *args, **kwargs):
        request_user = kwargs.pop("request_user", None)
        super().__init__(*args, **kwargs)

        dealers = Dealer.objects.filter(
            approval_status="APPROVED",
            is_active=True
        ).order_by("firm_name")

        if request_user:
            profile = getattr(request_user, "profile", None)
            role = profile.role if profile else ""

            if role in ["SALES_OFFICER_SENIOR", "SALES_OFFICER_JUNIOR"]:
                dealers = dealers.filter(created_by_sales_officer=request_user)

            elif role == "ASM":
                dealers = dealers.filter(concerned_asm=request_user)

        self.fields["dealer"].queryset = dealers

        self.fields["dealer"].label_from_instance = lambda obj: (
            f"{obj.firm_name} - {obj.dealer_code}" if obj.dealer_code else obj.firm_name
        )

        
        
class DealerCreditScoreForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = [
            "credit_score",
            "credit_score_note",
        ]

        widgets = {
            "credit_score": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "300",
                "max": "900",
                "placeholder": "Example: 711"
            }),
            "credit_score_note": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: Good payment history / overdue payment"
            }),
        }

    def clean_credit_score(self):
        score = self.cleaned_data.get("credit_score")

        if score < 300 or score > 900:
            raise forms.ValidationError("Credit score must be between 300 and 900.")

        return score



# ==========================================================
# SIMPLE PURCHASE MODULE - FORMS
# Paste this at the bottom of core/forms.py
# ==========================================================

from decimal import Decimal
from django import forms
from django.forms import formset_factory




class ProductPackChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        product = getattr(obj, "product", None)

        product_name = getattr(product, "name", "") if product else ""
        product_custom_id = getattr(product, "product_id", "") if product else ""
        product_db_id = getattr(product, "id", "") if product else ""

        pack_id = getattr(obj, "id", "")
        pack = f"{obj.pack_size} {obj.unit}"
        box = f"{obj.units_per_box} in 1 {obj.packing_type}" if getattr(obj, "units_per_box", None) else obj.packing_type
        stock = getattr(obj, "stock_boxes", 0)

        product_id_text = product_custom_id if product_custom_id else product_db_id

        return (
            f"{product_name} | "
            f"Product ID: {product_id_text} | "
            f"Pack ID: {pack_id} | "
            f"{pack} | "
            f"{box} | "
            f"Stock: {stock}"
        )

        
class InventoryItemChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        sku = f" | SKU: {obj.sku_code}" if obj.sku_code else ""
        return f"{obj.name} | Stock: {obj.stock_quantity} {obj.stock_unit}{sku}"


class PurchaseBillChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        party_name = obj.party.party_name if obj.party else "-"
        bill_date = obj.bill_date.strftime("%d/%m/%Y") if obj.bill_date else "-"
        grand_total = getattr(obj, "grand_total", 0)
        balance = getattr(obj, "balance_amount", 0)

        return (
            f"{obj.bill_number} | "
            f"{bill_date} | "
            f"{party_name} | "
            f"Total ₹{grand_total} | "
            f"Balance ₹{balance}"
        )

class SimplePurchaseEntryForm(forms.Form):
    party = forms.ModelChoiceField(
        queryset=PurchaseParty.objects.none(),
        required=False,
        empty_label="Select existing party",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    new_party_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Or type new party / supplier name"
        })
    )

    party_phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Party phone optional"
        })
    )

    party_gst = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Party GST optional"
        })
    )

    purchase_type = forms.ModelChoiceField(
        queryset=PurchaseType.objects.none(),
        required=False,
        empty_label="Select purchase type",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    new_purchase_type = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Or type new purchase type"
        })
    )

    bill_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Supplier bill number"
        })
    )

    bill_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            "class": "form-control",
            "type": "date"
        })
    )

    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Purchase note optional"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["party"].queryset = PurchaseParty.objects.filter(
            is_active=True
        ).order_by("party_name")

        self.fields["purchase_type"].queryset = PurchaseType.objects.filter(
            is_active=True
        ).order_by("name")

    def clean(self):
        cleaned = super().clean()

        party = cleaned.get("party")
        new_party_name = (cleaned.get("new_party_name") or "").strip()

        purchase_type = cleaned.get("purchase_type")
        new_purchase_type = (cleaned.get("new_purchase_type") or "").strip()

        if not party and not new_party_name:
            self.add_error("new_party_name", "Select existing party or enter new party name.")

        if not purchase_type and not new_purchase_type:
            self.add_error("new_purchase_type", "Select existing purchase type or enter new purchase type.")

        return cleaned


class SimplePurchaseItemForm(forms.Form):
    item = InventoryItemChoiceField(
        queryset=InventoryItem.objects.none(),
        required=False,
        empty_label="Select existing item",
        widget=forms.Select(attrs={"class": "form-control item-select"})
    )

    new_item_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Or type new item name"
        })
    )

    sku_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "SKU optional"
        })
    )

    item_type = forms.ChoiceField(
        choices=InventoryItem.ITEM_TYPE_CHOICES,
        required=True,
        initial="RAW_MATERIAL",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    unit = forms.ChoiceField(
        choices=PURCHASE_UNIT_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    quantity = forms.DecimalField(
        required=False,
        max_digits=14,
        decimal_places=3,
        min_value=Decimal("0.001"),
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.001",
            "placeholder": "Qty"
        })
    )

    purchase_price = forms.DecimalField(
        required=False,
        max_digits=14,
        decimal_places=2,
        min_value=Decimal("0.00"),
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.01",
            "placeholder": "Rate"
        })
    )

    gst_percent = forms.DecimalField(
        required=False,
        max_digits=6,
        decimal_places=2,
        initial=Decimal("0.00"),
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.01",
            "placeholder": "GST %"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["item"].queryset = InventoryItem.objects.filter(
            is_active=True
        ).order_by("name")

    def is_blank_row(self):
        data = self.cleaned_data if hasattr(self, "cleaned_data") else {}
        return not any([
            data.get("item"),
            (data.get("new_item_name") or "").strip(),
            data.get("quantity"),
            data.get("purchase_price"),
        ])

    def clean(self):
        cleaned = super().clean()

        marked_delete = cleaned.get("DELETE")
        if marked_delete:
            return cleaned

        item = cleaned.get("item")
        new_item_name = (cleaned.get("new_item_name") or "").strip()
        quantity = cleaned.get("quantity")
        purchase_price = cleaned.get("purchase_price")

        if not item and not new_item_name and not quantity and not purchase_price:
            return cleaned

        if not item and not new_item_name:
            self.add_error("new_item_name", "Select item or enter new item name.")

        if not quantity or quantity <= 0:
            self.add_error("quantity", "Quantity is required.")

        if purchase_price is None or purchase_price < 0:
            self.add_error("purchase_price", "Purchase price is required.")

        return cleaned


SimplePurchaseItemFormSet = formset_factory(
    SimplePurchaseItemForm,
    extra=1,
    can_delete=True
)


class SimplePaymentOutForm(forms.ModelForm):
    bill = PurchaseBillChoiceField(
        queryset=PurchaseBill.objects.none(),
        required=True,
        empty_label="Select unpaid / partial purchase bill",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = PurchasePaymentOut
        fields = [
            "bill",
            "payment_date",
            "amount",
            "payment_mode",
            "reference_number",
            "cheque_number",
            "payment_screenshot",
            "note",
        ]

        widgets = {
            "payment_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Paid amount"
            }),
            "payment_mode": forms.Select(attrs={"class": "form-control"}),
            "reference_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "UPI / Bank reference number"
            }),
            "cheque_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Cheque number"
            }),
            "payment_screenshot": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "note": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Payment note optional"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["bill"].queryset = PurchaseBill.objects.select_related(
            "party"
        ).filter(
            balance_amount__gt=0
        ).order_by("-id")


class SimplePurchaseReturnForm(forms.Form):
    bill = PurchaseBillChoiceField(
        queryset=PurchaseBill.objects.none(),
        required=True,
        empty_label="Select purchase bill",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    return_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            "class": "form-control",
            "type": "date"
        })
    )

    reason = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Reason for return / debit note"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show all purchase bills which have items.
        # Do not filter only stock_added=True because asset bills / edited bills may hide.
        self.fields["bill"].queryset = PurchaseBill.objects.select_related(
            "party"
        ).filter(
            items__isnull=False
        ).distinct().order_by("-id")


class SimpleReturnItemForm(forms.Form):
    inventory_item = InventoryItemChoiceField(
        queryset=InventoryItem.objects.none(),
        required=True,
        empty_label="Select returned item",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    quantity = forms.DecimalField(
        required=True,
        max_digits=14,
        decimal_places=3,
        min_value=Decimal("0.001"),
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.001",
            "placeholder": "Return quantity"
        })
    )

    unit = forms.ChoiceField(
        choices=PURCHASE_UNIT_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    return_price = forms.DecimalField(
        required=True,
        max_digits=14,
        decimal_places=2,
        min_value=Decimal("0.00"),
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.01",
            "placeholder": "Return price"
        })
    )

    gst_percent = forms.DecimalField(
        required=False,
        max_digits=6,
        decimal_places=2,
        initial=Decimal("0.00"),
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.01",
            "placeholder": "GST %"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["inventory_item"].queryset = InventoryItem.objects.filter(
            is_active=True
        ).order_by("name")


SimpleReturnItemFormSet = formset_factory(
    SimpleReturnItemForm,
    extra=1,
    can_delete=True
)


class SimpleMakeProductForm(forms.Form):
    production_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Example: Final Product Mix / Repacking 1KG"
        })
    )

    output_product_pack = ProductPackChoiceField(
        queryset=ProductPackSize.objects.none(),
        required=True,
        empty_label="Select final product pack to increase stock",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    output_boxes = forms.IntegerField(
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Final output boxes / pieces"
        })
    )

    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Production / repacking note optional"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["output_product_pack"].queryset = ProductPackSize.objects.select_related(
            "product",
            "warehouse",
        ).filter(
            is_active=True
        ).order_by(
            "product__name",
            "pack_size",
        )


class SimpleMakeProductItemForm(forms.Form):
    inventory_item = InventoryItemChoiceField(
        queryset=InventoryItem.objects.none(),
        required=True,
        empty_label="Select used raw/packing item",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    quantity = forms.DecimalField(
        required=True,
        max_digits=14,
        decimal_places=3,
        min_value=Decimal("0.001"),
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.001",
            "placeholder": "Used qty"
        })
    )

    unit = forms.ChoiceField(
        choices=PURCHASE_UNIT_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["inventory_item"].queryset = InventoryItem.objects.filter(
            is_active=True
        ).order_by("name")


SimpleMakeProductItemFormSet = formset_factory(
    SimpleMakeProductItemForm,
    extra=1,
    can_delete=True
)


# ==========================================================
# MAIN WAREHOUSE DEFAULT + STOCK TRANSFER - FORMS
# Paste this at the bottom of core/forms.py
#
# IMPORTANT:
# This redefines ProductPackSizeForm and ProductPackSizeFormSet so
# warehouse is not asked during product creation/edit.
# ==========================================================

from decimal import Decimal
from django import forms
from django.forms import inlineformset_factory

from .models import Warehouse, Product, ProductPackSize


MAIN_WAREHOUSE_NAME = "Main Warehouse"


def get_default_main_warehouse():
    main = Warehouse.objects.filter(name__iexact=MAIN_WAREHOUSE_NAME).first()

    if main:
        return main

    return Warehouse.objects.order_by("id").first()


class ProductPackSizeForm(forms.ModelForm):
    class Meta:
        model = ProductPackSize
        fields = [
            "warehouse",
            "pack_size",
            "unit",
            "packing_type",
            "units_per_box",
            "mrp_per_unit",
            "sale_price_per_unit",
            "purchase_price_per_unit",
            "stock_boxes",
            "is_active",
        ]

        widgets = {
            "warehouse": forms.HiddenInput(),
            "pack_size": forms.NumberInput(attrs={"class": "form-control", "step": "0.001"}),
            "unit": forms.Select(attrs={"class": "form-control"}),
            "packing_type": forms.Select(attrs={"class": "form-control"}),
            "units_per_box": forms.NumberInput(attrs={"class": "form-control", "step": "0.001"}),
            "mrp_per_unit": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "sale_price_per_unit": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "purchase_price_per_unit": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "stock_boxes": forms.NumberInput(attrs={"class": "form-control", "step": "0.001"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

        labels = {
            "stock_boxes": "Main Warehouse Stock",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main = get_default_main_warehouse()

        if "warehouse" in self.fields:
            self.fields["warehouse"].required = False
            self.fields["warehouse"].widget = forms.HiddenInput()

            if main:
                self.fields["warehouse"].initial = main.id

        for name, field in self.fields.items():
            if name != "is_active":
                field.widget.attrs.setdefault("class", "form-control")

    def clean_warehouse(self):
        if self.instance and self.instance.pk and self.instance.warehouse_id:
            return self.instance.warehouse

        main = get_default_main_warehouse()

        if not main:
            raise forms.ValidationError(
                "Please create one warehouse first. Name it 'Main Warehouse'."
            )

        return main


ProductPackSizeFormSet = inlineformset_factory(
    Product,
    ProductPackSize,
    form=ProductPackSizeForm,
    extra=1,
    can_delete=True,
)


class TransferProductPackChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        product = getattr(obj, "product", None)

        product_name = getattr(product, "name", "") if product else ""
        product_custom_id = getattr(product, "product_id", "") if product else ""
        product_db_id = getattr(product, "id", "") if product else ""
        product_id_text = product_custom_id if product_custom_id else product_db_id

        pack_text = f"{obj.pack_size} {obj.unit}"
        box_text = f"{obj.units_per_box} in 1 {obj.packing_type}" if getattr(obj, "units_per_box", None) else obj.packing_type
        stock = getattr(obj, "stock_boxes", 0)

        return (
            f"{product_name} | "
            f"Product ID: {product_id_text} | "
            f"Pack ID: {obj.id} | "
            f"{pack_text} | "
            f"{box_text} | "
            f"Main Stock: {stock}"
        )


class ProductStockTransferForm(forms.Form):
    product_pack = TransferProductPackChoiceField(
        queryset=ProductPackSize.objects.none(),
        required=True,
        empty_label="Search product / product id / pack id",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    to_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.none(),
        required=True,
        empty_label="Select warehouse to transfer stock",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    quantity_boxes = forms.DecimalField(
        required=True,
        max_digits=14,
        decimal_places=3,
        min_value=Decimal("0.001"),
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.001",
            "placeholder": "How many boxes / pieces to transfer?"
        })
    )

    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Transfer note optional"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main = get_default_main_warehouse()

        if main:
            self.fields["product_pack"].queryset = ProductPackSize.objects.select_related(
                "product",
                "warehouse",
            ).filter(
                warehouse=main,
                is_active=True,
            ).order_by("product__name", "pack_size")

            self.fields["to_warehouse"].queryset = Warehouse.objects.exclude(
                id=main.id
            ).order_by("name")
        else:
            self.fields["product_pack"].queryset = ProductPackSize.objects.none()
            self.fields["to_warehouse"].queryset = Warehouse.objects.none()

    def clean(self):
        cleaned = super().clean()

        source_pack = cleaned.get("product_pack")
        to_warehouse = cleaned.get("to_warehouse")
        quantity = cleaned.get("quantity_boxes")

        if not source_pack or not quantity:
            return cleaned

        if to_warehouse and source_pack.warehouse_id == to_warehouse.id:
            self.add_error("to_warehouse", "Cannot transfer to same warehouse.")

        available = source_pack.stock_boxes or Decimal("0.000")

        if quantity > available:
            self.add_error(
                "quantity_boxes",
                f"Only {available} available in Main Warehouse."
            )

        return cleaned


