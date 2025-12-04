"""
Utility functions for calculating transportation impacts and adjusting GWP based on travel distance.
Based on the transportation impact formulas documented in README.md
"""
import yaml
import os

# Transportation emission factor (kgCO2e per ton-km for diesel truck)
TRANSPORT_EMISSION_FACTOR = 0.062  # kgCO2e/ton-km

def calculate_transportation_impact(distance_km, mass_kg, emission_factor=TRANSPORT_EMISSION_FACTOR):
    """
    Calculate transportation impact for A4 stage (factory to construction site).
    
    Formula: Transportation Impact (kgCO2e) = Distance (km) × Load (kg) × Emission Factor (kgCO2e/ton-km) ÷ 1000
    
    Args:
        distance_km: Distance from manufacturing to construction site in kilometers
        mass_kg: Mass of the product in kilograms (from mass_per_declared_unit)
        emission_factor: Emission factor in kgCO2e/ton-km (default: 0.062 for diesel truck)
    
    Returns:
        Transportation impact in kgCO2e
    """
    return (distance_km * mass_kg * emission_factor) / 1000

def get_default_transportation_impact(epd):
    """
    Get the default transportation impact based on category defaults.
    
    Args:
        epd: EPD dictionary loaded from YAML
    
    Returns:
        Default transportation impact in kgCO2e, or None if data not available
    """
    category = epd.get('category', {})
    default_distance = category.get('default_distance')
    
    if default_distance is None:
        return None
    
    # Try to get mass from product level first, then category level
    mass = epd.get('mass_per_declared_unit')
    if mass is None:
        mass = category.get('mass_per_declared_unit')
    
    if mass is None:
        return None
    
    # Extract numeric value if it's a string like "1000 kg"
    if isinstance(mass, str):
        try:
            mass = float(mass.split()[0])
        except (ValueError, IndexError):
            return None
    
    # Extract numeric value from default_distance if it's a string like "51.49888 km"
    if isinstance(default_distance, str):
        try:
            default_distance = float(default_distance.split()[0])
        except (ValueError, IndexError):
            return None
    
    return calculate_transportation_impact(default_distance, mass)

def calculate_adjusted_gwp(epd, actual_distance_km, emission_factor=TRANSPORT_EMISSION_FACTOR):
    """
    Calculate adjusted GWP based on actual transportation distance.
    
    Adjusted GWP = gwp + (Actual Transportation Impact - Default Transportation Impact)
    
    Args:
        epd: EPD dictionary loaded from YAML
        actual_distance_km: Actual distance from manufacturing to construction site in kilometers
        emission_factor: Emission factor in kgCO2e/ton-km (default: 0.062 for diesel truck)
    
    Returns:
        Dictionary with:
        - adjusted_gwp: Adjusted GWP value in kgCO2e
        - base_gwp: Original GWP value
        - default_transport_impact: Default transportation impact
        - actual_transport_impact: Actual transportation impact
        - transport_adjustment: Difference (actual - default)
        - savings: Positive if actual < default (negative value means increase)
    """
    base_gwp = epd.get('gwp')
    if base_gwp is None:
        return None
    
    # Extract numeric value from gwp if it's a string like "53.38 kgCO2e"
    if isinstance(base_gwp, str):
        try:
            base_gwp = float(base_gwp.split()[0])
        except (ValueError, IndexError):
            return None
    
    # Get mass
    mass = epd.get('mass_per_declared_unit')
    category = epd.get('category', {})
    if mass is None:
        mass = category.get('mass_per_declared_unit')
    
    if mass is None:
        return None
    
    # Extract numeric value if it's a string
    if isinstance(mass, str):
        try:
            mass = float(mass.split()[0])
        except (ValueError, IndexError):
            return None
    
    # Calculate actual transportation impact
    actual_transport_impact = calculate_transportation_impact(actual_distance_km, mass, emission_factor)
    
    # Get default transportation impact
    default_transport_impact = get_default_transportation_impact(epd)
    if default_transport_impact is None:
        # If no default, just add actual transport impact
        default_transport_impact = 0
    
    # Calculate adjustment
    transport_adjustment = actual_transport_impact - default_transport_impact
    adjusted_gwp = base_gwp + transport_adjustment
    
    return {
        'adjusted_gwp': adjusted_gwp,
        'base_gwp': base_gwp,
        'default_transport_impact': default_transport_impact,
        'actual_transport_impact': actual_transport_impact,
        'transport_adjustment': transport_adjustment,
        'savings': -transport_adjustment,  # Positive if we're saving (reducing impact)
        'percent_change': (transport_adjustment / base_gwp * 100) if base_gwp > 0 else 0
    }

def example_calculation():
    """Example calculation as shown in README.md"""
    # Example from README:
    # Product gwp: 468 kgCO2e (for 1000 sf)
    # mass_per_declared_unit: 357.43 kg
    # category.default_distance: 1647.968 km
    # Actual distance: 500 km
    
    example_epd = {
        'gwp': '468 kgCO2e',
        'mass_per_declared_unit': '357.43 kg',
        'category': {
            'default_distance': '1647.968 km',
            'default_transport_mode': 'truck, unspecified'
        }
    }
    
    result = calculate_adjusted_gwp(example_epd, 500)
    
    print("Example Calculation:")
    print(f"Base GWP: {result['base_gwp']} kgCO2e")
    print(f"Default transport impact: {result['default_transport_impact']:.1f} kgCO2e")
    print(f"Actual transport impact (500 km): {result['actual_transport_impact']:.1f} kgCO2e")
    print(f"Adjusted GWP: {result['adjusted_gwp']:.1f} kgCO2e")
    print(f"Savings: {result['savings']:.1f} kgCO2e ({result['percent_change']:.1f}% reduction)")
    
    return result

if __name__ == "__main__":
    example_calculation()

