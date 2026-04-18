
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from locations.models import City
from users.models import Provider


class Attribute(models.Model):
    """Model to store chemical attributes of wines."""
    
    total_sulfur_dioxide = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        help_text='Total sulfur dioxide (0-300 mg/L)'
    )
    fixed_acidity = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[MinValueValidator(5.0), MaxValueValidator(20.0)],
        help_text='Fixed acidity (5.0-20.0 g/L)'
    )
    volatile_acidity = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[MinValueValidator(0.1), MaxValueValidator(2.0)],
        help_text='Volatile acidity (0.1-2.0 g/L)'
    )
    free_sulfur_dioxide = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(80)],
        help_text='Free sulfur dioxide (1-80 mg/L)'
    )
    citric_acid = models.DecimalField(
        max_digits=4, 
        decimal_places=3,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        help_text='Citric acid (0.0-10.0 g/L)'
    )
    residual_sugar = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0.5), MaxValueValidator(15.0)],
        help_text='Residual sugar (0.5-15.0 g/L)'
    )
    chlorides = models.DecimalField(
        max_digits=5, 
        decimal_places=4,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text='Chlorides (0.0-1.0 g/L)'
    )
    density = models.DecimalField(
        max_digits=7, 
        decimal_places=5,
        validators=[MinValueValidator(0.9900), MaxValueValidator(1.0100)],
        help_text='Density (0.9900-1.0100 g/cm³)'
    )
    pH = models.DecimalField(
        max_digits=3, 
        decimal_places=2,
        validators=[MinValueValidator(2.0), MaxValueValidator(5.0)],
        help_text='pH (2.0-5.0)'
    )
    sulphates = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0)],
        help_text='Sulphates(0.0-2.0 g/L)'
    )
    alcohol = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[MinValueValidator(5.0), MaxValueValidator(20.0)],
        help_text='Alcohol (5.0-20.0 %vol)'
    )
    
    class Meta:
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'
    
    def __str__(self):
        return f"Attributes (pH: {self.pH}, Alcohol: {self.alcohol}%)"


class Wine(models.Model):
    """
    Model to store wine information.
    """
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100,
        db_index=True,  # Index for faster search by name
        help_text='Wine name'
    )
    description = models.TextField(
        blank=True,
        help_text='Description of the wine'
    )
    harvest_year = models.IntegerField(
        validators=[
            MinValueValidator(1900, message='The year must be after 1900'),
            MaxValueValidator(
                datetime.now().year,
                message='The year cannot be in the future'
            )
        ],
        db_index=True,  
        help_text='Harvest year of the wine'
    )
    maker = models.CharField(
        max_length=100,
        help_text='Wine maker or producer'
    )
    variety = models.CharField(
        max_length=100,
        db_index=True, 
        help_text='Variety of the wine'
    )
    
    
    attribute = models.OneToOneField(
        Attribute,
        on_delete=models.CASCADE,
        related_name='wine',
        help_text='Attributes of the wine'
    )
    
    
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='wines',
        help_text='City where the wine is produced'
    )

    added_date = models.DateField(
    auto_now_add=True,
    help_text='Date the wine was added'
)

    class Meta:
        verbose_name = 'Wine'
        verbose_name_plural = 'Wines'
        ordering = ['-harvest_year', 'name']  
        indexes = [
            models.Index(fields=['harvest_year', 'variety']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.harvest_year})"
    
    def get_age(self):
        """Calculate the age of the wine based on the harvest year."""
        return datetime.now().year - self.harvest_year
