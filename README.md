# Orders Team for CSCI-GA.3033-013

[![Build Status](https://travis-ci.org/NYU-DevOps-Spring2018-Orders/orders.svg?branch=master)](https://travis-ci.org/NYU-DevOps-Spring2018-Orders/orders)
[![codecov](https://codecov.io/gh/NYU-DevOps-Spring2018-Orders/orders/branch/master/graph/badge.svg)](https://codecov.io/gh/NYU-DevOps-Spring2018-Orders/orders)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Our team handled the order process of a retail website.  Functions are built to create and update as needed both orders and items from a customer.


## Structure

-   Two classes Order and Item.  An Item object represents an item from an associated order.
    - Order: id (auto generated), customer_id, status, date
    - Item: id (auto generated), product_id, order_id, name, quantity, price
-   Status has 3 states - processing (initial state), cancelled, shipped
-   Two tables - Orders and Items
    - Order table does not include any detail of the items in the order.  ID auto generated
    - Item table has a unique ID that is auto generated as well.  Each Item has a Product ID and Order ID (foreign key) associated with it.
-   Two paths
    - "http://localhost:5000/orders"
    - "http://localhost:5000/items"
-   Main REST API Functions
    - CREATE:  Creates an order by generating an Order object and Item objects for each item which is a part of the orders
    - GET:  Get an order or get an item
    - UPDATE:  Updates an order based on the differences sent in the JSON
    - LIST:  List items from an order, list all orders or list all items
    - QUERY:  Find orders and items based on the fields in their respective tables
    - ACTION:  Cancels an order by changing the status of the order
    - DELETE:  Delete an order or delete an item from an order

## Prerequisites

This component of the website levarages VirtualBox and Vagrant to standardize environments.  If you do not have either of theses installed, please download the apps from the following links...

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)


## Starting the Service

After the required software is installed, you can start up the orders service by following these steps...

    git clone https://github.com/NYU-DevOps-Spring2018-Orders/orders.git
    cd orders
    vagrant up
    vagrant ssh
    cd /vagrant
    export DATABASE_URI='mysql+pymysql://root:passw0rd@localhost:3306/test'

Then run the following command while running the VM...

    python server.py

Service will be listening on port 5000: http://localhost:5000/

Note there is a test json with the expected fields for the service...

    orders/tests/test.json

## REST API Functions

-  CREATE - takes the JSON and creates the order and item details for their respective tables
   - `POST http://localhost:5000/orders`
-  GET - Gets the details of a specific order
   - `GET http://localhost:5000/orders/{id}`  
-  GET - Get details of a specific item:
   - `GET http://localhost:5000/items/{id}`
-  LIST - All orders in the system:
   - `GET http://localhost:5000/orders`
-  LIST - All items in the system:
   - `GET http://localhost:5000/items`
-  LIST - Items from a specified order:
   - `GET http://localhost:5000/orders/{id}/items`
-  DELETE - deletes an order and its items:
   - `DELETE http://localhost:5000/orders/{id}`
-  DELETE - deletes an item from an order:
   - `DELETE http://localhost:5000/orders/{id}/items/{id}`
-  ACTION - cancel an order:
   - `PUT http://localhost:5000/orders/{id}/cancel`
-  PUT - update an order:
   - `PUT http://localhost:5000/orders/{id}`
-  PUT - update an item:
   - `PUT http://localhost:5000/item/{id}`
-  QUERY - query for a list of orders based on field:
   - `GET http://localhost:5000/orders?<field>=<value>`
-  QUERY - query for a list of items based on field:
   - `GET http://localhost:5000/items?<field>=<value>`


## Testing

`nosetests` can be used after starting the VM and switching to the Vagrant directory.  This checks coverage on both `models.py` and `server.py`.  No argument needed regardless of Windows or MacOS
