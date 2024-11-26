# Technical Notes: Drone Delivery Demand Estimation

## Key Learnings

### Geospatial Data Handling
- **CRS Issues**: Always project geometries before distance calculations
  ```python
  utm_zone = int((df.geometry.centroid.x.mean() + 180) / 6) + 1
  utm_crs = f'EPSG:326{utm_zone}' if df.geometry.centroid.y.mean() >= 0 else f'EPSG:327{utm_zone}'
  df_projected = df.to_crs(utm_crs)
  ```

### Plotly + GeoPandas Integration
- Reset GeoDataFrame index before choropleth creation to avoid MultiIndex errors
- Ensure consistent map dimensions (800x600) for better UX
- Use `use_container_width=True` for responsive layouts

### Streamlit Layout
- Avoid nested columns (max one level deep)
- Use tabs for complex multi-view layouts
- Keep sidebar for parameters and controls

### Building Height Estimation
1. Primary source: OSM `height` tag
2. Secondary: `building:levels` × 3.0m
3. Fallback: k-NN with projected coordinates
4. Default: 10.0m if insufficient data

### Performance Tips
- Project coordinates once, store results
- Pre-calculate centroids when used multiple times
- Reset indices early in the pipeline

## Census Data Integration

### Data Sources
- American Community Survey (ACS) 5-year estimates (2021)
- Census tract level data for demographic and socioeconomic variables
- Key variables:
  - Total Population (B01003_001E)
  - Median Household Income (B19013_001E)
  - Total Housing Units (B25001_001E)
  - Workers 16 and over (B08014_001E)
  - Total Units in Structure (B25024_001E)

### Population Allocation Methodology
1. Population is allocated only to buildings classified as Delivery Destinations (DD)
2. Within each census tract:
   - Calculate total residential building area
   - Distribute population proportionally based on building area
   - Non-residential buildings receive zero population

### Sanity Checks
- Total allocated population should match census tract totals
- Population density per building area should be reasonable
- Zero population in non-residential buildings
- Population distribution should follow expected patterns (e.g., higher in apartment buildings)

### Technical Limitations
- Assumes uniform population density within residential buildings
- Does not account for building vacancy rates
- May not capture mixed-use buildings accurately
- Census tract boundaries may not align perfectly with natural neighborhood boundaries

## TODO
- [ ] Implement building classification editor
- [ ] Add temporal demand patterns
- [ ] Optimize k-NN calculations for large areas
