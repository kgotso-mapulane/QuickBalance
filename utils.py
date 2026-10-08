import json  # json is a built-in Python module - no need to install it
import os    # os lets us work with file paths in a cross-platform way


def load_data():
    """
    Reads the mock_data.json file and returns the full data as a Python dictionary.
    """
    # Build the path to the JSON file relative to this script's location.
    # os.path.dirname(__file__) gives us the folder where utils.py lives.
    # os.path.join then adds the rest of the path - works on Windows and Mac/Linux.
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "data", "mock_data.json")

    # Open the file and parse it from JSON text into a Python dictionary
    with open(data_path, "r") as file:
        data = json.load(file)  # json.load reads the file and converts it to a dict

    return data  # Return the whole dictionary so we can use it elsewhere


def find_customer(customer_id, data):
    """
    Searches the list of customers for one matching the given customer_id.
    Returns the customer dictionary if found, or None if not found.
    """
    # data["customers"] gives us the list of customer dicts from the JSON
    for customer in data["customers"]:
        # Compare in uppercase so login is not case-sensitive (cust001 == CUST001)
        if customer["customer_id"].upper() == customer_id.strip().upper():
            return customer  # Found a match - return the customer dict immediately

    return None  # No match found after checking all customers
