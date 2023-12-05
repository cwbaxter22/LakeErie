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
    center_latitude, center_longitude = 51.5074, -0.1278

    # Define the buoy locations
    buoy_locations = [
        {"name": "Buoy 1", "latitude": 40.7128, "longitude": -74.0060},
        {"name": "Buoy 2", "latitude": 34.0522, "longitude": -118.2437},
        {"name": "Buoy 3", "latitude": 51.5074, "longitude": -0.1278},
        {"name": "Buoy 4", "latitude": 48.8566, "longitude": 2.3522},
        {"name": "Buoy 5", "latitude": 55.7558, "longitude": 37.6176},
        {"name": "Buoy 6", "latitude": -33.8651, "longitude": 151.2093}
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
    m = folium.Map(location=[center_latitude, center_longitude], zoom_start=13)

    # Add markers for each buoy
    for buoy in buoy_locations:
        color = "red" if buoy["name"] == selected_buoy else "gray"
        folium.Marker([buoy["latitude"], buoy["longitude"]],
                      popup=buoy["name"], icon=folium.Icon(color=color)).add_to(m)

    return m