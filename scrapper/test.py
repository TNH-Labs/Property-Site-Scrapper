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
list1 = ["Popular Industries", "Restaurants & Food", "Retail", "Service Businesses", "Wholesale & Distributors", "Transportation & Storage", "Online & Technology", "Automotive & Boat", "Franchise Opportunities", "All Industries"]
list2 = ["Office","Retail","Multifamily", "Industrial", "Mixed Use", "Hospitality", "Land", "Self Storage", "Mobile Home Park", "Senior Living", "Special Purpose", "Note/Loan"]
list3 = ["Office", "Industrial", "Retail", "Restaurant", "Shopping Center", "Multifamily", "Specialty", "Health Care", "Hospitality", "Sports & Entertainment", "Land", "Residential Income"]
list4 = ["Office","Retail","Multifamily", "Industrial", "Mixed Use", "Hospitality", "Land", "Self Storage", "Mobile Home Park", "Senior Living", "Special Purpose", "Note/Loan"]

# add all the lists and remove duplicates
list5 = list(set(list1 + list2))
print(list5)