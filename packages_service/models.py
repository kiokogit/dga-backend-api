from django.db import models
import uuid
# Create your models here.


PRICE_TYPES = [
    ('PER PERSON PER DAY', 'PER PERSON PER DAY'),
    ('PER PERSON PER WHOLE TRIP', 'PER PERSON PER WHOLE TRIP'),
    ('PER GROUP', 'PER GROUP'),
    ('OTHER', 'OTHER')
]

# basic model
class BaseModel(models.Model):
    id=models.UUIDField(default=uuid.uuid4(), primary_key=True, max_length=50, editable=False)
    date_created=models.DateTimeField(auto_now=True) 
    date_modified=models.DateTimeField(auto_now_add=True)
    
    
class BaseModelWithStatus(BaseModel):
    is_active=models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)
    date_deleted=models.DateTimeField(blank=True, null=True)


class PackageModel(BaseModelWithStatus):
    title=models.CharField(max_length=100)
    reference_number=models.CharField(max_length=50, unique=True)
    description=models.TextField(blank=True, null=True)
    cover_image=models.TextField(blank=True, null=True)
    package_particulars=models.TextField(blank=True, null=True)
    requirements=models.TextField(blank=True, null=True)
    tie_to_event=models.BooleanField(default=False)
    expire_after_event=models.BooleanField(default=False)
    created_by=models.UUIDField(blank=True, null=True)


class PackageLocationModel(BaseModel):
    country=models.CharField(max_length=100, blank=True, null=True)
    county=models.CharField(max_length=100, blank=True, null=True)
    city_town=models.CharField(max_length=100, blank=True, null=True)
    # geolocation=models.JSONField(blank=True, null=True)
    lat = models.CharField(max_length=50, blank=True, null=True)
    lng = models.CharField(max_length=50, blank=True, null=True)
    package=models.ForeignKey(
        PackageModel,
        on_delete=models.CASCADE,
        related_name='location'
    )

class PackageCurrencyModel(BaseModelWithStatus):
    type=models.CharField(max_length=100, choices=PRICE_TYPES, blank=True, null=True)
    currency=models.CharField(max_length=100, blank=True, null=True)
    amount=models.CharField(max_length=100, blank=True, null=True)
    package=models.ForeignKey(
        PackageModel,
        on_delete=models.CASCADE,
        related_name='price'
    )


class PackageImagesModel(BaseModelWithStatus):
    image=models.TextField(blank=True, null=True)
    uploaded_by=models.UUIDField(blank=True, null=True)
    description=models.CharField(max_length=100, blank=True, null=True)
    package=models.ForeignKey(
        PackageModel,
        on_delete=models.CASCADE,
        related_name='images'
    )


class PackageReviewsModel(BaseModel):
    rating=models.IntegerField(default=0)
    review_text=models.TextField(blank=True, null=True)
    reviewed_by=models.CharField(max_length=100, default='Anonymous')
    package=models.ForeignKey(
        PackageModel,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

class PackageTimelinesModel(BaseModelWithStatus):
    package_from=models.DateTimeField(blank=True, null=True)
    package_to=models.DateTimeField(blank=True, null=True)
    no_of_days=models.IntegerField(blank=True, null=True)
    no_of_nights=models.IntegerField(blank=True, null=True)
    package=models.ForeignKey(
        PackageModel,
        on_delete=models.CASCADE,
        related_name='duration'
    )

# ti a package to an event or holiday ocassion
class PackageRelatedEvent(BaseModelWithStatus):
    event_name=models.CharField(max_length=100, blank=False, null=False)
    event_from=models.DateTimeField(blank=True, null=True)
    event_to=models.DateTimeField(blank=True, null=True)
    package=models.ManyToManyField(
        PackageModel,
        related_name='related_events'
    )


class PackageAnalytics(BaseModel):
    likes=models.IntegerField(default=0)
    dislikes=models.IntegerField(default=0)
    package=models.OneToOneField(
        PackageModel,
        on_delete=models.CASCADE,
        related_name='analytics'
    )