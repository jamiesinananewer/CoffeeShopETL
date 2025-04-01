import csv
import psycopg2
from functions import *

#region \\MAIN// This is the main script for the application
def main():
    

    
    
    leeds = open_files('leeds_09-05-2023_09-00-00.csv')     #opens the file
    print(leeds)
        

    for row in leeds:                                       #loops over all dictionaries in list
        del row['card_number']                              #deletes card number and customer_name key-value pair
        del row['customer_name']

    

    og_key = 'date_time'
    date_key = 'date'
    time_key = 'time'

        
    for row in leeds:                                               # Splits date and time, row by row in the dict.
        if og_key in row:
            value = row[og_key]

            date, time = value.split(maxsplit=1)

            del row[og_key]

            row[date_key] = date

            row[time_key] = time

    products = []                                                       #initialise item list of dictionaries
    
    for row in leeds:
        order_list = row['order_list']

        items = [item.strip() for item in order_list.split(',')]            #split different items in order

        for item in items:
            item_name, item_price = item.rsplit(' - ', 1)                   #split item name and price from item
            item_name = item_name.strip()
            item_price = float(item_price.strip())

            new_item = {                                                    #create item dictionary
                    'item_name' : item_name,
                    'item_price' : item_price
                }
            
            if new_item not in products:                                #add item to list of dictionaries if not already there
                products.append(new_item)
        
    for index, item in enumerate(products):                             #give items in list unique id
        item['item_id'] = index + 1            
    
    for order in leeds:                                                     #loop over items and orders
        order_id_list = []
        
        for item in products:
            price_len = len(str(item['item_price']))

            match price_len:                                            #create reference to see if item is in order
                    case 3:
                        ref_string = item['item_name'] + ' - ' + str(item['item_price']) + '0'      #if 1d.p., add 0 to price
                    case 4:
                        ref_string = item['item_name'] + ' - ' + str(item['item_price'])            #if 2d.p, don't add 0 to price
                    case _:
                        print("ERROR IN price_len")

            order_list = order['order_list']       
            
            if ref_string in order_list.split(', '):                     #create list of item ids corresponding to items in order
                order_id_list.append(item['item_id'])
                   
            order['item_ids'] = order_id_list                            #add key-value pair to orders with item ids

        del order['order_list']                                          #remove original order list
    
    for index, order in enumerate(leeds):
        order['order_id'] = index + 1
    
    print(leeds[4]) #{'location': 'Leeds', 'order_total': '4.4', 'payment_method': 'CASH', 'date': '09/05/2023', 'time': '09:06', 'item_ids': [7, 8, 9], 'order_id': 5}

    junction_data = []
                                                                        #create list of tuples to store normalised data
    for order in leeds:
        ord_id = order['order_id']
        item_order_ids = order['item_ids']                              #store tuples connecting order and item IDs in list
        for item_num in item_order_ids:
            junction_data.append((ord_id, item_num))

    print(junction_data)
    
    
    db_params = {                                                       #define parameters for connection to PostgreSQL
    "host": "localhost",
    "database": "livindb",
    "user": "admin",
    "password": "password",
    "port": "5432"
    }

    with psycopg2.connect(**db_params) as connection:                   #connect to PostgreSQL 
        
        cursor = connection.cursor()                                    #establish cursor to run sql commands

                                                                        #create orders table
        create_orders = '''                                             
            CREATE TABLE orders (
            order_id SERIAL PRIMARY KEY,
            order_location VARCHAR(255) NOT NULL,
            order_total FLOAT NOT NULL,
            order_payment_method VARCHAR(255) NOT NULL,
            order_date VARCHAR(255) NOT NULL,
            order_time VARCHAR(255) NOT NULL
            )
            '''
                                                                        #create items table     
        create_items = '''
            
            CREATE TABLE items (
            item_id SERIAL PRIMARY KEY,
            item_name VARCHAR(255) NOT NULL,
            item_price FLOAT NOT NULL
            )
        
        '''
                                                                        #create junction table for normalisation
        create_junction = '''
            CREATE TABLE order_item_junction (
            order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
            item_id INT REFERENCES items(item_id) ON DELETE CASCADE,
            CONSTRAINT orders_items_pk PRIMARY KEY (order_id, item_id)
            )

        '''
        
        cursor.execute('DROP TABLE IF EXISTS orders CASCADE')           #make sure tables are dropped before being rewritten 
        cursor.execute('DROP TABLE IF EXISTS items CASCADE')
        cursor.execute('DROP TABLE IF EXISTS order_item_junction')
        cursor.execute(create_orders)                                   #execute creation of data tables
        cursor.execute(create_items)
        cursor.execute(create_junction)
        
        
                                                                        #save leeds list to orders table
        order_fill = '''
            INSERT INTO orders (order_id, order_location, order_total, order_payment_method, order_date, order_time)
            VALUES (%s,%s,%s,%s,%s,%s)

        '''
        for order in leeds:                                             #fill orders table with orders from leeds dictionary in correct order
            
            order_data = (order['order_id'], order['location'], order['order_total'], order['payment_method'], order['date'], order['time'])
            cursor.execute(order_fill, order_data)

                                                                        #save products list to items table
        item_fill = '''
            INSERT INTO items (item_id, item_name, item_price)
            VALUES (%s, %s, %s)

        '''
        for item in products:                                       #fill items table with items from unique items list in correct order
            
            item_data = (item['item_id'], item['item_name'], item['item_price'])
            cursor.execute(item_fill, item_data)

                                                                        #save normalised data to junction table
        junction_fill = '''
            INSERT INTO order_item_junction (order_id, item_id)
            VALUES (%s, %s)

        '''
        for junc in junction_data:                                      #fill junction table with junction_data list linking orders to items
            cursor.execute(junction_fill, junc)

        
        
        
        connection.commit()                                             #commit changes to databse and close cursor (connection closes automatically)
        cursor.close()








    print("this is the main function")
#endregion //MAIN\\

main()