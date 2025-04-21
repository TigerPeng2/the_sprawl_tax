import json

with open('unioncity_filtered.geojson', 'r') as f: #here
    data = json.load(f)

print("Type of GeoJSON decatur:", data.get('type')) #here
print(data['features'][0])

# zoning_descriptions = set()

# for feature in data['features']:
#     desc = feature['properties'].get('ZoningNew')
#     if desc:
#         zoning_descriptions.add(desc)

# # Print each unique description
# for desc in sorted(zoning_descriptions):
#     print(desc)

