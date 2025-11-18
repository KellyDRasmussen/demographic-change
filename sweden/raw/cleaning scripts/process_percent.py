import csv

# Read the raw CSV with proper encoding
data = {}

with open('foreigner_percent.csv', 'r', encoding='iso-8859-1') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header

    for row in reader:
        if len(row) < 5:
            continue

        age = row[0]
        region = row[1]
        background = row[2]
        year = row[3]
        percent = float(row[4])

        # Extract kommun name (remove code prefix)
        # Format: "0114 Upplands Väsby" -> "Upplands Väsby"
        kommun_name = ' '.join(region.split()[1:])

        data[kommun_name] = percent

# Write output
with open('foreigner_percent_clean.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['kommun', 'percent'])

    for kommun_name in sorted(data.keys()):
        writer.writerow([kommun_name, data[kommun_name]])

print("Processing complete! Created foreigner_percent_clean.csv")
print(f"Processed {len(data)} kommuner")
