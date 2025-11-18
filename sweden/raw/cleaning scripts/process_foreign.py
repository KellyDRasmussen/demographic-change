import csv

# Read the raw CSV with proper encoding (using ISO-8859-1/Latin-1 for Swedish characters)
data = {}

with open('change_foreign.csv', 'r', encoding='iso-8859-1') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header

    for row in reader:
        if len(row) < 5:
            continue

        region = row[0]
        background = row[1]
        age = row[2]
        year = row[3]
        count = int(row[4])

        # Extract kommun name (remove code prefix)
        # Format: "0114 Upplands Väsby" -> "Upplands Väsby"
        kommun_name = ' '.join(region.split()[1:])

        if kommun_name not in data:
            data[kommun_name] = {}

        data[kommun_name][year] = count

# Calculate changes and write output
with open('change_foreign_clean.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['kommun', 'change'])

    for kommun_name in sorted(data.keys()):
        if '2014' in data[kommun_name] and '2024' in data[kommun_name]:
            change = data[kommun_name]['2024'] - data[kommun_name]['2014']
            writer.writerow([kommun_name, change])

print("Processing complete! Created change_foreign_clean.csv")
print(f"Processed {len(data)} kommuner")
