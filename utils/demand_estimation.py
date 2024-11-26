import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import poisson

def calculate_demand_potential(building, params, components=None, current_hour=None):
    """
    Calculate demand potential for a building with configurable components
    
    Parameters:
    -----------
    building : dict
        Building attributes including population, income, height
    params : dict
        Parameters for each component (alpha, beta, epsilon)
    components : dict, optional
        Dictionary of boolean flags to enable/disable components
        {'population': True, 'income': True, 'height': True, 'time': True}
    current_hour : int, optional
        Current hour (0-23) for time-based calculations
    """
    if components is None:
        components = {
            'population': True,
            'income': True,
            'height': True,
            'time': True
        }
    
    D_j = 1.0
    
    if components['population']:
        population = building.get('population', 1)
        D_j *= (population ** params['alpha'])
    
    if components['income']:
        income = building.get('income', 50000)
        income_factor = logistic_income_factor(income)
        D_j *= (income_factor ** params['beta'])
    
    if components['height']:
        height = building.get('height', 10)
        D_j *= (height ** params['epsilon'])
    
    if components['time'] and current_hour is not None:
        time_factor = calculate_time_factor(current_hour)
        D_j *= time_factor
    
    return D_j

def logistic_income_factor(income, midpoint=50000, steepness=0.00005):
    """Calculate demand factor based on income using logistic function"""
    return 1 / (1 + np.exp(-steepness * (income - midpoint)))

def calculate_time_factor(hour, peak_hours=[(8, 10), (12, 14), (18, 20)]):
    """Calculate time-based demand factor"""
    for start, end in peak_hours:
        if start <= hour < end:
            return 1.5  # Peak hours have 50% more demand
    return 1.0

def simulate_deliveries(lambda_param, n_simulations=1000):
    """Simulate delivery counts using Poisson distribution"""
    return poisson.rvs(lambda_param, size=n_simulations)

def plot_poisson_distribution(lambda_param, actual_value=None, seed_value=None):
    """Create a Poisson distribution plot for a building"""
    x = np.arange(0, poisson.ppf(0.99, lambda_param))
    pmf = poisson.pmf(x, lambda_param)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=pmf, name='Probability'))
    
    if actual_value is not None:
        fig.add_vline(x=actual_value, line_dash="dash", 
                     line_color="red", annotation_text="Average")
    
    if seed_value is not None:
        fig.add_vline(x=seed_value, line_dash="dash", 
                     line_color="green", annotation_text="Current Simulation")
    
    fig.update_layout(
        title=f'Poisson Distribution (λ={lambda_param:.2f})',
        xaxis_title='Number of Deliveries',
        yaxis_title='Probability',
        showlegend=False
    )
    return fig

def calculate_hotspots(gdf, threshold_percentile=90):
    """Identify delivery hotspots"""
    threshold = np.percentile(gdf['demand_potential'], threshold_percentile)
    return gdf['demand_potential'] >= threshold

def get_summary_statistics(gdf):
    """Calculate key statistics for the area"""
    stats = {
        'total_buildings': len(gdf),
        'avg_demand': gdf['demand_potential'].mean(),
        'max_demand': gdf['demand_potential'].max(),
        'total_demand': gdf['demand_potential'].sum(),
        'hotspot_count': sum(gdf['is_hotspot']),
        'avg_height': gdf['height'].mean()
    }
    return stats

def estimate_building_heights(gdf, k_neighbors=5):
    """
    Estimate building heights using k-NN for buildings with missing heights.
    
    Parameters:
    -----------
    gdf : GeoDataFrame
        The input geodataframe containing building data
    k_neighbors : int, default=5
        Number of neighbors to use for height estimation
    """
    # Convert height and building:levels to numeric, handling errors
    gdf['height'] = pd.to_numeric(gdf['height'], errors='coerce')
    gdf['building:levels'] = pd.to_numeric(gdf['building:levels'], errors='coerce')
    
    # Initialize height source column
    gdf['height_source'] = None
    
    # First pass: use building levels if height is missing
    mask_no_height = gdf['height'].isna()
    levels_mask = mask_no_height & gdf['building:levels'].notna()
    gdf.loc[levels_mask, 'height'] = \
        gdf.loc[levels_mask, 'building:levels'] * 3.0
    
    # Set height sources
    gdf.loc[~mask_no_height, 'height_source'] = 'height'
    gdf.loc[levels_mask, 'height_source'] = 'building:levels'
    
    # Second pass: use k-NN for remaining missing heights
    mask_still_missing = gdf['height'].isna()
    if mask_still_missing.any():
        # Get buildings with known heights
        known_heights = gdf[~mask_still_missing].copy()
        missing_heights = gdf[mask_still_missing].copy()
        
        if len(known_heights) >= k_neighbors:
            # Project to a local UTM zone for accurate distance calculations
            utm_zone = int((known_heights.geometry.centroid.x.mean() + 180) / 6) + 1
            utm_crs = f'EPSG:326{utm_zone}' if known_heights.geometry.centroid.y.mean() >= 0 else f'EPSG:327{utm_zone}'
            
            known_heights_proj = known_heights.to_crs(utm_crs)
            missing_heights_proj = missing_heights.to_crs(utm_crs)
            
            # Calculate distances between all pairs of buildings
            from sklearn.neighbors import NearestNeighbors
            nbrs = NearestNeighbors(n_neighbors=min(k_neighbors, len(known_heights)), metric='euclidean')
            
            # Fit on known heights using centroids
            known_coords = np.column_stack((
                known_heights_proj.geometry.centroid.x,
                known_heights_proj.geometry.centroid.y
            ))
            nbrs.fit(known_coords)
            
            # Find nearest neighbors for missing heights
            missing_coords = np.column_stack((
                missing_heights_proj.geometry.centroid.x,
                missing_heights_proj.geometry.centroid.y
            ))
            distances, indices = nbrs.kneighbors(missing_coords)
            
            # Store neighbor information for visualization
            neighbor_info = []
            for idx, neighbor_indices in enumerate(indices):
                neighbors = known_heights.iloc[neighbor_indices]
                neighbor_info.append({
                    'neighbor_indices': neighbor_indices,
                    'neighbor_heights': neighbors['height'].tolist(),
                    'neighbor_coords': [
                        (n.centroid.y, n.centroid.x) 
                        for n in neighbors.geometry
                    ]
                })
            
            # Calculate average height of neighbors for each missing building
            estimated_heights = np.array([
                known_heights.iloc[idx]['height'].mean()
                for idx in indices
            ])
            
            # Update the original dataframe
            gdf.loc[mask_still_missing, 'height'] = estimated_heights
            
            # Store neighbor information
            gdf['neighbor_info'] = None
            gdf.loc[mask_still_missing, 'neighbor_info'] = neighbor_info
            
            # Set height sources
            gdf.loc[mask_still_missing, 'height_source'] = 'k-NN'
        else:
            # If not enough known heights, use default
            gdf.loc[mask_still_missing, 'height'] = 10.0
            
            # Set height sources
            gdf.loc[mask_still_missing, 'height_source'] = 'default'
    
    # Add a flag for estimated heights
    gdf['height_estimated'] = mask_no_height
    
    return gdf

def plot_building_heights(gdf):
    """Create a plotly figure showing building heights with neighbor connections"""
    fig = go.Figure()
    
    # Reset index to handle MultiIndex
    gdf = gdf.reset_index(drop=True)
    
    # Common color scale for both known and estimated heights
    colorscale = 'Viridis'
    
    # Plot buildings with known heights (green outline)
    known = gdf[~gdf['height_estimated']]
    if len(known) > 0:
        fig.add_trace(go.Choroplethmapbox(
            geojson=known.geometry.__geo_interface__,
            locations=known.index,
            z=known['height'],
            colorscale=colorscale,
            marker=dict(
                opacity=0.8,
                line_width=2,
                line_color='green'
            ),
            name='Known Heights',
            showscale=True,
            colorbar_title='Height (m)',
            hovertemplate=(
                'Height: %{z:.1f}m<br>' +
                'Type: %{customdata[0]}<br>' +
                'Source: %{customdata[1]}<extra></extra>'
            ),
            customdata=known[['building', 'height_source']]
        ))
    
    # Plot buildings with estimated heights (orange outline)
    estimated = gdf[gdf['height_estimated']]
    if len(estimated) > 0:
        fig.add_trace(go.Choroplethmapbox(
            geojson=estimated.geometry.__geo_interface__,
            locations=estimated.index,
            z=estimated['height'],
            colorscale=colorscale,
            marker=dict(
                opacity=0.8,
                line_width=2,
                line_color='orange'
            ),
            name='Estimated Heights',
            showscale=False,
            hovertemplate=(
                'Height: %{z:.1f}m (Estimated)<br>' +
                'Type: %{customdata[0]}<br>' +
                'Based on %{customdata[1]} nearest buildings<br>' +
                'Neighbor heights: %{customdata[2]}<extra></extra>'
            ),
            customdata=estimated.apply(
                lambda x: [
                    x['building'],
                    len(x['neighbor_info']['neighbor_heights']) if isinstance(x['neighbor_info'], dict) else 0,
                    ', '.join([f'{h:.1f}m' for h in x['neighbor_info']['neighbor_heights']]) if isinstance(x['neighbor_info'], dict) else 'N/A'
                ],
                axis=1
            ).tolist()
        ))
        
        # Add lines to nearest neighbors for estimated buildings
        for idx, row in estimated.iterrows():
            if isinstance(row['neighbor_info'], dict):
                start_point = (row.geometry.centroid.y, row.geometry.centroid.x)
                for neighbor_coord in row['neighbor_info']['neighbor_coords']:
                    fig.add_trace(go.Scattermapbox(
                        lon=[start_point[1], neighbor_coord[1]],
                        lat=[start_point[0], neighbor_coord[0]],
                        mode='lines',
                        line=dict(width=1, color='orange'),
                        opacity=0.3,
                        showlegend=False,
                        hoverinfo='skip'
                    ))
    
    # Update layout
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox=dict(
            center=dict(
                lat=gdf.geometry.centroid.y.mean(),
                lon=gdf.geometry.centroid.x.mean()
            ),
            zoom=14
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        height=400,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        )
    )
    
    return fig
