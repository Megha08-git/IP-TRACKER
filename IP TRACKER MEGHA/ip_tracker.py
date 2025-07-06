# ip_tracker.py
import requests

def fetch_ip_details(ip_address):
    """
    Fetch details of the given IP address from ipinfo.io

    Args:
        ip_address (str): The IP address you want to fetch data for.
    
    Returns:
        dict or None: A dictionary containing IP details if successful, else None.
    """
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching IP details.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
