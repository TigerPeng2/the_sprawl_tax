import json
from shapely.geometry import shape, mapping

def generalize_zoning(code):
    if not code:
        return 'Unknown'

    code = code.upper().strip()

    single_family = {
    'R-1', 'R-2', 'R-3', 'R-4', 'R-5', 'R-6', 'R-60', 'R-75', 'R-85', 'R-100', 'RE', 'RSM',
    'R-2A', 'R-3A', 'R-4A', 'R-5A', 'RS100', 'RS200', 'RS15', 'RS180', 'RA', 'RA-5', 'RA-8',
    'RA200', 'RLL', 'RL', 'RD', 'RTH', 'RS100CSD', 'RS100PRD', 'RS150', 'RS30', 'RS5', 'RS60',
    'RS72', 'RSR', 'RZT', 'Single-Family Residential', 'Single-family Residential',
    'Single Family Residential', 'Single Family Cluster Residential', 
    'Single Family Attached Residential', 'Single Family Attached Residential Conditional'
    }

    multi_family = {
        'MR-1', 'MR-2', 'RM', 'RM-3', 'RM-3/8', 'RM-4', 'RM-6', 'RM-8', 'RM-10', 'RM-12', 'RM-24',
        'RM-HD', 'RMHR', 'RMD', 'RMD-1', 'RDU', 'Multi Family Residential', 'Multifamily Residential',
        'Mulitfamily Residential', 'Two- and Three-Family Residential', 'Townhomes - UPA',
        'MULTI FAMILY RESIDENCE', 'MULTI-FAMILY APARTMENTS CONDITIONAL'
    }

    commercial = {
        'C-1', 'C-2', 'CS', 'CS-3', 'CS-4', 'CS-5', 'CS-6', 'CC-3', 'CX-3', 'CX-6', 'GC', 'NC',
        'NS', 'General Commercial', 'Local Commercial', 'Corridor Commercial', 'Corridor village commercial',
        'Neighborhood Commercial', 'Neighborhood Commercial 1', 'Neighborhood Commercial 2',
        'Neighborhood Commercial District', 'Neighborhood Shopping', 'Village Commercial',
        'Village commercial', 'CX', 'BG', 'BGC', 'BH', 'BN', 'CB', 'CH', 'CI', 'CMU', 'CSO',
        'C1', 'C2', 'C1C', 'C2C', 'C1M', 'C2M', 'CL', 'CLC', 'CLM', 'CR', 'CRC'
    }
    if code in single_family:
        return 'Single Family Residential'
    elif code in multi_family:
        return 'Multiple Family Residential'
    elif code in commercial:
        return 'Commercial'
    else:
        return 'Mixed Use'

# Load GeoJSON file
with open('UnionCity_Zoning.geojson', 'r') as f: #here
    data = json.load(f)

new_features = []

for feature in data['features']:
    props = feature.get('properties', {})
    geometry = feature.get('geometry')

    if not geometry or geometry['type'] != 'Polygon':
        continue  # skip invalid geometries

    # Extract zoning info
    zoning_class = props.get('ZoningNew') # R-4  #here
    zoning_desc = props.get('ZoningNew') #single-fam #here

    try:
        polygon = shape(geometry)
        centroid = polygon.centroid
        lat, lon = centroid.y, centroid.x
    except Exception as e:
        print(f"Skipping invalid geometry: {e}")
        continue

    # Build new feature
    new_feature = {
        "type": "Feature",
        "geometry": geometry,
        "properties": {
            "zoning_classification": zoning_class,
            "zoning_description": generalize_zoning(zoning_desc),
            "centroid_lat": lat,
            "centroid_lon": lon
        }
    }

    new_features.append(new_feature)

# Build new FeatureCollection
output_geojson = {
    "type": "FeatureCollection",
    "name": "Filtered_Zoning_Parcels",
    "features": new_features
}

# Write to a new GeoJSON file
with open('unioncity_filtered.geojson', 'w') as f: #here
    json.dump(output_geojson, f, separators=(',', ':'))

print("Filtered GeoJSON saved as 'unioncity_filtered.geojson'") #here
