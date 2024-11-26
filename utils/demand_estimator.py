import numpy as np
from scipy.spatial.distance import cdist

class DemandEstimator:
    def __init__(self):
        self.buildings_gdf = None
        self.parameters = None
        
    def set_parameters(self, parameters):
        """
        Set model parameters
        """
        self.parameters = parameters
    
    def calculate_proximity_factor(self, buildings_gdf):
        """
        Calculate proximity factor (PF_j) for each building
        PF_j = 1 / (d_store,j + ε)^η
        """
        # Get coordinates of all buildings
        coords = np.array([(p.x, p.y) for p in buildings_gdf.geometry.centroid])
        
        # Get coordinates of delivery origin points (stores, restaurants, etc.)
        do_buildings = buildings_gdf[buildings_gdf['classification'] == 'DO']
        do_coords = np.array([(p.x, p.y) for p in do_buildings.geometry.centroid])
        
        if len(do_coords) > 0:
            # Calculate distances to nearest delivery origin
            distances = cdist(coords, do_coords).min(axis=1)
            
            # Calculate proximity factor
            epsilon = 1e-6  # Small constant to avoid division by zero
            eta = self.parameters.get('eta', 1.0)
            proximity_factor = 1 / (distances + epsilon) ** eta
        else:
            proximity_factor = np.ones(len(buildings_gdf))
        
        return proximity_factor
    
    def calculate_demand_potential(self, buildings_gdf):
        """
        Calculate demand potential score (D_j) for each building
        D_j = (P_adj,j/P_max)^α × (I_j/I_max)^β × B_j^ε × PF_j^ζ
        """
        # Get parameters
        alpha = self.parameters.get('alpha', 1.0)
        beta = self.parameters.get('beta', 1.0)
        epsilon = self.parameters.get('epsilon', 1.0)
        zeta = self.parameters.get('zeta', 1.0)
        
        # Normalize population and income
        P_max = buildings_gdf['adjusted_population'].max()
        I_max = buildings_gdf['income'].max()
        
        # Calculate components
        pop_component = (buildings_gdf['adjusted_population'] / P_max) ** alpha
        income_component = (buildings_gdf['income'] / I_max) ** beta
        building_component = buildings_gdf['estimated_height'] ** epsilon
        proximity_component = self.calculate_proximity_factor(buildings_gdf) ** zeta
        
        # Calculate demand potential
        demand_potential = pop_component * income_component * building_component * proximity_component
        
        return demand_potential
    
    def calculate_temporal_weight(self, hour, day, month):
        """
        Calculate temporal weight T(t) = f_hour(h) × f_day(d) × f_month(m)
        """
        # Hour component (assuming normal distribution around peak hours)
        mu_h = 14  # Peak hour (2 PM)
        sigma_h = 4
        hour_weight = np.exp(-((hour - mu_h) ** 2) / (2 * sigma_h ** 2))
        
        # Day component (weekday vs weekend)
        day_weight = 1.2 if day < 5 else 0.8  # Higher weight for weekdays
        
        # Month component (seasonal variation)
        month_weight = 1 + 0.2 * np.sin(2 * np.pi * (month - 1) / 12)  # Seasonal variation
        
        return hour_weight * day_weight * month_weight
    
    def estimate_demand(self, buildings_gdf, hour=14, day=2, month=6):
        """
        Calculate expected deliveries λ_j(t) = D_j × T(t) × λ_0
        """
        # Set buildings data
        self.buildings_gdf = buildings_gdf
        
        # Calculate demand potential
        demand_potential = self.calculate_demand_potential(buildings_gdf)
        
        # Calculate temporal weight
        temporal_weight = self.calculate_temporal_weight(hour, day, month)
        
        # Calculate expected deliveries
        lambda_0 = self.parameters.get('lambda_0', 10.0)
        expected_deliveries = demand_potential * temporal_weight * lambda_0
        
        return expected_deliveries
