import csv

#region \\OPEN CSV FILES//
def extract_data(csvfile):                            #read file into list of lists
    with open(csvfile, 'r',newline='') as file :
        csv_list = []
        contents = csv.reader(file)
        
        for item in contents :
            
            csv_list.append(item)
    
    keys = ['date_time','location','customer_name','order_list','order_total','payment_method','card_number']

    list_of_dicts = [dict(zip(keys, row)) for row in csv_list]          # Converts list of list into list of dicts
    
    return list_of_dicts


#endregion //OPEN CSV FILES\\

def transform_data (list_of_dicts):
    for row in list_of_dicts:                                       #loops over all dictionaries in list
        del row['card_number']                              #deletes card number and customer_name key-value pair
        del row['customer_name']

    og_key = 'date_time'
    date_key = 'date'
    time_key = 'time'

        
    for row in list_of_dicts:                                               # Splits date and time, row by row in the dict.
        if og_key in row:
            value = row[og_key]

            date, time = value.split(maxsplit=1)

            del row[og_key]

            row[date_key] = date

            row[time_key] = time
    
    products = []                                                       #initialise item list of dictionaries
    
    for row in list_of_dicts:
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


    for order in list_of_dicts:                                                     #loop over items and orders
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

        del order['order_list'] 

    for index, order in enumerate(list_of_dicts):
        order['order_id'] = index + 1


    junction_data = []
                                                                        #create list of tuples to store normalised data
    for order in list_of_dicts:
        ord_id = order['order_id']
        item_order_ids = order['item_ids']                              #store tuples connecting order and item IDs in list
        for item_num in item_order_ids:
            junction_data.append((ord_id, item_num))


    return list_of_dicts, products , junction_data