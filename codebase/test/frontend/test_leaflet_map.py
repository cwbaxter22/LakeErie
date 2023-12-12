"""Test cases for the map_main function in leaflet_map.py, 
    which used folium to create a simple map of Bouy locations
    and a specified basemap. Location markers turn red based 
    on the user selected site location."""

import unittest
import importlib
import pathlib

codebase_path = pathlib.Path(__file__).parents[2]
leaflet_map_mod_path = codebase_path / "src" / "frontend" / "leaflet_map.py"

spec = importlib.util.spec_from_file_location(
    name="leaflet_map_mod",
    location=str(leaflet_map_mod_path),
)

leaflet_map_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(leaflet_map_mod)


class TestMapMain(unittest.TestCase):
    """
    Test cases for the map_main function in leaflet_map.py. 
    Produced map of Buoy Sites and colors the selected location marker red.
    """

    # Test invalid buoy
    def test_map_main_invalid_buoy(self):
        """Tests that the map_main function raises a ValueError
            if an invalid buoy is selected."""
        with self.assertRaises(ValueError):
            selected_buoy = "Invalid_Buoy"
            leaflet_map_mod.map_main(selected_buoy)

    def test_map_main_valid_data(self):
        """Tests that the map_main function creates a map object with valid data."""
        selected_buoy = "Beach2_Buoy"
        buoy_map = leaflet_map_mod.map_main(selected_buoy)

        # Assert that the map object is not None
        self.assertIsNotNone(buoy_map)
