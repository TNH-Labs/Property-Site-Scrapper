# import os
# import pandas as pd
#
# # Set the directory path where the CSV files are located
# directory = r"E:\CSV"
#
# # Create an empty DataFrame to store the merged data
# merged_data = pd.DataFrame()
#
# # Iterate over all files in the directory
# for filename in os.listdir(directory):
#     if filename.endswith(".csv"):
#         file_path = os.path.join(directory, filename)
#         # Read each CSV file into a DataFrame
#         data = pd.read_csv(file_path)
#
#         # Merge the data with the existing merged_data DataFrame
#         merged_data = pd.concat([merged_data, data])
#
# # Remove duplicate records based on the 'address' column
# merged_data = merged_data.drop_duplicates(subset=['address'])
#
# # Write the merged data to a new CSV file
# merged_data.to_csv("merged_data.csv", index=False)
#
# print("Data merging and deduplication completed!")
def find_matching_key(list1, list2):
    matching_key = None
    for key in list1:
        for element in list2:
            if key.lower() in element.lower():
                matching_key = key
                break
        if matching_key:
            break
    return matching_key

# Example usage
list1 = ["Office", "Retail", "Industrial", "Land", "Special Purpose", "Restaurant", "Retail Space"]
list2 = ['Land', 'Flex', 'Industrial and Warehouse Space', 'Retail Space', 'Special Purpose', 'Restaurants', 'Hotel and Motel', 'Events', 'Office', 'Agriculture', 'Multi-Family', 'Health Care', 'Restaurant', 'Mixed Use', 'Office Space', 'Medical', 'Medical Offices', 'Industrial', 'Flex Space', 'Coworking', 'Retail', 'Sports and Entertainment', 'Coworking Space', 'Senior Housing', 'All Spaces']

user_input = input("Enter a value: ")

matching_key = find_matching_key(list1, list2)

if matching_key:
    print(matching_key)
else:
    print(None)
