from django import forms
from .models import EnergyConsumption



# Dictionary of energy prices for different states
ENERGY_PRICES = {
    'Maharashtra': 9.85,
    'Andhra Pradesh': 8.15,
    'West Bengal': 8.00,
    'Kerala': 8.00,
    'Karnataka': 6.95,
    'Delhi': 6.80,
    'Tamil Nadu': 6.40,
    'Andaman & Nicobar': 6.20,
    'Odisha': 6.15,
    'Rajasthan': 6.05,
    'Madhya Pradesh': 6.05,
    'Punjab': 5.90,
    'Tripura': 5.85,
    'Haryana': 5.45,
    'Lakshadweep': 5.00,
    'Uttar Pradesh': 4.80,
    'Bihar': 4.60,
    'Meghalaya': 4.30,
    'Himachal Pradesh': 4.05,
    'Jammu & Kashmir': 4.00,
    'Goa': 3.90,
    'Uttarakhand': 3.70,
    'Puducherry': 3.35,
    'Chattisgarh': 3.35,
    'Daman & Diu': 3.00,
    'Dadra & Nagar Haveli': 2.75
}

DEFAULT_ENERGY_PRICE = 5.50  # Default price for unlisted states

class EnergyConsumptionForm(forms.ModelForm):
    # Create a list of choices for states (for the dropdown)
    STATE_CHOICES = [('', 'Select a location')] + [(state, state) for state in ENERGY_PRICES.keys()]
    STATE_CHOICES.append(('Other', 'Other'))  # Option for unlisted states

    # Convert the location field to a ChoiceField with predefined options
    location = forms.ChoiceField(choices=STATE_CHOICES, label="State")

    # Set initial value for energy_price to None
    energy_price = forms.DecimalField(
        min_value=0, 
        max_digits=6, 
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Price per kWh'})
    )

    class Meta:
        model = EnergyConsumption
        fields = ['household_name', 'monthly_energy_usage', 'location', 'energy_price', 'renewable_efficiency', 'sunlight_hours']
        widgets = {
            'household_name': forms.TextInput(attrs={'placeholder': 'Enter household name'}),
            'monthly_energy_usage': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'placeholder': 'kWh'}),
            'energy_price': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'placeholder': 'Price per kWh'}),
            'renewable_efficiency': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.1, 'placeholder': '% Efficiency'}),
            'sunlight_hours': forms.NumberInput(attrs={'min': 1, 'max': 24, 'step': 0.1, 'placeholder': 'Hours of sunlight per day'}),
        }

        labels = {
            'household_name': 'Household Name',
            'monthly_energy_usage': 'Monthly Energy Usage (kWh)',
            'location': 'State',
            'energy_price': 'Energy Price (per kWh)',
            'renewable_efficiency': 'Renewable Efficiency (%)',
            'sunlight_hours': 'Average Sunlight Hours per Day',
        }

    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get('location')

        # Auto-fill the energy price based on the location (state)
        if location in ENERGY_PRICES:
            cleaned_data['energy_price'] = ENERGY_PRICES[location]
        else:
            cleaned_data['energy_price'] = DEFAULT_ENERGY_PRICE  # Default price if state is not listed

        return cleaned_data






