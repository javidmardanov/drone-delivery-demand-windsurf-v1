"""
Census data handling utilities for the Drone Delivery Demand Estimation project.
"""
import pandas as pd
import geopandas as gpd
import cenpy
import numpy as np
from shapely.geometry import Point, Polygon
import plotly.express as px
from typing import Dict, List, Tuple, Optional
import os

# Default variables we're interested in for demand estimation
DEFAULT_CENSUS_VARIABLES = {
    'B01003_001E': 'Total Population',
    'B19013_001E': 'Median Household Income',
    'B25001_001E': 'Total Housing Units',
    'B08014_001E': 'Workers 16 and over',
    'B25024_001E': 'Total Units in Structure'
}

# Hardcoded Census API key
CENSUS_API_KEY = "7ea7151ee08ce736334cae8a9bdd5b0f3f21b639"

def get_census_data(
    polygon: Polygon,
    variables: Dict[str, str] = DEFAULT_CENSUS_VARIABLES,
    year: int = 2019
) -> gpd.GeoDataFrame:
    """
    Fetch census data for the given area.
    
    Args:
        polygon: Area of interest
        variables: Dictionary of census variables to fetch
        year: Census year
        
    Returns:
        GeoDataFrame with census data
    """
    # Get the bounding box
    minx, miny, maxx, maxy = polygon.bounds
    
    # Set up the Census API connection
    conn = cenpy.remote.APIConnection('ACSDT5Y{}'.format(year))
    conn.api_key = CENSUS_API_KEY
    
    # Get census tracts for the area
    tracts_data = conn.query(
        cols=list(variables.keys()) + ['tract', 'state', 'county'],
        geo_unit='tract',
        geo_filter={
            'state': '*',
            'county': '*',
            'tract': '*'
        }
    )
    
    # Get the geometry for the tracts
    tracts_geo = conn.get_geos(
        geo_unit='tract',
        geo_filter={
            'state': '*',
            'county': '*',
            'tract': '*'
        }
    )
    
    # Merge data with geometry
    tracts_gdf = tracts_data.merge(
        tracts_geo[['GEOID', 'geometry']], 
        left_on='state_county_tract', 
        right_on='GEOID'
    )
    
    # Convert to GeoDataFrame
    tracts_gdf = gpd.GeoDataFrame(tracts_gdf, geometry='geometry')
    tracts_gdf = tracts_gdf.set_crs('EPSG:4326')
    
    # Clip to our polygon
    tracts_gdf = gpd.clip(tracts_gdf, polygon)
    
    # Rename columns to friendly names
    tracts_gdf = tracts_gdf.rename(columns=variables)
    
    # Convert numeric columns from string to float
    for var_name in variables.values():
        tracts_gdf[var_name] = pd.to_numeric(tracts_gdf[var_name], errors='coerce')
    
    return tracts_gdf

def get_census_stats(census_gdf: gpd.GeoDataFrame) -> Dict:
    """
    Calculate summary statistics for census data.
    """
    stats = {}
    numeric_columns = census_gdf.select_dtypes(include=[np.number]).columns
    
    for col in numeric_columns:
        if col not in ['LONGITUDE', 'LATITUDE']:
            stats[col] = {
                'mean': census_gdf[col].mean(),
                'median': census_gdf[col].median(),
                'std': census_gdf[col].std(),
                'min': census_gdf[col].min(),
                'max': census_gdf[col].max()
            }
    
    return stats

def allocate_population(
    buildings_gdf: gpd.GeoDataFrame,
    census_gdf: gpd.GeoDataFrame,
    population_col: str = 'Total Population'
) -> gpd.GeoDataFrame:
    """
    Allocate population from census tracts to buildings based on building area
    and classification.
    
    Args:
        buildings_gdf: GeoDataFrame with buildings
        census_gdf: GeoDataFrame with census data
        population_col: Name of population column
        
    Returns:
        buildings_gdf with allocated population
    """
    # Only consider residential buildings (DD class) for population allocation
    residential_mask = buildings_gdf['delivery_class'] == 'DD'
    buildings_gdf.loc[~residential_mask, 'estimated_population'] = 0
    
    # Spatial join to get census tract for each building
    buildings_with_census = gpd.sjoin(
        buildings_gdf[residential_mask],
        census_gdf[[population_col, 'geometry']],
        how='left',
        predicate='within'
    )
    
    # Calculate building areas
    buildings_with_census['area'] = buildings_with_census.geometry.area
    
    # Group by census tract and calculate area proportions
    tract_groups = buildings_with_census.groupby('index_right')
    
    for tract_idx, group in tract_groups:
        total_area = group['area'].sum()
        tract_population = census_gdf.loc[tract_idx, population_col]
        
        # Allocate population proportionally to building area
        population_per_building = (group['area'] / total_area) * tract_population
        
        # Update the original buildings_gdf
        buildings_gdf.loc[group.index, 'estimated_population'] = population_per_building
    
    # Fill any NaN values with 0
    buildings_gdf['estimated_population'] = buildings_gdf['estimated_population'].fillna(0)
    
    return buildings_gdf

def plot_census_choropleth(
    census_gdf: gpd.GeoDataFrame,
    variable: str,
    center: Tuple[float, float],
    zoom: int = 12
) -> px.choropleth_mapbox:
    """
    Create a choropleth map for a census variable.
    """
    fig = px.choropleth_mapbox(
        census_gdf,
        geojson=census_gdf.geometry.__geo_interface__,
        locations=census_gdf.index,
        color=variable,
        hover_data=[variable],
        title=f"Census Tracts - {variable}",
        mapbox_style="carto-positron",
        center={"lat": center[1], "lon": center[0]},
        zoom=zoom,
        width=800,
        height=600
    )
    
    return fig
