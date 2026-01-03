import re
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def validate_nepal_nid(value):
    """
    Validate Nepal NID format: District-Ward-Number
    Format: XX-XX-XXXXXXXX (e.g., 01-05-12345678)
    District: 01-77 (77 districts in Nepal)
    Ward: 01-32 (max wards in a municipality)
    Number: 8 digit unique number
    """
    pattern = r'^([0-7][0-9]|0[1-9])-([0-2][0-9]|3[0-2]|0[1-9])-\d{8}$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Invalid Nepal NID format. Expected: District-Ward-Number (e.g., 01-05-12345678)'
        )


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('PUBLIC', 'Public'),
        ('CONTRACTOR', 'Contractor'),
        ('GOVERNMENT', 'Government'),
        ('AUDITOR', 'Auditor'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PUBLIC')
    # ✅ NID Verification - Nepal format (District-Ward-Number)
    nepal_nid = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        validators=[validate_nepal_nid],
        help_text="Nepal NID format: District-Ward-Number (e.g., 01-05-12345678)"
    )
    nid_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


# ✅ Contractor Qualification System - Certificates, skills, experience, tests
class ContractorProfile(models.Model):
    """Extended profile for contractors with qualification system"""
    SKILL_LEVEL_CHOICES = (
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
        ('EXPERT', 'Expert'),
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='contractor_profile'
    )
    
    # ✅ Smart Rating System - Harder to gain points, easier to lose (asymmetric)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=Decimal('5.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('5.00'))]
    )
    total_projects_completed = models.PositiveIntegerField(default=0)
    total_projects_failed = models.PositiveIntegerField(default=0)
    
    # ✅ Suspension System - Contractors below 3.8 rating are suspended
    is_suspended = models.BooleanField(default=False)
    suspension_reason = models.TextField(blank=True)
    suspended_at = models.DateTimeField(null=True, blank=True)
    
    # Qualification fields
    years_of_experience = models.PositiveIntegerField(default=0)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='BEGINNER')
    
    # Test scores
    qualification_test_score = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MaxValueValidator(100)],
        help_text="Score from qualification test (0-100)"
    )
    test_passed = models.BooleanField(default=False)
    test_taken_at = models.DateTimeField(null=True, blank=True)
    
    # ✅ AI Integration Ready - Placeholder for AI-based contractor ratings
    ai_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="AI-generated rating based on historical performance"
    )
    ai_rating_updated_at = models.DateTimeField(null=True, blank=True)
    ai_risk_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="AI-calculated risk score for project delays/failures"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Contractor: {self.user.username} (Rating: {self.rating})"
    
    def update_rating(self, points, is_positive=True):
        """
        ✅ Smart Rating System - Asymmetric rating calculation
        Harder to gain points (0.5x), easier to lose (1.5x)
        """
        if is_positive:
            # Harder to gain points - only get 50% of positive points
            adjusted_points = Decimal(str(points)) * Decimal('0.5')
        else:
            # Easier to lose points - lose 150% of negative points
            adjusted_points = Decimal(str(points)) * Decimal('1.5')
        
        if is_positive:
            self.rating = min(Decimal('5.00'), self.rating + adjusted_points)
        else:
            self.rating = max(Decimal('0.00'), self.rating - adjusted_points)
        
        # ✅ Suspension System - Auto-suspend if rating drops below 3.8
        if self.rating < Decimal('3.80'):
            self.is_suspended = True
            self.suspension_reason = f"Rating dropped below 3.8 (Current: {self.rating})"
            from django.utils import timezone
            self.suspended_at = timezone.now()
        
        self.save()
        return self.rating
    
    def check_contract_eligibility(self, contract_size):
        """
        ✅ Contract Size Categories - Check if contractor is eligible for contract size
        """
        if self.is_suspended:
            return False, "Contractor is suspended"
        
        requirements = {
            'SMALL': Decimal('3.00'),
            'MEDIUM': Decimal('3.50'),
            'LARGE': Decimal('4.00'),
        }
        
        required_rating = requirements.get(contract_size, Decimal('3.00'))
        if self.rating < required_rating:
            return False, f"Rating {self.rating} below required {required_rating} for {contract_size} contracts"
        
        return True, "Eligible"


# ✅ Contractor Certificates
class ContractorCertificate(models.Model):
    """Certificates held by contractors"""
    contractor = models.ForeignKey(
        ContractorProfile, 
        on_delete=models.CASCADE, 
        related_name='certificates'
    )
    name = models.CharField(max_length=200)
    issuing_authority = models.CharField(max_length=200)
    certificate_number = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    document = models.FileField(upload_to='certificates/', null=True, blank=True)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.contractor.user.username}"
    
    @property
    def is_valid(self):
        from django.utils import timezone
        if self.expiry_date:
            return self.expiry_date >= timezone.now().date()
        return True


# ✅ Contractor Skills
class ContractorSkill(models.Model):
    """Skills possessed by contractors"""
    contractor = models.ForeignKey(
        ContractorProfile, 
        on_delete=models.CASCADE, 
        related_name='skills'
    )
    skill_name = models.CharField(max_length=100)
    proficiency_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Proficiency level from 1-10"
    )
    years_of_practice = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['contractor', 'skill_name']
    
    def __str__(self):
        return f"{self.skill_name} (Level {self.proficiency_level}) - {self.contractor.user.username}"


class Project(models.Model):
    # ✅ Contract Size Categories - Small, Medium, Large with rating requirements
    CONTRACT_SIZE_CHOICES = (
        ('SMALL', 'Small (< 10 Lakh)'),
        ('MEDIUM', 'Medium (10 Lakh - 1 Crore)'),
        ('LARGE', 'Large (> 1 Crore)'),
    )
    
    STATUS_CHOICES = (
        ('PLANNING', 'Planning'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('DELAYED', 'Delayed'),
        ('ABANDONED', 'Abandoned'),
    )
    
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    ministry = models.CharField(max_length=200)
    contractor = models.CharField(max_length=200)
    contractor_profile = models.ForeignKey(
        ContractorProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects'
    )
    total_budget = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # ✅ Contract Size Categories
    contract_size = models.CharField(
        max_length=10, 
        choices=CONTRACT_SIZE_CHOICES, 
        default='SMALL'
    )
    min_contractor_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=Decimal('3.00'),
        help_text="Minimum contractor rating required for this project"
    )
    
    # ✅ Work Longevity Tracking - Expected vs actual lifespan of projects
    expected_lifespan_years = models.PositiveIntegerField(
        default=10,
        help_text="Expected lifespan of the completed work in years"
    )
    actual_lifespan_years = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Actual lifespan (filled when work deteriorates)"
    )
    warranty_period_years = models.PositiveIntegerField(
        default=1,
        help_text="Warranty period in years"
    )
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING')
    
    # ✅ Blockchain Ready - Schema prepared for transaction recording
    blockchain_tx_hash = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Blockchain transaction hash for project creation"
    )
    blockchain_contract_address = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Smart contract address on blockchain"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def calculate_contract_size(self):
        """Automatically determine contract size based on budget"""
        budget = self.total_budget
        if budget < 1000000:  # < 10 Lakh
            return 'SMALL'
        elif budget < 10000000:  # < 1 Crore
            return 'MEDIUM'
        else:
            return 'LARGE'
    
    def save(self, *args, **kwargs):
        # Auto-calculate contract size based on budget
        self.contract_size = self.calculate_contract_size()
        # Set minimum rating requirement based on contract size
        rating_requirements = {
            'SMALL': Decimal('3.00'),
            'MEDIUM': Decimal('3.50'),
            'LARGE': Decimal('4.00'),
        }
        self.min_contractor_rating = rating_requirements.get(self.contract_size, Decimal('3.00'))
        super().save(*args, **kwargs)


class Fund(models.Model):
    """
    Fund model with blockchain-ready fields for transaction recording
    """
    project = models.ForeignKey(
        Project,
        related_name="funds",
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    released_at = models.DateTimeField(auto_now_add=True)
    
    # ✅ Blockchain Ready - Transaction recording fields
    blockchain_tx_hash = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Blockchain transaction hash for fund release"
    )
    blockchain_confirmed = models.BooleanField(default=False)
    blockchain_block_number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.project.name} - {self.amount}"


# ✅ Material Transparency - Detailed material pricing in plans and payments
class Material(models.Model):
    """Material used in projects with detailed pricing"""
    UNIT_CHOICES = (
        ('KG', 'Kilogram'),
        ('TON', 'Ton'),
        ('UNIT', 'Unit/Piece'),
        ('LITER', 'Liter'),
        ('SQFT', 'Square Feet'),
        ('SQMT', 'Square Meter'),
        ('CUFT', 'Cubic Feet'),
        ('CUMT', 'Cubic Meter'),
        ('BAG', 'Bag'),
        ('BUNDLE', 'Bundle'),
    )
    
    project = models.ForeignKey(
        Project,
        related_name="materials",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='UNIT')
    
    # Pricing details
    planned_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    actual_quantity = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_planned_cost = models.DecimalField(max_digits=14, decimal_places=2, editable=False)
    total_actual_cost = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    
    # Supplier information
    supplier_name = models.CharField(max_length=200, blank=True)
    supplier_contact = models.CharField(max_length=100, blank=True)
    
    # Quality and verification
    quality_grade = models.CharField(max_length=50, blank=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculate total planned cost
        self.total_planned_cost = self.planned_quantity * self.unit_price
        # Calculate actual cost if actual quantity is provided
        if self.actual_quantity is not None:
            self.total_actual_cost = self.actual_quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.project.name}"
    
    @property
    def cost_variance(self):
        """Calculate cost variance between planned and actual"""
        if self.total_actual_cost:
            return self.total_actual_cost - self.total_planned_cost
        return None


# ✅ Material Payment - Track payments for materials
class MaterialPayment(models.Model):
    """Payment records for materials"""
    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('PARTIAL', 'Partial'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    material = models.ForeignKey(
        Material,
        related_name="payments",
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_reference = models.CharField(max_length=100)
    status = models.CharField(max_length=15, choices=PAYMENT_STATUS, default='PENDING')
    
    # ✅ Blockchain Ready
    blockchain_tx_hash = models.CharField(max_length=100, blank=True, null=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment {self.payment_reference} - {self.material.name}"


class Progress(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    
    project = models.ForeignKey(
        Project,
        related_name="progress",
        on_delete=models.CASCADE
    )
    physical_progress = models.PositiveIntegerField()
    financial_progress = models.PositiveIntegerField()
    report_url = models.URLField(blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='submitted_progress')
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_progress')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # ✅ Time-Based Reporting - Track submission time
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    # ✅ Blockchain Ready
    blockchain_tx_hash = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        if self.physical_progress > 100 or self.financial_progress > 100:
            raise ValidationError("Progress cannot exceed 100%")
        
        # ✅ Time-Based Reporting - Contractors can only submit reports after 5 PM
        # This validation is also enforced in the API view
        from django.utils import timezone
        current_time = timezone.localtime(timezone.now())
        if current_time.hour < 17:  # Before 5 PM (17:00)
            raise ValidationError(
                "Progress reports can only be submitted after 5:00 PM. "
                f"Current time: {current_time.strftime('%H:%M')}"
            )

    def __str__(self):
        return f"{self.project.name} - {self.date}"


# ✅ OPTION E — AUDIT LOG
class AuditLog(models.Model):
    ACTION_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} {self.model_name} ({self.object_id})"

class ProgressImage(models.Model):
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='progress_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.progress}"


# ✅ Issue Reporting System - Distinguish between natural disasters and contractor faults
class IssueReport(models.Model):
    """
    System to report issues distinguishing between natural disasters and contractor faults
    """
    ISSUE_TYPE_CHOICES = (
        ('NATURAL_DISASTER', 'Natural Disaster'),
        ('CONTRACTOR_FAULT', 'Contractor Fault'),
        ('DESIGN_FLAW', 'Design Flaw'),
        ('MATERIAL_DEFECT', 'Material Defect'),
        ('VANDALISM', 'Vandalism'),
        ('NORMAL_WEAR', 'Normal Wear and Tear'),
        ('OTHER', 'Other'),
    )
    
    SEVERITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    )
    
    STATUS_CHOICES = (
        ('REPORTED', 'Reported'),
        ('UNDER_REVIEW', 'Under Review'),
        ('VERIFIED', 'Verified'),
        ('FORGIVEN', 'Forgiven'),
        ('PENALIZED', 'Penalized'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    )
    
    project = models.ForeignKey(
        Project,
        related_name="issues",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='REPORTED')
    
    # ✅ Forgiveness System - Natural disasters can be forgiven vs contractor faults
    is_forgivable = models.BooleanField(default=False)
    forgiveness_reason = models.TextField(blank=True)
    is_forgiven = models.BooleanField(default=False)
    forgiven_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='forgiven_issues'
    )
    forgiven_at = models.DateTimeField(null=True, blank=True)
    
    # Reporter information
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reported_issues'
    )
    reported_at = models.DateTimeField(auto_now_add=True)
    
    # Verification
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_issues'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Rating impact
    rating_impact = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Rating points deducted from contractor"
    )
    
    # Resolution
    resolution_notes = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.project.name}"
    
    def save(self, *args, **kwargs):
        # ✅ Forgiveness System - Natural disasters are forgivable by default
        if self.issue_type == 'NATURAL_DISASTER':
            self.is_forgivable = True
        elif self.issue_type in ['CONTRACTOR_FAULT', 'DESIGN_FLAW', 'MATERIAL_DEFECT']:
            self.is_forgivable = False
        super().save(*args, **kwargs)
    
    def apply_penalty(self, contractor_profile):
        """Apply rating penalty to contractor if not forgiven"""
        if not self.is_forgiven and self.issue_type == 'CONTRACTOR_FAULT':
            severity_penalties = {
                'LOW': Decimal('0.1'),
                'MEDIUM': Decimal('0.25'),
                'HIGH': Decimal('0.5'),
                'CRITICAL': Decimal('1.0'),
            }
            penalty = severity_penalties.get(self.severity, Decimal('0.25'))
            self.rating_impact = penalty
            contractor_profile.update_rating(penalty, is_positive=False)
            self.status = 'PENALIZED'
            self.save()
            return penalty
        return Decimal('0')


# ✅ Issue Evidence - Photos/videos for issue reports
class IssueEvidence(models.Model):
    """Evidence (photos/videos) for issue reports"""
    EVIDENCE_TYPE_CHOICES = (
        ('PHOTO', 'Photo'),
        ('VIDEO', 'Video'),
        ('DOCUMENT', 'Document'),
    )
    
    issue = models.ForeignKey(
        IssueReport,
        related_name="evidence",
        on_delete=models.CASCADE
    )
    evidence_type = models.CharField(max_length=10, choices=EVIDENCE_TYPE_CHOICES, default='PHOTO')
    file = models.FileField(upload_to='issue_evidence/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.evidence_type} for {self.issue.title}"


# ✅ Proof-Based Ratings - Negative ratings require photo/video evidence
class ContractorRating(models.Model):
    """
    Rating system for contractors with proof requirements for negative ratings
    """
    contractor = models.ForeignKey(
        ContractorProfile,
        related_name="ratings",
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project,
        related_name="contractor_ratings",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    rated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='given_ratings'
    )
    
    # Rating details
    rating_value = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1-5"
    )
    comment = models.TextField(blank=True)
    
    # ✅ Proof-Based Ratings - Evidence required for negative ratings
    is_negative = models.BooleanField(default=False)
    evidence_required = models.BooleanField(default=False)
    evidence_provided = models.BooleanField(default=False)
    
    # Status
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_ratings'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['contractor', 'project', 'rated_by']
    
    def __str__(self):
        return f"Rating {self.rating_value} for {self.contractor.user.username}"
    
    def save(self, *args, **kwargs):
        # ✅ Proof-Based Ratings - Negative ratings (<=2) require evidence
        if self.rating_value <= 2:
            self.is_negative = True
            self.evidence_required = True
        else:
            self.is_negative = False
            self.evidence_required = False
        super().save(*args, **kwargs)
    
    def apply_to_contractor(self):
        """Apply rating impact to contractor's overall rating"""
        if self.is_negative and self.evidence_required and not self.evidence_provided:
            # Don't apply negative rating without evidence
            return False
        
        # Calculate points based on rating
        # Rating 5 = +0.2, Rating 4 = +0.1, Rating 3 = 0, Rating 2 = -0.1, Rating 1 = -0.2
        points = (self.rating_value - 3) * Decimal('0.1')
        is_positive = points >= 0
        self.contractor.update_rating(abs(points), is_positive=is_positive)
        return True


# ✅ Rating Evidence - Evidence for contractor ratings
class RatingEvidence(models.Model):
    """Evidence attached to contractor ratings"""
    EVIDENCE_TYPE_CHOICES = (
        ('PHOTO', 'Photo'),
        ('VIDEO', 'Video'),
        ('DOCUMENT', 'Document'),
    )
    
    rating = models.ForeignKey(
        ContractorRating,
        related_name="evidence",
        on_delete=models.CASCADE
    )
    evidence_type = models.CharField(max_length=10, choices=EVIDENCE_TYPE_CHOICES, default='PHOTO')
    file = models.FileField(upload_to='rating_evidence/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.evidence_type} for rating {self.rating.id}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mark rating as having evidence provided
        self.rating.evidence_provided = True
        self.rating.save()

