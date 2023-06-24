import csv


def save_dict_to_csv(data, filename):
    if not data:
        print("Data list is empty. Nothing to save.")
        return

    # Get the keys from the first dictionary to use as CSV headers
    headers = data[0].keys()

    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"CSV file '{filename}' has been created successfully.")
    except IOError:
        print(f"Error occurred while creating the CSV file '{filename}'.")
