# Project Development Instructions for Drone Delivery Demand Estimation Web Application

## Table of Contents

1. [Introduction](#1-introduction)
2. [Project Overview](#2-project-overview)
3. [Technical Stack](#3-technical-stack)
4. [System Architecture](#4-system-architecture)
5. [Data Acquisition and Preprocessing](#5-data-acquisition-and-preprocessing)
   - 5.1 [OpenStreetMap (OSM) Data](#51-openstreetmap-osm-data)
   - 5.2 [U.S. Census Data](#52-us-census-data)
   - 5.3 [Data Cleaning and Standardization](#53-data-cleaning-and-standardization)
   - 5.4 [Building Height Estimation](#54-building-height-estimation)
6. [Backend Development](#6-backend-development)
   - 6.1 [Data Processing Pipeline](#61-data-processing-pipeline)
   - 6.2 [Demand Estimation Model](#62-demand-estimation-model)
   - 6.3 [Sensitivity Analysis and Sobol' Indices](#63-sensitivity-analysis-and-sobol-indices)
7. [Frontend Development](#7-frontend-development)
   - 7.1 [User Interface Design](#71-user-interface-design)
   - 7.2 [Interactive Visualization](#72-interactive-visualization)
   - 7.3 [Parameter Adjustment Controls](#73-parameter-adjustment-controls)
8. [Implementation Steps](#8-implementation-steps)
   - 8.1 [Setup and Environment](#81-setup-and-environment)
   - 8.2 [Data Acquisition Scripts](#82-data-acquisition-scripts)
   - 8.3 [Data Processing Functions](#83-data-processing-functions)
   - 8.4 [Model Implementation](#84-model-implementation)
   - 8.5 [Frontend Integration](#85-frontend-integration)
9. [Testing and Validation](#9-testing-and-validation)
10. [Deployment](#10-deployment)
11. [Additional Features and Considerations](#11-additional-features-and-considerations)
12. [Appendix](#12-appendix)
    - 12.1 [Formulas and Mathematical Expressions](#121-formulas-and-mathematical-expressions)

---

## 1. Introduction

This document provides detailed instructions for developing a user-friendly web application that estimates last-mile drone delivery demand using open-source data. The application allows users to interactively adjust parameters, visualize data at each processing step, perform sensitivity analyses, and understand the impact of various factors on drone delivery demand.

---

## 2. Project Overview

The goal is to create a prototype web application that:

- **Processes and visualizes geospatial and demographic data** for any user-selected area within the United States.
- **Estimates drone delivery demand** at the individual building level, considering various demographic and spatial factors.
- **Allows users to adjust model parameters interactively**, with real-time updates to the demand estimations and visualizations.
- **Provides statistical analyses and sensitivity analyses**, including Sobol' indices, to understand the influence of different parameters.
- **Offers step-by-step data visualization** for users to perform sanity checks at each stage of data processing.

---

## 3. Technical Stack

- **Programming Language**: Python 3.x
- **Web Framework**: Streamlit (preferred for simplicity and rapid development)
- **Geospatial Libraries**:
  - `geopandas` for spatial data manipulation
  - `osmnx` for OpenStreetMap data extraction
  - `folium` or `plotly` for interactive maps
- **Data Analysis Libraries**:
  - `pandas` for data manipulation
  - `numpy` for numerical computations
  - `scipy` for statistical analyses
  - `SALib` for sensitivity analysis and Sobol' indices
- **Visualization Libraries**:
  - `matplotlib` and `seaborn` for plotting
  - `plotly` for interactive visualizations
- **Other Libraries**:
  - `scikit-learn` for machine learning tasks (e.g., k-NN regression)
  - `requests` and `json` for API interactions
- **Deployment Platform**: Streamlit Sharing or Heroku (for sharing with one person)

---

## 4. System Architecture

- **Frontend**: Streamlit app that runs in the user's browser, providing interactive controls and visualizations.
- **Backend**: Python scripts and functions that handle data processing, model computations, and data retrieval.
- **Data Storage**: In-memory data processing for prototype; consider using temporary caching for performance optimization.

---

## 5. Data Acquisition and Preprocessing

### 5.1 OpenStreetMap (OSM) Data

**Objective**: Extract building footprints, attributes, and Points of Interest (POIs) for the user-selected area.

- **Tools**: Use `osmnx` to download and process OSM data.
- **Data Elements**:
  - Building footprints (`building` tags)
  - Building attributes (`height`, `building:levels`, `amenity`, `shop`, `office` tags)
  - POIs such as retail stores and restaurants (`amenity`, `shop` tags)

**Implementation Steps**:

1. **Define Area of Interest (AoI)**: Allow users to select an area by drawing a polygon on a map or entering an address/coordinates.
2. **Download Data**: Use `osmnx.geometries_from_polygon()` to fetch building data within the AoI.
3. **Extract Relevant Tags**: Focus on tags necessary for classification and modeling.

### 5.2 U.S. Census Data

**Objective**: Retrieve demographic and socioeconomic data for the AoI.

- **Tools**: Use `census` API or `cenpy` library.
- **Data Elements**:
  - Population statistics
  - Median household income
  - Age distribution
  - Occupancy rates
  - Employment rates

**Implementation Steps**:

1. **Obtain Census Geographies**: Match the AoI to corresponding census tracts or blocks.
2. **Fetch Data**: Use the Census API to retrieve ACS variables for these geographies.
3. **Data Mapping**: Associate demographic data with spatial units (census tracts/blocks).

### 5.3 Data Cleaning and Standardization

**Objective**: Ensure data consistency and handle missing or conflicting information.

**Implementation Steps**:

1. **Standardize Tags**: Convert all tags to lowercase and handle synonyms.
2. **Handle Missing Values**: Implement strategies to estimate missing building attributes.
3. **Filter Relevant Features**: Exclude irrelevant or incomplete data entries.

### 5.4 Building Height Estimation

**Objective**: Estimate building heights for buildings lacking height data.

**Methodology**:

- **Available Data**:
  - If `building:levels` is available, estimate height:
    \[
    H = N_{\text{floors}} \times h_{\text{avg}}
    \]
- **k-NN Regression**:
  - For buildings without height or levels, use k-NN regression based on nearby buildings with known heights.
  
**Implementation Steps**:

1. **Identify Buildings Lacking Height Data**.
2. **Collect Neighboring Buildings with Known Heights**.
3. **Compute Estimated Heights** using the average height of k nearest neighbors.
4. **Visualization**: Provide an option to visualize the height estimation process on the map.

---

## 6. Backend Development

### 6.1 Data Processing Pipeline

**Objective**: Process raw data into inputs suitable for the demand estimation model.

**Implementation Steps**:

1. **Spatial Join**: Associate buildings with census data.
2. **Building Classification**: Assign each building to `DO`, `DD`, or `UD` based on OSM tags.
3. **Population Allocation**: Distribute census population to buildings based on volume and occupancy rates.
4. **Parameter Preparation**: Prepare all variables required for the demand model.

### 6.2 Demand Estimation Model

**Objective**: Compute the expected drone delivery demand for each building.

**Key Components**:

1. **Demand Potential Score (\( D_j \))**:
   \[
   D_j = \left( \frac{P_{\text{adj}, j}}{P_{\text{max}}} \right)^\alpha \times \left( \frac{I_j}{I_{\text{max}}} \right)^\beta \times B_j^\epsilon \times PF_j^\zeta
   \]
   - Allow users to adjust exponents \( \alpha, \beta, \epsilon, \zeta \).
   - Users can select which demographic variables to include.
2. **Proximity Factor (\( PF_j \))**:
   \[
   PF_j = \frac{1}{(d_{\text{store}, j} + \epsilon)^\eta}
   \]
   - Allow users to adjust \( \eta \) and \( \epsilon \).
3. **Temporal Weight (\( T(t) \))**:
   \[
   T(t) = f_{\text{hour}}(h) \times f_{\text{day}}(d) \times f_{\text{month}}(m)
   \]
   - Users can select temporal profiles or adjust parameters like \( \mu_h \) and \( \sigma_h \).
4. **Expected Deliveries (\( \lambda_j(t) \))**:
   \[
   \lambda_j(t) = D_j \times T(t) \times \lambda_0
   \]
   - Allow users to adjust base rate \( \lambda_0 \).

### 6.3 Sensitivity Analysis and Sobol' Indices

**Objective**: Assess the influence of each parameter on the output demand estimates.

**Implementation Steps**:

1. **Parameter Sampling**: Use `SALib` to define parameter ranges and distributions.
2. **Run Simulations**: Perform Monte Carlo simulations varying parameters within specified ranges.
3. **Compute Sobol' Indices**: Calculate first-order and total-order indices.
4. **Visualization**: Display sensitivity analysis results, highlighting influential parameters.

---

## 7. Frontend Development

### 7.1 User Interface Design

**Objective**: Create an intuitive and interactive interface for users to interact with the model.

**Key Components**:

1. **Sidebar Controls**: For parameter adjustments and data selection.
2. **Main Panel**: Display maps, visualizations, and results.
3. **Step-by-Step Tabs**: Allow users to navigate through data processing stages.

### 7.2 Interactive Visualization

**Objective**: Provide real-time visual feedback based on user inputs.

**Implementation Steps**:

1. **Map Display**: Use `folium` or `plotly` to display the AoI and building data.
2. **Heatmaps**: Generate heatmaps of demand estimates that update in real-time.
3. **Data Inspection**: Allow users to click on buildings to see underlying data and calculations.

### 7.3 Parameter Adjustment Controls

**Objective**: Enable users to modify model parameters and see immediate effects.

**Implementation Steps**:

1. **Sliders and Input Fields**: For adjusting exponents (\( \alpha, \beta, \epsilon, \zeta \)), base rates, and temporal parameters.
2. **Checkboxes**: To include or exclude specific demographic variables.
3. **Real-Time Updates**: Ensure that changes trigger recalculations and visual updates.

---

## 8. Implementation Steps

### 8.1 Setup and Environment

1. **Install Python 3.x** and necessary libraries using `pip` or `conda`.
2. **Create a Virtual Environment** to manage dependencies.
3. **Install Streamlit**:
   ```bash
   pip install streamlit
   ```
4. **Install Required Libraries**:
   ```bash
   pip install geopandas osmnx pandas numpy matplotlib seaborn plotly folium scikit-learn SALib requests
   ```

### 8.2 Data Acquisition Scripts

**OSM Data Extraction**:

- **Function**: `get_osm_data(aoi_polygon)`
- **Inputs**: Polygon defining the AoI.
- **Outputs**: GeoDataFrames for buildings and POIs.
- **Steps**:
  1. Use `osmnx.geometries_from_polygon()` to fetch data.
  2. Filter data for relevant tags.
  3. Return cleaned GeoDataFrames.

**Census Data Retrieval**:

- **Function**: `get_census_data(census_geographies)`
- **Inputs**: List of census tracts/blocks.
- **Outputs**: DataFrame with demographic data.
- **Steps**:
  1. Use the Census API to fetch ACS variables.
  2. Map data to geographies.
  3. Return DataFrame.

### 8.3 Data Processing Functions

**Building Classification**:

- **Function**: `classify_buildings(buildings_gdf)`
- **Inputs**: GeoDataFrame of buildings.
- **Outputs**: Updated GeoDataFrame with classification.
- **Steps**:
  1. Extract relevant tags.
  2. Apply classification logic.
  3. Add a new column `classification`.

**Building Height Estimation**:

- **Function**: `estimate_building_heights(buildings_gdf)`
- **Inputs**: GeoDataFrame of buildings.
- **Outputs**: Updated GeoDataFrame with height estimates.
- **Steps**:
  1. Identify buildings lacking height data.
  2. Implement k-NN regression.
  3. Update heights in the GeoDataFrame.

**Population Allocation**:

- **Function**: `allocate_population(buildings_gdf, census_data)`
- **Inputs**: Buildings GeoDataFrame, Census DataFrame.
- **Outputs**: Updated GeoDataFrame with population estimates.
- **Steps**:
  1. Calculate building volumes.
  2. Allocate population proportionally.
  3. Adjust for occupancy rates.

### 8.4 Model Implementation

**Demand Potential Score Calculation**:

- **Function**: `calculate_demand_potential(buildings_gdf, parameters)`
- **Inputs**: Buildings GeoDataFrame, user-defined parameters.
- **Outputs**: Updated GeoDataFrame with `D_j`.
- **Formula**:
  \[
  D_j = \left( \frac{P_{\text{adj}, j}}{P_{\text{max}}} \right)^\alpha \times \left( \frac{I_j}{I_{\text{max}}} \right)^\beta \times B_j^\epsilon \times PF_j^\zeta
  \]

**Proximity Factor Calculation**:

- **Function**: `calculate_proximity_factor(buildings_gdf, pois_gdf, parameters)`
- **Inputs**: Buildings GeoDataFrame, POIs GeoDataFrame, parameters.
- **Outputs**: Updated GeoDataFrame with `PF_j`.
- **Steps**:
  1. Compute distances to nearest retail store.
  2. Apply the proximity factor formula.

**Temporal Weight Calculation**:

- **Function**: `calculate_temporal_weight(time, parameters)`
- **Inputs**: Time parameters (hour, day, month), user-defined parameters.
- **Outputs**: Temporal weight `T(t)`.
- **Formula**:
  \[
  T(t) = f_{\text{hour}}(h) \times f_{\text{day}}(d) \times f_{\text{month}}(m)
  \]

**Expected Deliveries Simulation**:

- **Function**: `simulate_deliveries(buildings_gdf, parameters)`
- **Inputs**: Buildings GeoDataFrame, parameters.
- **Outputs**: Updated GeoDataFrame with expected deliveries.
- **Steps**:
  1. Calculate \( \lambda_j(t) \) for each building.
  2. Simulate deliveries using Poisson distribution.

### 8.5 Frontend Integration

**Streamlit App Structure**:

1. **Main Script**: `app.py`
2. **Sections**:
   - **Home Page**: Introduction and instructions.
   - **Data Exploration**: Visualize raw data (OSM and Census).
   - **Data Processing Steps**:
     - Building classification visualization.
     - Height estimation visualization.
     - Population allocation visualization.
   - **Model Parameters**: Interactive controls for adjusting parameters.
   - **Demand Visualization**: Heatmaps and statistics.
   - **Sensitivity Analysis**: Display Sobol' indices and impact of parameters.
   - **Census Data and Population**: Instructions for using census data features.

**Implementation Steps**:

1. **Create Sidebar Controls**:
   - Input fields for AoI selection.
   - Sliders and checkboxes for parameters.
2. **Main Panel Displays**:
   - Use `st.map()` or `folium` for maps.
   - Use `st.pyplot()` or `plotly` for charts.
3. **Callbacks**:
   - Ensure that changes in parameters trigger recalculations.
   - Use `@st.cache` where appropriate to optimize performance.

---

## Census Data and Population

### Setting Up Census API
1. Get a Census API key from https://api.census.gov/data/key_signup.html
2. Enter your API key in the "Census Data Overview" tab
3. The key will be securely stored for your session

### Viewing Census Data
1. Navigate to the "Census Data Overview" tab
2. View different demographic variables through the subtabs:
   - Overview: Summary statistics for all variables
   - Demographics: Population distribution
   - Housing: Housing unit distribution
   - Employment: Worker distribution

### Population Allocation
1. Go to the "Population Allocation" tab
2. Click "Allocate Population to Buildings" to distribute population
3. Review the allocation results:
   - Population heatmap
   - Building-level statistics
   - Sanity check comparisons

### Tips
- Ensure buildings are classified before population allocation
- Check the sanity metrics to verify reasonable allocation
- Use the population data to refine demand estimates

---

## 9. Testing and Validation

1. **Unit Tests**: Write tests for each function to ensure correctness.
2. **Data Validation**: Check data at each processing step; provide visualizations for sanity checks.
3. **Model Verification**: Compare model outputs with expected results or known benchmarks.
4. **User Testing**: Have users interact with the app to identify usability issues.

---

## 10. Deployment

1. **Prepare for Deployment**:
   - Ensure all dependencies are listed in `requirements.txt`.
2. **Deploy on Streamlit Sharing**:
   - Push code to a GitHub repository.
   - Connect the repository to Streamlit Sharing.
   - Share the app URL with the intended user.
3. **Alternative Deployment**:
   - Use Heroku or another cloud platform if needed.
   - Configure necessary environment variables and settings.

---

## 11. Additional Features and Considerations

- **Error Handling**: Provide informative messages for data retrieval failures or invalid inputs.
- **Performance Optimization**: Use caching (`@st.cache`) and optimize data processing to handle larger AoIs efficiently.
- **Documentation**: Include user guides and documentation within the app using `st.markdown()`.
- **Security**: Since the app is shared with one person, ensure access is controlled if sensitive data is involved.
- **Extensibility**: Design the codebase to allow for future enhancements, such as integrating additional data sources or machine learning models.

---

## 12. Appendix

### 12.1 Formulas and Mathematical Expressions

1. **Building Height Estimation**:
   - Using number of floors:
     \[
     H = N_{\text{floors}} \times h_{\text{avg}}
     \]
   - Using k-NN estimation:
     \[
     H = \frac{1}{k} \sum_{j=1}^{k} H_j
     \]
2. **Building Volume**:
   \[
   V_i = A_{\text{footprint}, i} \times H_i
   \]
3. **Population Allocation**:
   \[
   P_i = P_{\text{block}} \times \left( \frac{V_i}{\sum_{k} V_k} \right)
   \]
4. **Adjusted Population**:
   \[
   P_{\text{adj}, i} = P_i \times O_{\text{rate}}
   \]
5. **Demand Potential Score**:
   \[
   D_j = \left( \frac{P_{\text{adj}, j}}{P_{\text{max}}} \right)^\alpha \times \left( \frac{I_j}{I_{\text{max}}} \right)^\beta \times B_j^\epsilon \times PF_j^\zeta
   \]
6. **Proximity Factor**:
   \[
   PF_j = \frac{1}{(d_{\text{store}, j} + \epsilon)^\eta}
   \]
7. **Temporal Weight**:
   \[
   T(t) = f_{\text{hour}}(h) \times f_{\text{day}}(d) \times f_{\text{month}}(m)
   \]
   - **Hourly Function** (Gaussian):
     \[
     f_{\text{hour}}(h) = \exp\left( -\frac{(h - \mu_h)^2}{2\sigma_h^2} \right)
     \]
   - **Daily Function**:
     \[
     f_{\text{day}}(d) = \begin{cases}
     \alpha_{\text{weekday}} & \text{if } d \in \{\text{Monday, ..., Friday}\} \\
     \alpha_{\text{weekend}} & \text{if } d \in \{\text{Saturday, Sunday}\}
     \end{cases}
     \]
   - **Monthly Function**:
     \[
     f_{\text{month}}(m) = \begin{cases}
     \beta_{\text{holiday}} & \text{if } m \in \{\text{November, December}\} \\
     1 & \text{otherwise}
     \end{cases}
     \]
8. **Expected Deliveries**:
   \[
   \lambda_j(t) = D_j \times T(t) \times \lambda_0
   \]
9. **Poisson Distribution**:
   - Simulating deliveries:
     \[
     k_j(t) \sim \text{Poisson}(\lambda_j(t))
     \]
10. **Sensitivity Analysis**:
    - **Sobol' Indices**: Calculated using the `SALib` library based on parameter variations.

---

**Note**: Feel free to update and modify this document as the project progresses.