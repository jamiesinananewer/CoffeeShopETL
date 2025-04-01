import csv
import psycopg2

def open_files(csvfile):
    with open(csvfile, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)  # Read all rows into a list
    return data

def add_headers_and_write(csvfile, data, fieldnames):
    with open(csvfile, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write headers
        writer.writeheader()
        
        # Write rows
        for row in data:
            writer.writerow({
                fieldnames[i]: row[i] for i in range(len(fieldnames))
            })

# Example usage
csv_file = '/Users/Iacopoalessandropedde/Desktop/python/La-Vida-Mocha/leeds_09-05-2023_09-00-00.csv'
fieldnames = ['date_time', 'location', 'customer_name', 'order_list', 'order_total', 'payment_method', 'card_number']

# Read data from CSV without headers
data_without_headers = open_files(csv_file)

# Add headers and write back to CSV
add_headers_and_write(csv_file, data_without_headers, fieldnames)
      