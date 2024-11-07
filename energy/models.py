from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class EnergyConsumption(models.Model):
    household_name = models.CharField(max_length=100)
    monthly_energy_usage = models.FloatField()  # in kWh
    location = models.CharField(max_length=100)
    
    # New fields for calculation
    energy_price = models.FloatField(default=0.12)  # Local price per kWh (default to $0.12)
    renewable_efficiency = models.FloatField(default=20)  # Efficiency of renewable source (e.g., 80%)
    
    # New field: Sunlight hours per day
    sunlight_hours = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(24)], 
        default=5.0,  # Default value can be modified
        help_text="Average hours of sunlight per day"
    )

    def __str__(self):
        return self.household_name
