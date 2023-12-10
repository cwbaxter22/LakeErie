import folium 

def map_main(selected_buoy):
    """
    Generate a Folium map with buoy locations and markers.

    Arguments:
    selected_buoy (str): The name of the selected buoy.

    Returns:
    folium.Map: Folium map object showing buoy locations with markers.

    Raises:
    ValueError: If the selected_buoy is not in the predefined list of buoy names.
    ValueError: If latitude or longitude values for any buoy are not numeric.
    """

    # Define the center of the map (for example, using the coordinates of Buoy 3)
    center_latitude, center_longitude = 42.10992, -80.15459

    # Define the buoy locations
    buoy_locations = [
    {"name": "Beach2_Buoy", "latitude": 42.15763, "longitude": -80.14044},
    {"name": "Beach2_Tower", "latitude": 42.15381, "longitude": -80.13071},
    {"name": "Beach6_Buoy", "latitude": 42.16363, "longitude": -80.12830},
    {"name": "Near_Shore_Buoy", "latitude": 42.17890, "longitude": -80.12679},
    {"name": "Walnut_Creek", "latitude": 42.13970, "longitude": -80.28418},
    {"name": "Trec_Tower", "latitude": 42.10992, "longitude": -80.15459},
    {"name": "Surface_Data", "latitude": 42.116952, "longitude": -80.149409},
    ]
    # Check if the selected buoy is in the predefined list
    buoy_names = [buoy["name"] for buoy in buoy_locations]
    if selected_buoy not in buoy_names:
        raise ValueError(f"Invalid selected buoy '{selected_buoy}'. "
                         f"Please select a valid buoy from the list.")

    # Check latitude and longitude values for completeness and numeric format
    for buoy in buoy_locations:
        if not isinstance(buoy["latitude"], (float, int)) or not isinstance(buoy["longitude"], (float, int)):
            raise ValueError(f"Invalid coordinates for buoy '{buoy['name']}'. "
                             "Latitude and longitude must be numeric.")

    # Create a map object using Folium
    m = folium.Map(location=[center_latitude, center_longitude], zoom_start=11)

    # Add markers for each buoy
    for buoy in buoy_locations:
        color = "red" if buoy["name"] == selected_buoy else "gray"
        folium.Marker([buoy["latitude"], buoy["longitude"]],
                      popup=buoy["name"], icon=folium.Icon(color=color)).add_to(m)

    folium.TileLayer('cartodbdark_matter').add_to(m)
    
    return m