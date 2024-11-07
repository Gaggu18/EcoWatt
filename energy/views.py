import requests
from django.shortcuts import render, redirect
from .forms import EnergyConsumptionForm
from django.http import JsonResponse
from .models import EnergyConsumption
from django.views.decorators.csrf import csrf_exempt
import uuid


# Keeping the ENERGY_PRICES constant and DEFAULT_ENERGY_PRICE as it is
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

# 1. Existing energy calculator view
def energy_calculator(request):
    form = EnergyConsumptionForm()
    
    if request.method == 'POST':
        form = EnergyConsumptionForm(request.POST)
        if form.is_valid():
            energy_data = form.save(commit=False)
            
            # Extract form data
            state = energy_data.location  # Assuming 'location' is the field for state
            monthly_energy = energy_data.monthly_energy_usage
            renewable_efficiency = energy_data.renewable_efficiency / 100  # Convert percentage to decimal
            sunlight_hours = energy_data.sunlight_hours

            # Get energy price based on location
            energy_price = ENERGY_PRICES.get(state, DEFAULT_ENERGY_PRICE)
            
            # Solar panel system power calculation (in kW)
            system_power = monthly_energy / (30 * sunlight_hours)

            # Required surface area based on 200W/m² efficiency
            panel_efficiency = 0.2  # 200W/m²
            surface_area = system_power / panel_efficiency

            # Estimated installation cost (e.g., $2500/kW)
            installation_cost_per_kw = 2500
            total_installation_cost = system_power * installation_cost_per_kw

            # Adjusted energy production calculation using renewable efficiency
            yearly_energy_production = system_power * sunlight_hours * 365 * renewable_efficiency

            # Calculate yearly savings
            yearly_savings = yearly_energy_production * energy_price

            # CO2 emission reduction (0.92 kg CO2 per kWh)
            carbon_saved = yearly_energy_production * 0.92

            # Fetch nearby solar system providers based on state
            providers = fetch_nearby_solar_providers(state)

            return render(request, 'energy/result.html', {
                'form': form,
                'system_power': system_power,
                'surface_area': surface_area,
                'total_installation_cost': total_installation_cost,
                'yearly_savings': yearly_savings,
                'carbon_saved': carbon_saved,
                'providers': providers,  # Pass the providers to the template
            })

    return render(request, 'energy/calculator.html', {'form': form})



# 3. Existing fetch provider function
def fetch_nearby_solar_providers(state):
    # Replace with your RapidAPI key and endpoint
    url = "https://google-map-places.p.rapidapi.com/maps/api/place/textsearch/json"
    querystring = {"query": f"solar system providers in {state}", "language": "en"}
    headers = {
        "x-rapidapi-key": "a4e640e5aemsh32e9befa10340e0p183ebajsn3276fcfeecf1",
        "x-rapidapi-host": "google-map-places.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    results = response.json().get('results', [])
    
    # Extract relevant details for each provider
    providers = [
        {
            'name': result.get('name'),
            'address': result.get('formatted_address'),
            'rating': result.get('rating', 'N/A'),
            'place_id': result.get('place_id')
        }
        for result in results
    ]
    
    return providers

# Existing views unchanged
def renewable_map(request):
    return render(request, 'energy/map.html')

def renewable_news(request):
    api_key = 'b030cf031dd4410ba0575fc2fd11f7c3'
    url = ('https://newsapi.org/v2/everything?'
           'q=renewable energy&'
           'sortBy=publishedAt&'
           'apiKey=' + api_key)
    
    response = requests.get(url)
    news_data = response.json()

    context = {
        'articles': news_data.get('articles', [])
    }
    
    return render(request, 'energy/news.html', context)

def wind_map(request):
    lat = 37.7749  
    lon = -122.4194 
    api_key = 'ffd15dc166a2a58dee0b73e39a730c65'

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

    response = requests.get(url)
    data = response.json()

    wind_speed = (data['wind']['speed']) * 3.6  # Convert from m/s to km/h

    context = {
        'lat': lat,
        'lon': lon,
        'wind_speed': wind_speed
    }

    return render(request, 'energy/windmap.html', context)

def home_page(request):
    return render(request, 'energy/home.html')

def why_renewable(request):
    return render(request, 'energy/why_renewable.html')

def get_started(request):
    return render(request, 'energy/get_started.html')

def privacy_policy(request):
    return render(request, 'energy/privacy_policy.html')

def terms_and_conditions(request):
    return render(request, 'energy/terms_and_conditions.html')

# Existing chat view for API-based chat functionality
external_user_id = str(uuid.uuid4())

API_KEY = 'SBIzzYQvtbMBGRiD15EBdw0BdONCibbF'

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')

        if not session_id:
            create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
            create_session_headers = {'apikey': API_KEY}
            create_session_body = {"pluginIds": [], "externalUserId": external_user_id}

            session_response = requests.post(create_session_url, headers=create_session_headers, json=create_session_body)
            session_response.raise_for_status()
            session_data = session_response.json()
            session_id = session_data['data']['id']

        user_query = request.POST.get('query')

        submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
        submit_query_headers = {'apikey': API_KEY}
        submit_query_body = {
            "endpointId": "predefined-openai-gpt4o",
            "query": user_query,
            "pluginIds": ["plugin-1712327325", "plugin-1713962163", "plugin-1726225108"],
            "responseMode": "sync"
        }

        query_response = requests.post(submit_query_url, headers=submit_query_headers, json=submit_query_body)
        query_response.raise_for_status()
        query_response_data = query_response.json()

        response_data = {
            'data': {
                'sessionId': session_id,
                'answer': query_response_data.get('data', {}).get('answer', 'No answer found'),
                'status': query_response_data.get('data', {}).get('status', 'unknown')
            }
        }
        return JsonResponse(response_data)

    return render(request, 'energy/chat.html')

