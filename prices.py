import requests
import json

# Function to retrieve prices
def get_prices(api_key, service='', country=''):
    url = f"https://smshub.org/stubs/handler_api.php?api_key={api_key}&action=getPrices&service={service}&country={country}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data")
        return None
    
# Load country mappings from a file
with open('country_mappings.json', 'r') as file:
    country_names = json.load(file)

# Function to find the cheapest price in each country and sort them
def find_cheapest_and_sort(prices):
    cheapest_prices = {}
    for country, services in prices.items():
        for service, operators in services.items():
            for operator, price in operators.items():
                if country not in cheapest_prices or price < cheapest_prices[country][3]:
                    cheapest_prices[country] = (country, service, operator, price)
    return sorted(cheapest_prices.values(), key=lambda x: x[3])

# Function to save the sorted prices to a file
def save_to_file(sorted_prices, filename="sorted_prices.txt"):
    with open(filename, "w") as file:
        for price in sorted_prices:
            country_name = price[0] # This will be the ID, replace with actual name as needed
            file.write(f"{country_name}: {price}\n")

api_key = '182428U9a49b893a7c180be594c6fb876ac2703'  # Replace with your API key
service = 'bz'      # Replace with your desired service
country = ''              # Fetch all countries

prices = get_prices(api_key, service, country)
if prices:
    sorted_cheapest_prices = find_cheapest_and_sort(prices)
    save_to_file(sorted_cheapest_prices)
    print("Prices saved to sorted_prices.txt")
