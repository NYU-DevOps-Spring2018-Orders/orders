# Orders Team for CSCI-GA.3033-013

[![Build Status](https://travis-ci.org/NYU-DevOps-Spring2018-Orders/orders.svg?branch=master)](https://travis-ci.org/NYU-DevOps-Spring2018-Orders/orders)
[![codecov](https://codecov.io/gh/NYU-DevOps-Spring2018-Orders/orders/branch/master/graph/badge.svg)](https://codecov.io/gh/NYU-DevOps-Spring2018-Orders/orders)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Our team handled the order process of a retail website.  Functions are built to create and update as needed both orders and items from a customer.


## Structure

-   Two classes have been set up - Order and Item.  An Item object represents an item from an associated order.  
-   Two paths
    - "http://localhost:5000/orders"
    - "http://localhost:5000/items"
-   Main REST API Functions
    - CREATE:  Creates an order by generating an Order object and Item objects for each item which is a part of the order
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
    
Then run the following command while running the VM...

    python server.py

Service will be listening on port 5000: http://localhost:5000/


## Testing

`nosetests` can be used after starting the VM and switching to the Vagrant directory.  This checks coverage on both `models.py` and `server.py`.  No argument needed regardless of Windows or MacOS

