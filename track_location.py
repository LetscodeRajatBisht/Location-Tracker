import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium
import csv

def get_valid_phone_number():
    while True:
        try:
            # Get phone number input from the user
            number = input("Enter your phone number with country code: ")
            pepnumber = phonenumbers.parse(number)
            if not phonenumbers.is_valid_number(pepnumber):
                raise ValueError("Invalid phone number. Please enter a valid number.")
            return number
        except ValueError as e:
            print(f"Error: {e}")

def process_phone_number(number):
    pepnumber = phonenumbers.parse(number)
    location = geocoder.description_for_number(pepnumber, "en")
    print(location)

    service_pro = phonenumbers.parse(number)
    # Uncomment the following line if you want to print the carrier name
    # print(carrier.name_for_number(service_pro, "en"))

    key = 'd6997bc7a5ff4a0c958f86fdc6122387'

    geocoder_instance = OpenCageGeocode(key)
    query = str(location)
    results = geocoder_instance.geocode(query)

    lat = results[0]['geometry']['lat']
    lng = results[0]['geometry']['lng']

    print(f"Latitude: {lat}, Longitude: {lng}")

    myMap = folium.Map(location=[lat, lng], zoom_start=9)
    folium.Marker([lat, lng], popup=location).add_to(myMap)

    # Save the results in the dictionary
    return {
        'Location': location,
        'Latitude': lat,
        'Longitude': lng
    }, myMap

def main():
    # Create an empty dictionary to store results
    results_dict = {}

    while True:
        number = get_valid_phone_number()

        result, myMap = process_phone_number(number)
        results_dict[number] = result

        myMap.save(f"{number}_location.html")

        # Ask the user if they want to enter another phone number
        another_number = input("Do you want to enter another phone number? (yes/no): ")
        if another_number.lower() != 'yes':
            break

    # Save the results in a CSV file
    csv_file_path = 'phone_number_results.csv'
    with open(csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = ['Phone Number', 'Location', 'Latitude', 'Longitude']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the results
        for phone_number, result in results_dict.items():
            writer.writerow({
                'Phone Number': phone_number,
                'Location': result['Location'],
                'Latitude': result['Latitude'],
                'Longitude': result['Longitude']
            })

    print(f"Results have been saved to {csv_file_path}")

if __name__ == "__main__":
    main()
