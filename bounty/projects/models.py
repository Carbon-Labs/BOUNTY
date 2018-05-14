from django.db import models
from smart_selects.db_fields import ChainedForeignKey
import uuid

class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

class SubCategories(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Sub Category")
        verbose_name_plural = ("Sub Categories")

class Client(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    email = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(blank=True, upload_to='images/clients/profiles')
    website = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    DISABLED = 'DISABLED'
    STATUS_CHOICES = (
        (NEW, 'New'),
        (ACTIVE, 'Active'),
        (DISABLED, 'Disabled'),
    )
    name = models.CharField(max_length=60)
    blurb = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    subcategory = ChainedForeignKey(
        SubCategories,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    description = models.TextField()
    status = models.CharField(
        max_length = 10,
        choices = STATUS_CHOICES,
        default = NEW,
    )
    thumbnail = models.ImageField(blank=True, upload_to='images/projects')
    featured = models.BooleanField(default=0)
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(blank=False, unique=True)

    def __str__(self):
        return self.name

class Developer(models.Model):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    DISABLED = 'DISABLED'
    STATUS_CHOICES = (
        (NEW, 'New'),
        (ACTIVE, 'Active'),
        (DISABLED, 'Disabled'),
    )

    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    bio = models.TextField()
    url = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    github_name = models.CharField(max_length=50)
    status = models.CharField(
        max_length = 10,
        choices = STATUS_CHOICES,
        default = NEW,
    )

    def __str__(self):
        return self.name

class Tasks(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    short_description = models.CharField(max_length=100)
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    long_description = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=30,decimal_places=18, default=0)
    funding = models.DecimalField(max_digits=30,decimal_places=18, blank=True, default=0)
    class Meta:
        verbose_name = ("Task")
        verbose_name_plural = ("Tasks")

    def __str__(self):
        return self.short_description

    @property
    def remaining(self):
        return self.budget - self.funding

class FundingMethods(models.Model):
    name = models.CharField(max_length=100)
    token_id = models.CharField(max_length=4, help_text="This has to match the Exchange")
    url = models.CharField(max_length=100, blank=True)
    amount_held = models.DecimalField(max_digits=30,decimal_places=18, default=0, blank=True)
    class Meta:
        verbose_name = ("Funding Method")
        verbose_name_plural = ("Funding Methods")

    def __str__(self):
        return self.name

class Fundings(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    task = models.ForeignKey(Tasks, on_delete=models.DO_NOTHING)
    token = models.ForeignKey(FundingMethods, on_delete=models.DO_NOTHING)
    sender = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=30,decimal_places=18)
    memo = models.CharField(max_length=100)
    created_at = models.DateTimeField('Created', auto_now_add=True)

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name = ("Funding")
        verbose_name_plural = ("Fundings")
