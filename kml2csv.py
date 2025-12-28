def extract_places_with_coordinates(kml_path_or_string, from_string=False):
    import xml.etree.ElementTree as ET
    NS = {'kml': 'http://www.opengis.net/kml/2.2'}

    if from_string:
        root = ET.fromstring(kml_path_or_string)
    else:
        tree = ET.parse(kml_path_or_string)
        root = tree.getroot()

    places = []
    for pm in root.findall('.//kml:Placemark', NS):
        name_el = pm.find('kml:name', NS)
        full_name = (name_el.text or '').strip()
        
        # Split code and name
        code = ''
        name = full_name
        parts = full_name.split(' ', 1)
        if len(parts) == 2 and parts[0].isupper() and len(parts[0]) >= 3:
            code = parts[0]
            name = parts[1].strip()

        coords_el = pm.find('.//kml:coordinates', NS)
        if coords_el is None or not (coords_el.text and coords_el.text.strip()):
            continue

        # coordinates may contain multiple coordinate tuples; take the first
        coord_text = coords_el.text.strip().split()[0]
        parts = coord_text.split(',')
        try:
            lon = float(parts[0])
            lat = float(parts[1]) if len(parts) > 1 else None
            alt = float(parts[2]) if len(parts) > 2 else None
        except ValueError:
            continue

        places.append({
            'name': name, 
            'code': code,
            'lon': lon, 
            'lat': lat, 
            'alt': alt
        })

    return places

def save_places_to_csv(places, output_file):
    import csv
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        #writer.writerow(['Type', 'Name', 'Code', 'Latitude', 'Longitude'])
        
        # Write data
        for place in places:
            writer.writerow([
                'Location',
                place['name'],
                place['code'],
                place['lat'],
                place['lon']
            ])

# Example usage
places = extract_places_with_coordinates("test.kml")
save_places_to_csv(places, "airports.csv")