#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inspect import currentframe, getfile
from os import path

import pandas as pd
from mysql import connector

databases = {
    'orders': 'WebShop_Orders',
    'products': 'WebShop_Products',
    'customers': 'WebShop_Customer',
    'addresses': 'WebShop_Address'
}

config = {
    'user': 'edca17',
    'password': 'uopdJPDnSiav',
    'host': 'blu-ray.student.bth.se',
    'database': 'edca17',
    'port': '3306',
    'raise_on_warnings': True,
    'use_unicode': True,
}

configHome = {
    'user': 'Edwin',
    'password': 'Edwin98',
    'host': 'localhost',
    'database': 'database-bth',
    'port': '8889',
    'raise_on_warnings': True,
    'use_unicode': True,
}

headers = ['brand', 'origin', 'type', 'subtype', 'color', 'gender', 'price', 'size', 'product_name', 'category',
           'weight', 'article_identifier']

connection = connector.connect(**configHome)
cursor = connection.cursor(dictionary=True)
cursor.execute('SELECT * FROM WebShop_Products')
pre_pros_result = cursor.fetchall()

cmd_folder = path.realpath(
    path.abspath(path.split(getfile(currentframe()))[0])) + '/'


def get_products_filtered(categories=None):
    """
    Indata
    Antingen skickas None in (pythons version av NULL) via categories och då
    skall alla produkter hämtas. Om categories inte är None, skickas en
    dictionary in med gender, type och subtype. Gender är plaggets målgrupps
    kön, type representerar huvudkategorin, subtype subkategorin.

    Returdata
    En lista av produkter. Respektive produkts information finns i en
    dictionary med följande nycklar:
    id: Det unika artikelnumret
    brand: Märket på produkten
    type: Typ av plagg, huvudkategori.
    subtype: Typ av plagg, subkategori
    color: Plaggets färg
    gender: Kön
    price: Priset på plagget
    size: Storleken på plagget

    Exempelvis:
    [{'id': 1, 'brand': 'WESC', 'type': 'Shirt, 'subtype': 'T-shirt',
       'color': 'Red', 'gender': 'Female', 'price': 299, 'size': 'M'},
    ...,
    {'id': 443, 'brand': 'Cheap Monday', 'type': 'Pants, 'subtype': 'Jeans',
     'color': 'Black', 'gender': 'Male', 'price': 449, 'size': 'S'}]
    """
    input_is_not_none = categories is not None

    if input_is_not_none:
        if categories['type'] is None or categories['subtype'] is None or categories['gender'] is None:
            raise RuntimeError('You need to specify the filtering dictionary.')

        ps = 'select * from WebShop_Products where type = %s AND subtype = %s AND gender = %s'
        cursor.execute(ps, (categories['type'], categories['subtype'], categories['gender']))
        result = cursor.fetchall()
    else:
        result = pre_pros_result

    if len(result) > 0:
        return result
    else:
        return None


def get_products_search(values):
    """
    Indata
    En lista (array) utav strängar (enskilda ord) som skall matchas mot märket
    på alla typer av produkter.

    Returdata
    En lista av produkter. Respektive produkts information finns i en
    dictionary med följande nycklar:

    id: Det unika artikelnumret
    brand: Märket på produkten
    type: Typ av plagg, huvudkategori.
    subtype: Typ av plagg, subkategori
    color: Plaggets färg
    gender: Kön
    price: Priset på plagget
    size: Storleken på plagget

    Exempelvis:
    [{'id': 1, 'brand': 'WESC', 'type': 'Shirt, 'subtype': 'T-shirt',
      'color': 'Red', 'gender': 'Female', 'price': 299, 'size': 'M'},
    ...,
    {'id': 443, 'brand': 'Cheap Monday', 'type': 'Pants, 'subtype': 'Jeans',
     'color': 'Black', 'gender': 'Male', 'price': 449, 'size': 'S'},
    ]
    """

    # end_res = {key: val for key, val in pre_pros_result.items() if val in values}

    # res = {key: val for el in pre_pros_result for key, val in pre_pros_result.items()}
    # print(res)
    # end_res = {}

    new_values = {}
    for i in range(len(values)):
        new_values[i] = values[i]

    # end_res = []
    # for row in pre_pros_result:
    #    for header in headers:
    #        row_brand = str(row[header]).split(" ")
    #        is_in_values = [x for x in row_brand if x in values]
    #        if len(is_in_values) > 0:
    #            end_res.append(row)

    end_res = []
    for row in pre_pros_result:
        brand_in_row = str(row['brand']).lower()
        brand_in_values = ' '.join(values)

        if brand_in_row == brand_in_values:
            end_res.append(row)

    #  for row in pre_pros_result:
    #     print(row['id'])
    #    for value in new_values:
    #       if any(row[header] is value for header in headers):
    #          pass
    #     else:
    #        end_res.append(row)

    return end_res


def get_products_ids(ids):
    """
    Indata
    En lista (array) av heltal som representerar artikelnummer på produkter.

    Returdata
    En lista av produkter. Respektive produkts information finns i en
    dictionary med följande nycklar:

    id: Det unika artikelnumret
    brand: Märket på produkten
    type: Typ av plagg, huvudkategori.
    subtype: Typ av plagg, subkategori
    color: Plaggets färg
    gender: Kön
    price: Priset på plagget
    size: Storleken på plagget

    Exempelvis:
    [{'id': 1, 'brand': 'WESC', 'type': 'Shirt, 'subtype': 'T-shirt',
      'color': 'Red', 'gender': 'Female', 'price': 299, 'size': 'M'},
    ...,
    {'id': 443, 'brand': 'Cheap Monday', 'type': 'Pants, 'subtype': 'Jeans',
     'color': 'Black', 'gender': 'Male', 'price': 449, 'size': 'S'}]
    """
    result = []
    for item_id in ids:
        sql_order = 'select id, brand, type, subtype, color, gender, price, size ' \
                    ' from WebShop_Products where id = ' + str(item_id) + ';'
        cursor.execute(sql_order)
        row = cursor.fetchall()
        result.append(row)

    return result


def get_categories():
    """
    Returdata
    En lista innehållande dictionaries med nycklarna title och children.
    title representerar könet plaggen är gjorda för (t.ex. Dam och Herr).
    children skall hålla en lista utav ytterligare dictionary object, där
    varje dictionary innehåller nycklarna url och name.
    url tilldelar ni en tom sträng (d.v.s. '') och nyckeln name tilldelar
    ni en huvudkategori.

    Exempelvis:
    [{'title': 'Dam', 'children': [{'url': '', 'name': 'Tröjor'},
                                   {'url': '', 'name': 'Byxor'}]},
    {'title': 'Herr', 'children': [{'url': '', 'name': 'Tröjor'},
                                   {'url': '', 'name': 'Väskor'}]}]
    """

    df = pd.DataFrame.from_dict(pre_pros_result)

    genders = df['gender'].unique()
    types = [
        df[(df['gender'] == genders[0])]['type'].unique().tolist(),
        df[(df['gender'] == genders[1])]['type'].unique().tolist(),
    ]

    children = \
        [
            [
                {
                    'url': '',
                    'name': name
                } for name in types[0]],
            [
                {
                    'url': '',
                    'name': name
                } for name in types[1]
            ]
        ]
    ''' SQL '''

    result = [{
        'title': genders[0],
        'children': children[0]
    }, {
        'title': genders[1],
        'children': children[1]
    }]
    return result


def get_subcategories(gender, category):
    """
    Indata
    Två strängar, gender och category, där gender är könet som det efterfrågas
    kläder för och category är huvudkategorin vars subkategorier vi vill hämta.

    Returdata
    En lista innahållande dictionaries med nycklarna gender, category, och
    children. gender representerar könet plaggen är gjorda för (t.ex. Dam och
    Herr). category är den inkommande kategorin vi hämtar subkategorier för
    children skall hålla en lista utav ytterligare dictionary object, där
    varje dictionary
    innehåller nycklarna url och name.
    url tilldelar ni en tom sträng (d.v.s. '') och nyckeln name tilldelar ni en
    subkategori.

    Exempelvis:
    [{'gender': 'Dam', 'category': 'Tröjor', 'children':
        [{'url': '', 'name': 'T-shirts'}, {'url': '', 'name': 'Linnen'}]}]
    """

    df = pd.DataFrame.from_dict(pre_pros_result)

    types = df[(df['gender'] == gender)
               & (df['type'] == category)]['subtype'].unique().tolist()
    children = [{'url': '', 'name': name} for name in types]
    result = [{'gender': gender, 'category': category, 'children': children}]
    ''' SQL '''

    return result


def write_order_sql(order):
    """
    Indata
    order som är en dictionary med nycklarna och dess motsvarande värden:
    town: Kundens stad
    name: Kundens namn
    zipcode: Kundens postkod
    address: Kundens address
    email: Kundens email
    items: En lista av heltal som representerar alla produkters artikelnummer.
        Så många gånger ett heltal finns i listan, så många artiklar av den
        typen har kunden köpt. Exempelvis: [1,2,2,3]. I den listan har kunden
        köpt 1 styck av produkt 1, 2 styck av produkt 2, och 1 styck av
        produkt 3.
    """
    sql_order = 'select * from salesforcustomer where concat(first_name,\' \',last_name) = %s or first_name = %s'
    print(sql_order)

    cursor.execute(sql_order, (get_name(order['name']), get_name(order['name'])))
    final_res = cursor.fetchall()
    print()

    try:
        firstname, lastname = order['name'].split()
    except Exception:
        firstname = order['name']
        lastname = ''
    email = order['email']
    address = order['address']
    zipcode = order['zipcode']
    town = order['town']


def write_order(order):
    """
    Indata
    order som är en dictionary med nycklarna och dess motsvarande värden:
    town: Kundens stad
    name: Kundens namn
    zipcode: Kundens postkod
    address: Kundens address
    email: Kundens email
    items: En lista av heltal som representerar alla produkters artikelnummer.
        Så många gånger ett heltal finns i listan, så många artiklar av den
        typen har kunden köpt. Exempelvis: [1,2,2,3]. I den listan har kunden
        köpt 1 styck av produkt 1, 2 styck av produkt 2, och 1 styck av
        produkt 3.
    """
    df_orders = pd.read_csv(cmd_folder + 'data/Orders.csv')
    # Get new order ID
    orderID = df_orders['orderid'].max() + 1
    print(orderID)
    # Grab the products id number and the amount of each product
    item_ids = list(map(int, order['items'].strip('[]').split(',')))
    items = [{
        'id': int(x),
        'amount': item_ids.count(x)
    } for x in list(set(item_ids))]

    # Get the name and so on for the customer.
    try:
        firstname, lastname = order['name'].split()
    except Exception:
        firstname = order['name']
        lastname = ''
    email = order['email']
    address = order['address']
    zipcode = order['zipcode']
    town = order['town']

    # Write the actual order
    df_products = pd.read_csv(cmd_folder + 'data/Products.csv')
    for item in items:
        product = df_products[df_products['id'] == item['id']].to_dict(
            'records')[0]
        df_orders.loc[len(df_orders)] = [
            orderID, firstname, lastname, address, town, zipcode,
            product['id'], product['brand'], product['type'],
            product['subtype'], product['color'], product['gender'],
            product['price'], product['size'], item['amount']
        ]
    df_orders.to_csv('data/Orders.csv', index=False, encoding='utf-8')


def get_name(name):
    return '\'' + str(name) + '\''


def get_20_most_popular():
    """
    Returdata
    En lista av de 20 produkter som är mest sålda i webshopen.
    Respektive produkts information finns i en dictionary med följande nycklar:
    id: Det unika artikelnumret
    brand: Märket på produkten
    type: Typ av plagg, huvudkategori.
    subtype: Typ av plagg, subkategori
    color: Plaggets färg
    gender: Kön
    price: Priset på plagget
    size: Storleken på plagget

    Exempelvis:
    [{'id': 1, 'brand': 'WESC', 'type': 'Shirt, 'subtype': 'T-shirt',
      'color': 'Red', 'gender': 'Female', 'price': 299, 'size': 'M'},
    ...,
    {'id': 443, 'brand': 'Cheap Monday', 'type': 'Pants,
     'subtype': 'Jeans', 'color': 'Black', 'gender': 'Male', 'price': 449,
     'size': 'S'}]
    """

    ps = 'SELECT * FROM best20Sellers limit 20'
    cursor.execute(ps)
    res = cursor.fetchall()

    return res


def main():
    # test1 = get_products_filtered({'type': 'Shirts', 'subtype': 'T-shirt', 'gender': 'Female'})
    # test2 = get_products_filtered(None)
    # test3 = get_products_search() FUNKAR EJ
    # test4 = get_20_most_popular()

    write_order_sql({'email': 'edca17@student.bth.se', 'name': 'Martino Baldcock', 'address': 'Utridarevägen 5A',
                     'zipcode': '37140', 'town': 'Karlskrona', 'items': '[777]'})

    # test = get_subcategories('Male', 'Jackets')
    # test = get_products_search(['jack', 'and', 'jones'])
    # test = get_products_search(['wesc'])

    # test = get_categories()
    # test = get_20_most_popular()


if __name__ == '__main__':
    main()
