import streamlit as st
import osmnx as ox
import geopandas as gpd
import numpy as np
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium, folium_static
import json
import plotly.express as px
import plotly.graph_objects as go
from utils.demand_estimation import (
    calculate_demand_potential, simulate_deliveries,
    plot_poisson_distribution, calculate_hotspots,
    get_summary_statistics, estimate_building_heights,
    plot_building_heights
)
from utils.building_classifier import (
    classify_buildings,
    get_classification_stats,
    load_classification_rules,
    save_classification_rules,
    DEFAULT_RULES
)
from utils.census_data import (
    get_census_data,
    get_census_stats,
    allocate_population,
    plot_census_choropleth,
    DEFAULT_CENSUS_VARIABLES
)
import os
from dotenv import load_dotenv
from shapely.geometry import Polygon, box

# Load environment variables from .env file
load_dotenv()

# Initialize session state
if 'area_polygon' not in st.session_state:
    st.session_state.area_polygon = None
if 'buildings_gdf' not in st.session_state:
    st.session_state.buildings_gdf = None
if 'selected_building' not in st.session_state:
    st.session_state.selected_building = None
if 'simulation_seed' not in st.session_state:
    st.session_state.simulation_seed = 42
if 'classification_rules' not in st.session_state:
    st.session_state.classification_rules = DEFAULT_RULES.copy()
if 'census_data' not in st.session_state:
    st.session_state.census_data = None

st.set_page_config(page_title="Drone Delivery Demand Estimation", layout="wide")

def geocode_location(location_name):
    """Geocode a location name to get coordinates"""
    try:
        location = ox.geocode(location_name)
        return location
    except:
        return None

def create_map(location=None):
    """Create a folium map with drawing tools"""
    # Use provided location or default to Downtown Austin, Texas
    if location is None:
        location = [30.2672, -97.7431]  # Downtown Austin coordinates
    
    # Create a map centered on the location
    m = folium.Map(
        location=location,
        zoom_start=12,
        control_scale=True
    )
    
    # Add drawing tools
    draw = plugins.Draw(
        export=False,
        position='topleft',
        draw_options={
            'polyline': False,
            'circle': False,
            'polygon': True,
            'marker': False,
            'circlemarker': False,
            'rectangle': True
        }
    )
    draw.add_to(m)
    
    return m

def main():
    st.title("Drone Delivery Demand Estimation")
    
    # Add location search
    st.sidebar.subheader("Location Search")
    location_name = st.sidebar.text_input("Enter location (e.g., 'Downtown Austin, TX'):")
    
    # Add demand component controls
    st.sidebar.subheader("Demand Components")
    
    # Display demand estimation formula
    st.sidebar.markdown("### Demand Estimation Formula")
    formula = r"""
    $D_{ij} = \begin{cases}
    1 & \text{if all components disabled} \\
    \prod_{k} C_k & \text{otherwise}
    \end{cases}$
    
    where components $C_k$ are:
    """
    st.sidebar.markdown(formula)
    
    component_formulas = []
    
    if 'demand_components' not in st.session_state:
        st.session_state.demand_components = {
            'population': True,
            'income': True,
            'height': True,
            'time': True
        }
    
    # Population component
    st.session_state.demand_components['population'] = st.sidebar.checkbox("Population Factor", value=st.session_state.demand_components['population'])
    if st.session_state.demand_components['population']:
        component_formulas.append(r"$C_{pop} = P^{\alpha}$ (Population)")
    
    # Income component with logistic function
    st.session_state.demand_components['income'] = st.sidebar.checkbox("Income Factor (Logistic)", value=st.session_state.demand_components['income'])
    if st.session_state.demand_components['income']:
        component_formulas.append(r"$C_{inc} = \left(\frac{1}{1 + e^{-\beta(I-I_0)}}\right)$ (Income)")
    
    # Height component
    st.session_state.demand_components['height'] = st.sidebar.checkbox("Building Height Factor", value=st.session_state.demand_components['height'])
    if st.session_state.demand_components['height']:
        component_formulas.append(r"$C_{h} = H^{\epsilon}$ (Height)")
    
    # Time component
    st.session_state.demand_components['time'] = st.sidebar.checkbox("Time-based Factor", value=st.session_state.demand_components['time'])
    if st.session_state.demand_components['time']:
        component_formulas.append(r"$C_t = \begin{cases} 1.5 & \text{peak hours} \\ 1.0 & \text{otherwise} \end{cases}$ (Time)")
    
    if component_formulas:
        st.sidebar.markdown("Selected components:")
        for formula in component_formulas:
            st.sidebar.markdown(formula)
    
    # Add time simulation controls if time component is enabled
    if 'current_hour' not in st.session_state:
        st.session_state.current_hour = 12
        
    if st.session_state.demand_components['time']:
        st.session_state.current_hour = st.sidebar.slider("Simulation Hour", 0, 23, st.session_state.current_hour)
        st.sidebar.markdown("🕒 Peak hours: 8-10, 12-14, 18-20")
    
    # Parameters for demand calculation
    if 'demand_params' not in st.session_state:
        st.session_state.demand_params = {
            'alpha': 1.0,
            'beta': 1.0,
            'epsilon': 0.5
        }
    
    st.sidebar.subheader("Demand Parameters")
    st.session_state.demand_params.update({
        'alpha': st.sidebar.slider("Population Impact (α)", 0.0, 2.0, st.session_state.demand_params['alpha'], 0.1),
        'beta': st.sidebar.slider("Income Impact (β)", 0.0, 2.0, st.session_state.demand_params['beta'], 0.1),
        'epsilon': st.sidebar.slider("Height Impact (ε)", 0.0, 2.0, st.session_state.demand_params['epsilon'], 0.1)
    })
    
    if location_name:
        with st.spinner(f"Finding location: {location_name}"):
            coords = geocode_location(location_name)
            if coords:
                st.success(f"Found location: {location_name}")
                m = create_map(location=coords)
            else:
                st.error(f"Could not find location: {location_name}")
                m = create_map()
    else:
        m = create_map()
    
    # Sidebar for parameters and equations
    with st.sidebar:
        st.header("Model Parameters")
        
        # Demand estimation parameters
        st.subheader("Demand Estimation")
        alpha = st.slider("α (Distance Decay)", 0.1, 2.0, 1.0, 0.1,
                         help="Controls how quickly demand decreases with distance")
        beta = st.slider("β (Population Scaling)", 0.1, 2.0, 1.0, 0.1,
                         help="Controls how demand scales with population")
        
        # Building height estimation
        st.subheader("Building Height Estimation")
        k_neighbors = st.slider("Number of neighbors (k)", 3, 10, 5,
                              help="Number of neighbors for height estimation")
        
        # Display main equations
        st.header("Model Equations")
        
        # Demand estimation equation
        st.subheader("Demand Estimation")
        st.latex(r"""
        D_{ij} = \frac{P_i^\beta}{d_{ij}^\alpha}
        """)
        st.markdown("""
        Where:
        - D_{ij}: Demand between points i and j
        - P_i: Population at point i
        - d_{ij}: Distance between i and j
        - α: Distance decay parameter
        - β: Population scaling parameter
        """)
        
        # Distribution selection
        st.subheader("Delivery Distribution")
        distribution = st.selectbox(
            "Choose Distribution",
            ["Poisson", "Normal", "Negative Binomial"],
            help="Statistical distribution for simulating deliveries"
        )
        
        if distribution == "Poisson":
            st.latex(r"""
            P(X = k) = \frac{e^{-\lambda}\lambda^k}{k!}
            """)
        elif distribution == "Normal":
            st.latex(r"""
            f(x) = \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}
            """)
        else:  # Negative Binomial
            st.latex(r"""
            P(X = k) = \binom{k+r-1}{k}p^r(1-p)^k
            """)

    # Main content area with tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Area Selection", 
        "Building Overview", 
        "Building Classification",
        "Census Data Overview",
        "Population Allocation",
        "Building Heights",
        "Demand Estimation"
    ])
    
    with tab1:
        st.subheader("Select Area")
        output = st_folium(m, width=800, height=600)
        
        if output["last_active_drawing"]:
            coords = output["last_active_drawing"]["geometry"]["coordinates"][0]
            bounds = box(*[
                min(c[0] for c in coords),
                min(c[1] for c in coords),
                max(c[0] for c in coords),
                max(c[1] for c in coords)
            ])
            st.session_state.area_polygon = bounds
            
            try:
                with st.spinner("Fetching building data..."):
                    # Create a polygon from the bounds
                    bbox = box(
                        st.session_state.area_polygon.bounds[0],
                        st.session_state.area_polygon.bounds[1],
                        st.session_state.area_polygon.bounds[2],
                        st.session_state.area_polygon.bounds[3]
                    )
                    
                    # Use features_from_polygon with the bbox
                    buildings = ox.features_from_polygon(
                        polygon=bbox,
                        tags={'building': True}
                    )
                    
                    # Convert to GeoDataFrame if needed
                    if not isinstance(buildings, gpd.GeoDataFrame):
                        buildings = gpd.GeoDataFrame(buildings)
                    
                    # Ensure CRS is set
                    if buildings.crs is None:
                        buildings.set_crs(epsg=4326, inplace=True)
                    
                    # Filter buildings that intersect with our polygon
                    mask = buildings.intersects(st.session_state.area_polygon)
                    buildings = buildings[mask].copy()
                    
                    # Estimate building heights
                    buildings = estimate_building_heights(buildings, k_neighbors=k_neighbors)
                    
                    # Classify buildings
                    buildings = classify_buildings(buildings, st.session_state.classification_rules)
                    
                    st.session_state.buildings_gdf = buildings
                    st.success(f"Found {len(buildings)} buildings in the selected area")
            
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")
            
            # Fetch census data
            try:
                census_data = get_census_data(
                    st.session_state.area_polygon
                )
                st.session_state.census_data = census_data
                st.success("Successfully fetched census data")
            except Exception as e:
                st.error(f"Error fetching census data: {str(e)}")
            
            # Add simulation button
            col1, col2, col3 = st.columns([2,1,2])
            with col2:
                if st.button("🚀 Run Simulation", type="primary"):
                    with st.spinner("Running demand simulation..."):
                        # Update demand calculation with new components
                        st.session_state.buildings_gdf['demand_potential'] = \
                            st.session_state.buildings_gdf.apply(
                                lambda x: calculate_demand_potential(
                                    x, 
                                    st.session_state.demand_params,
                                    components=st.session_state.demand_components,
                                    current_hour=st.session_state.current_hour if st.session_state.demand_components['time'] else None
                                ), 
                                axis=1
                            )
                        
                        # Update hotspots
                        st.session_state.buildings_gdf['is_hotspot'] = \
                            calculate_hotspots(st.session_state.buildings_gdf)
                        
                        st.success("Simulation completed! 🎯")

    if st.session_state.buildings_gdf is not None:
        with tab2:
            st.subheader("Building Overview")
            # Display basic building information map
            buildings_overview = st.session_state.buildings_gdf.reset_index(drop=True)
            fig = px.choropleth_mapbox(
                buildings_overview,
                geojson=buildings_overview.geometry.__geo_interface__,
                locations=buildings_overview.index,
                color='building',
                title="Building Types Overview",
                mapbox_style="carto-positron",
                center={"lat": st.session_state.area_polygon.centroid.y, 
                       "lon": st.session_state.area_polygon.centroid.x},
                zoom=14,
                width=800,
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Display summary statistics
            st.subheader("Summary Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Buildings", len(st.session_state.buildings_gdf))
            with col2:
                st.metric("Unique Building Types", 
                         st.session_state.buildings_gdf['building'].nunique())
            with col3:
                st.metric("Average Building Area", 
                         f"{st.session_state.buildings_gdf.geometry.area.mean():.1f} m²")
        
        with tab3:
            st.subheader("Building Classification")
            
            # Display current classification map
            buildings_classified = st.session_state.buildings_gdf.reset_index(drop=True)
            fig = px.choropleth_mapbox(
                buildings_classified,
                geojson=buildings_classified.geometry.__geo_interface__,
                locations=buildings_classified.index,
                color='delivery_class',
                color_discrete_map={
                    'DO': '#00ff00',  # Green for Delivery Origin
                    'DD': '#0000ff',  # Blue for Delivery Destination
                    'UD': '#ff0000'   # Red for Unlikely Delivery
                },
                title="Building Classification Map",
                mapbox_style="carto-positron",
                center={"lat": st.session_state.area_polygon.centroid.y, 
                       "lon": st.session_state.area_polygon.centroid.x},
                zoom=14,
                width=800,
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Display classification statistics
            stats = get_classification_stats(st.session_state.buildings_gdf)
            if stats:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Delivery Origins (DO)", 
                             f"{stats['by_class'].get('DO', 0)} ({stats['percentages'].get('DO', 0):.1f}%)")
                with col2:
                    st.metric("Delivery Destinations (DD)", 
                             f"{stats['by_class'].get('DD', 0)} ({stats['percentages'].get('DD', 0):.1f}%)")
                with col3:
                    st.metric("Unlikely Deliveries (UD)", 
                             f"{stats['by_class'].get('UD', 0)} ({stats['percentages'].get('UD', 0):.1f}%)")
            
            # Classification rules editor
            with st.expander("Edit Classification Rules"):
                st.markdown("""
                ### Classification Rules Editor
                
                - **DO (Delivery Origin)**: Stores, restaurants, warehouses
                - **DD (Delivery Destination)**: Residential buildings
                - **UD (Unlikely Delivery)**: Industrial, schools, hospitals
                
                Edit the rules below to customize building classification:
                """)
                
                edited_rules = st.session_state.classification_rules.copy()
                
                for category in ['DO', 'DD', 'UD']:
                    st.subheader(f"{category} Rules")
                    for tag_type in ['building', 'amenity', 'shop', 'landuse', 'residential']:
                        current_values = edited_rules[category]['tags'].get(tag_type, [])
                        new_values = st.text_input(
                            f"{tag_type} tags for {category}",
                            value=", ".join(current_values),
                            key=f"{category}_{tag_type}"
                        )
                        if new_values.strip():
                            edited_rules[category]['tags'][tag_type] = [
                                v.strip() for v in new_values.split(",")
                            ]
                        elif tag_type in edited_rules[category]['tags']:
                            del edited_rules[category]['tags'][tag_type]
                
                if st.button("Apply New Rules"):
                    st.session_state.classification_rules = edited_rules
                    if st.session_state.buildings_gdf is not None:
                        st.session_state.buildings_gdf = classify_buildings(
                            st.session_state.buildings_gdf,
                            edited_rules
                        )
                        st.experimental_rerun()
        
        with tab4:
            st.subheader("Census Data Overview")
            
            if st.session_state.census_data is not None:
                # Display census tract boundaries
                st.subheader("Census Tract Boundaries")
                center = [
                    st.session_state.area_polygon.centroid.x,
                    st.session_state.area_polygon.centroid.y
                ]
                
                # Create tabs for different census visualizations
                census_tabs = st.tabs([
                    "Overview",
                    "Demographics",
                    "Housing",
                    "Employment"
                ])
                
                with census_tabs[0]:
                    # Display summary statistics
                    st.subheader("Census Data Summary")
                    stats = get_census_stats(st.session_state.census_data)
                    
                    for var_name, var_stats in stats.items():
                        st.write(f"**{var_name}**")
                        cols = st.columns(5)
                        cols[0].metric("Mean", f"{var_stats['mean']:.1f}")
                        cols[1].metric("Median", f"{var_stats['median']:.1f}")
                        cols[2].metric("Std Dev", f"{var_stats['std']:.1f}")
                        cols[3].metric("Min", f"{var_stats['min']:.1f}")
                        cols[4].metric("Max", f"{var_stats['max']:.1f}")
                
                with census_tabs[1]:
                    st.subheader("Population Distribution")
                    fig = plot_census_choropleth(
                        st.session_state.census_data,
                        'Total Population',
                        center
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with census_tabs[2]:
                    st.subheader("Housing Units")
                    fig = plot_census_choropleth(
                        st.session_state.census_data,
                        'Total Housing Units',
                        center
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with census_tabs[3]:
                    st.subheader("Workers Distribution")
                    fig = plot_census_choropleth(
                        st.session_state.census_data,
                        'Workers 16 and over',
                        center
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            else:
                st.info("Please select an area to view census data.")

        with tab5:
            st.subheader("Population Allocation")
            
            if st.session_state.census_data is not None and st.session_state.buildings_gdf is not None:
                if st.button("Allocate Population to Buildings"):
                    # Allocate population to buildings
                    buildings_with_pop = allocate_population(
                        st.session_state.buildings_gdf,
                        st.session_state.census_data
                    )
                    st.session_state.buildings_gdf = buildings_with_pop
                    
                    # Display statistics about population allocation
                    total_pop = buildings_with_pop['estimated_population'].sum()
                    max_pop = buildings_with_pop['estimated_population'].max()
                    avg_pop = buildings_with_pop['estimated_population'].mean()
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Population", f"{total_pop:.0f}")
                    col2.metric("Max Building Population", f"{max_pop:.1f}")
                    col3.metric("Avg Building Population", f"{avg_pop:.1f}")
                    
                    # Create a choropleth map of building populations
                    buildings_pop = st.session_state.buildings_gdf.copy()
                    fig = px.choropleth_mapbox(
                        buildings_pop,
                        geojson=buildings_pop.geometry.__geo_interface__,
                        locations=buildings_pop.index,
                        color='estimated_population',
                        color_continuous_scale='Viridis',
                        title="Estimated Population per Building",
                        mapbox_style="carto-positron",
                        center={"lat": st.session_state.area_polygon.centroid.y, 
                               "lon": st.session_state.area_polygon.centroid.x},
                        zoom=14,
                        width=800,
                        height=600
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Sanity check: compare total population
                    census_total = st.session_state.census_data['Total Population'].sum()
                    allocation_total = buildings_pop['estimated_population'].sum()
                    
                    st.write("### Population Allocation Sanity Check")
                    st.write(f"Census Total Population: {census_total:,.0f}")
                    st.write(f"Allocated Total Population: {allocation_total:,.0f}")
                    st.write(f"Difference: {abs(census_total - allocation_total):,.0f}")
                    st.write(f"Percentage Difference: {abs(census_total - allocation_total) / census_total * 100:.2f}%")
            
            else:
                st.info("Please load both building and census data to allocate population.")

        with tab6:
            st.subheader("Building Heights")
            # Show building heights visualization
            height_fig = plot_building_heights(st.session_state.buildings_gdf)
            st.plotly_chart(height_fig, use_container_width=True)
            
            # Show height statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Height", f"{st.session_state.buildings_gdf['height'].mean():.1f}m")
            with col2:
                st.metric("Known Heights", f"{(~st.session_state.buildings_gdf['height_estimated']).sum()}")
            with col3:
                st.metric("Estimated Heights", f"{st.session_state.buildings_gdf['height_estimated'].sum()}")

        with tab7:
            st.subheader("Demand Estimation")
            # Calculate demand potential
            params = {
                'alpha': alpha,
                'beta': beta,
                'epsilon': 1.0,
                'zeta': 1.0
            }
            
            st.session_state.buildings_gdf['demand_potential'] = \
                st.session_state.buildings_gdf.apply(
                    lambda x: calculate_demand_potential(x, params), axis=1)
            
            # Identify hotspots
            st.session_state.buildings_gdf['is_hotspot'] = \
                calculate_hotspots(st.session_state.buildings_gdf)
            
            # Create demand heatmap
            buildings_df = st.session_state.buildings_gdf.reset_index(drop=True)
            fig = px.choropleth_mapbox(
                buildings_df,
                geojson=buildings_df.geometry.__geo_interface__,
                locations=buildings_df.index,
                color='demand_potential',
                color_continuous_scale="Viridis",
                opacity=0.7,
                center={"lat": st.session_state.area_polygon.centroid.y, 
                       "lon": st.session_state.area_polygon.centroid.x},
                zoom=14,
                width=800,
                height=600,
                mapbox_style="carto-positron",
                title="Demand Potential Heatmap"
            )
            
            # Add hotspots
            hotspots = buildings_df[buildings_df['is_hotspot']]
            if len(hotspots) > 0:
                fig.add_scattermapbox(
                    lat=hotspots.geometry.centroid.y,
                    lon=hotspots.geometry.centroid.x,
                    mode='markers',
                    marker=dict(size=10, color='red'),
                    name='Hotspots'
                )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display key statistics
            st.subheader("Key Statistics")
            stats = get_summary_statistics(st.session_state.buildings_gdf)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Buildings", f"{stats['total_buildings']:,}")
            with col2:
                st.metric("Average Demand", f"{stats['avg_demand']:.2f}")
            with col3:
                st.metric("Hotspots", f"{stats['hotspot_count']:,}")

if __name__ == "__main__":
    main()
