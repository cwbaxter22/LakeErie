import unittest
import pathlib
import importlib
import folium


codebase_path = pathlib.Path(__file__).parents[2]

#https://stackoverflow.com/questions/65206129/importlib-not-utilising-recognising-path
spec = importlib.util.spec_from_file_location(
    name='leaflet_map',  # name is not related to the file, it's the module name!
    location= str(codebase_path) + "//src//frontend//leaflet_map.py"  # full path to the script
)
leaflet_map_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(leaflet_map_mod)

class TestMapMainFunction(unittest.TestCase):

    def test_valid_selected_buoy(self):
        # Test with a valid selected buoy
        selected_buoy = "Buoy 3"
        result = leaflet_map_mod.map_main(selected_buoy)
        self.assertIsInstance(result, folium.Map)

    def test_invalid_selected_buoy(self):
        # Test with an invalid selected buoy
        selected_buoy = "Invalid Buoy"
        with self.assertRaises(ValueError) as context:
            leaflet_map_mod.map_main(selected_buoy)
        self.assertEqual(str(context.exception), "Invalid selected buoy 'Invalid Buoy'. Please select a valid buoy from the list.")

    def test_invalid_coordinates(self):
        # Test with invalid coordinates (non-numeric)
        buoy_locations = [
            {"name": "Invalid Buoy", "latitude": "invalid", "longitude": "invalid"}
        ]
        with self.assertRaises(ValueError) as context:
            leaflet_map_mod.map_main("Buoy 3")
        self.assertEqual(str(context.exception), "Invalid coordinates for buoy 'Invalid Buoy'. Latitude and longitude must be numeric.")
