"""Building classification utilities for drone delivery demand estimation."""

import pandas as pd
import json
import os

# Default classification rules
DEFAULT_RULES = {
    "DO": {  # Delivery Origin
        "tags": {
            "shop": ["supermarket", "convenience", "mall"],
            "amenity": ["restaurant", "cafe", "fast_food"],
            "building": ["retail", "commercial", "warehouse"]
        },
        "priority": 1
    },
    "DD": {  # Delivery Destination
        "tags": {
            "building": ["residential", "house", "apartments", "dormitory"],
            "residential": ["yes"]
        },
        "priority": 2
    },
    "UD": {  # Unlikely Delivery
        "tags": {
            "building": ["industrial", "garage", "parking", "shed", "construction"],
            "amenity": ["school", "hospital", "police", "fire_station"],
            "landuse": ["industrial"]
        },
        "priority": 3
    }
}

def load_classification_rules(custom_rules_path=None):
    """Load building classification rules from file or use defaults."""
    if custom_rules_path and os.path.exists(custom_rules_path):
        with open(custom_rules_path, 'r') as f:
            return json.load(f)
    return DEFAULT_RULES

def save_classification_rules(rules, filepath):
    """Save classification rules to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(rules, f, indent=2)

def classify_building(building, rules):
    """Classify a single building based on its tags."""
    classifications = []
    
    # Check each category (DO, DD, UD)
    for category, category_rules in rules.items():
        for tag_key, valid_values in category_rules["tags"].items():
            if tag_key in building and building[tag_key] in valid_values:
                classifications.append((category, category_rules["priority"]))
                break
    
    if not classifications:
        return "UD"  # Default to Unlikely Delivery if no match
    
    # Return the category with highest priority (lowest priority number)
    return min(classifications, key=lambda x: x[1])[0]

def classify_buildings(gdf, rules=None):
    """Classify all buildings in a GeoDataFrame."""
    if rules is None:
        rules = DEFAULT_RULES
    
    # Create a copy to avoid modifying the original
    gdf = gdf.copy()
    
    # Apply classification to each building
    gdf['delivery_class'] = gdf.apply(lambda x: classify_building(x, rules), axis=1)
    
    return gdf

def get_classification_stats(gdf):
    """Get statistics about building classifications."""
    if 'delivery_class' not in gdf.columns:
        return None
    
    stats = {
        'total': len(gdf),
        'by_class': gdf['delivery_class'].value_counts().to_dict(),
        'percentages': (gdf['delivery_class'].value_counts(normalize=True) * 100).to_dict()
    }
    
    return stats
