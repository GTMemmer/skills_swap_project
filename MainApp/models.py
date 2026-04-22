from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('tutoring', 'Tutoring'),
        ('writing', 'Writing / Editing'),
        ('design', 'Design / Media'),
        ('tech', 'Tech / Programming'),
        ('other', 'Other'),
    ]

    CONTACT_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('chat', 'Chat / DM'),
    ]

    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('scheduled', 'Scheduled'),
    ]

    title = models.CharField(max_length=120, db_index=True)
    description = models.TextField()
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, db_index=True)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text='Set the price or choose free.',
    )
    free = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Mark this skill as free if you do not want payment.',
    )
    contact_preference = models.CharField(max_length=16, choices=CONTACT_CHOICES)
    availability_status = models.CharField(max_length=16, choices=AVAILABILITY_CHOICES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills', db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.owner.username}"

    @property
    def display_price(self):
        if self.free:
            return 'Free'
        if self.price is None:
            return 'Price not set'
        return f'${self.price:.2f}'

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0
        total = sum(review.rating for review in reviews)
        return round(total / reviews.count(), 1)


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('skill', 'user')  # One review per user per skill

    def __str__(self):
        return f"Review for {self.skill.title} by {self.user.username}"
