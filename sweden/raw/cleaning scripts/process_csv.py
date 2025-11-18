import csv
import sys

# Read the raw CSV with proper encoding (using ISO-8859-1/Latin-1 for Swedish characters)
data = {}

with open('change_raw.csv', 'r', encoding='iso-8859-1') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header

    for row in reader:
        if len(row) < 3:
            continue

        region = row[0]
        year_month = row[1]
        population = int(row[2])

        # Extract kommun name (remove code prefix)
        # Format: "0114 Upplands Väsby" -> "Upplands Väsby"
        kommun_name = ' '.join(region.split()[1:])

        if kommun_name not in data:
            data[kommun_name] = {}

        # Extract year
        year = year_month[:4]
        data[kommun_name][year] = population

# Calculate changes and write output
with open('change_clean.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['kommun', 'change'])

    for kommun_name in sorted(data.keys()):
        if '2014' in data[kommun_name] and '2024' in data[kommun_name]:
            change = data[kommun_name]['2024'] - data[kommun_name]['2014']
            writer.writerow([kommun_name, change])

print("Processing complete! Created change_clean.csv")
print(f"Processed {len(data)} kommuner")
