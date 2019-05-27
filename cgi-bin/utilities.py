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

connection = connector.connect(**configHome)
cursor = connection.cursor(dictionary=True)

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

        ps = 'select *, product_name as name from WebShop_Products where type = %s AND subtype = %s AND gender = %s'
        cursor.execute(ps, (categories['type'], categories['subtype'], categories['gender']))
        result = cursor.fetchall()

    else:
        select = 'select * from WebShop_Products'
        cursor.execute(select)
        res = cursor.fetchall()
        result = res

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
    cursor.execute('select * from WebShop_Products')
    pre_pros_result = cursor.fetchall()

    end_res = []
    for row in pre_pros_result:
        brand_in_row = str(row['brand']).lower()
        brand_in_values = ' '.join(values).lower()

        if brand_in_row == brand_in_values:
            end_res.append(row)

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

    # Make the ids unique...
    ids = list(set(ids))

    result = []
    for item_id in ids:
        sql_order = 'select id, brand, type, subtype, color, gender, price, size, product_name as name from WebShop_Products where id = ' + get_name(
            item_id)
        cursor.execute(sql_order)
        row = cursor.fetchall()
        result.append(row[0])

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

    # cast dict to data frame to sustain current system.
    cursor.execute('select * from WebShop_Products')
    pre_pros_result = cursor.fetchall()
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

    # cast dict to data frame to sustain current system.
    cursor.execute('select * from WebShop_Products')
    pre_pros_result = cursor.fetchall()
    df = pd.DataFrame.from_dict(pre_pros_result)

    types = df[(df['gender'] == gender)
               & (df['type'] == category)]['subtype'].unique().tolist()
    children = [{'url': '', 'name': name} for name in types]
    result = [{'gender': gender, 'category': category, 'children': children}]

    return result


def insert_customer(first_name, last_name, email, address_id):
    sql_check = 'select * from WebShop_Customer where first_name = %s and last_name = %s'
    cursor.execute(sql_check, (first_name, last_name))
    res = cursor.fetchall()

    if len(res) == 1:
        return res[0]
    else:
        sql_order = 'insert into WebShop_Customer' \
                    ' (address_id, first_name, last_name, identifier, gender, mobile, email)' \
                    ' VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql_order, (address_id, first_name, last_name, None, None, None, email))
        connection.commit()
        return insert_customer(first_name, last_name, email, address_id)
        # insert a new customer


def insert_address(address, zipcode, town):
    sql_check = 'select * from WebShop_Address where first_line = %s and second_line = %s and third_line = %s'
    cursor.execute(sql_check, (address, zipcode, town))
    res = cursor.fetchall()

    if len(res) == 1:
        return res[0]
    else:
        sql_order = 'insert into WebShop_Address (first_line, second_line, third_line) VALUES (%s, %s, %s)'
        cursor.execute(sql_order, (address, zipcode, town))
        connection.commit()
        return insert_address(address, zipcode, town)


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
    try:
        firstname, lastname = order['name'].split()
    except Exception:
        firstname = order['name']
        lastname = ''
    email = order['email']
    address = order['address']
    zipcode = order['zipcode']
    town = order['town']

    item_ids = list(map(int, order['items'].strip('[]').split(',')))
    items = [
        {
            'id': int(x),
            'amount': item_ids.count(x)
        } for x in list(set(item_ids))
    ]

    # Grab or generate ids for customer and address, grab if they exist in our db,
    # else generate via inserting both address and customer.
    customer_address = insert_address(address, zipcode, town)
    customer = insert_customer(firstname, lastname, email, customer_address['address_id'])
    for item in items:
        # Add an order for each product purchased, i.e. if you bought 5 shirts, this will add 5 order inserts.
        for _ in range(item['amount']):
            sql_write_order = 'insert into WebShop_Orders (customer_id, product_id, date_time) VALUES (%s,%s, now());'
            cursor.execute(sql_write_order, (customer['customer_id'], item['id']))

        # always commit in when changing a db...
        connection.commit()


def get_name(name):
    """ Helper function to return a sql-queryable string...
    :param name: whatever string parseable type
    :return: 'name'.
    """
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
    test1 = get_products_filtered({'type': 'Shirts', 'subtype': 'T-shirt', 'gender': 'Female'})

    # test2 = get_products_filtered(None)
    # test4 = get_20_most_popular()

    # write_order_sql({'email': 'jesu17@student.bth.se', 'name': 'Jesper Sundius', 'address': 'Byggmästaregatan 5A',
    #                 'zipcode': '37140', 'town': 'Karlskrona',
    #                'items': '[777,1331,777,47842,1230,16543,8798,6656,6656]'})

    # test3 = get_subcategories('Male', 'Jackets')
    # test5 = get_products_search(['jack', 'and', 'jones'])
    # test6 = get_products_search(['wesc'])

    # test = get_products_ids([1, 2, 3, 4, 5, 6, 1, 2, 1])
    # test7 = get_categories()
    # test8 = get_20_most_popular()


if __name__ == '__main__':
    main()
