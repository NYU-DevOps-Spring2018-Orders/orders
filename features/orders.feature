Feature: The order microservices back-end
    As a API User
    I need a RESTful catalog service
    So that I can keep track of all orders

Background:
    Given the following orders
        | id | customer_id | date             | status     | item_id | order_id | product_id | name   | quantity | price   |
        |  1 | 72          | 2017-12-24T09:29 | returned   | 1       | 1        | 14         | cup    | 2        | 10.12   |
        |  2 | 11          | 2018-01-25T09:30 | processing | 1       | 2        | 7          | box    | 1        | 5.32    |
        |  3 | 14          | 2018-02-25T09:30 | processing | 1       | 3        | 71         | laptop | 1        | 999.32  |
        |  4 | 15          | 2018-02-27T09:30 | processing | 1       | 4        | 72         | laptop | 1        | 999.32  |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: List all orders
    When I visit the "Home Page"
    And I press the "list" order button
    Then I should see "72" in the order results
    And I should not see "kitty" in the order results

Scenario: List all items
    When I visit the "Home Page"
    And I press the "list" item button
    Then I should see "cup" in the item results
    And I should see "7" in the item results
    And I should not see "leo" in the item results

Scenario: Read an order
    When I visit the "Home Page"
    And I set the "order_id" to "2"
    And I press the "retrieve" order Button
    Then I should see "11" in the "order_customer_id" field
    Then I should see the message "Success"

Scenario: Read an item
    When I visit the "Home Page"
    And I set the "item_id" to "2"
    And I press the "retrieve" item Button
    Then I should see "7" in the "item_product_id" field
    Then I should see "box" in the "item_name" field
    Then I should see the message "Success"

Scenario: Delete an item
    When I visit the "Home Page"
    And I set the "item_id" to "1"
    And I press the "retrieve" item button
    And I press the "delete" item button
    Then I should see the message "Item has been Deleted!"

Scenario: Delete an order
    When I visit the "Home Page"
    And I set the "order_id" to "1"
    And I press the "delete" order button
    Then I should see the message "Order has been Deleted!"

Scenario: Update an item
    When I visit the "Home Page"
    And I set the "item_id" to "1"
    And I press the "Retrieve" item button
    Then I should see "2" in the "item_quantity" field
    When I change "item_quantity" to "3"
    And I press the "Update" item button
    Then I should see the message "Success"
    When I press the "Clear" item button
    When I set the "item_id" to "1"
    And I press the "Retrieve" item button
    Then I should see "3" in the "item_quantity" field

Scenario: Update an order
    When I visit the "Home Page"
    And I set the "order_id" to "1"
    And I press the "Retrieve" order button
    Then I should see "returned" in the "order_status" field
    When I change "order_status" to "shipped"
    And I press the "Update" order button
    Then I should see the message "Success"
    When I press the "Clear" order button
    When I set the "order_id" to "1"
    And I press the "Retrieve" order button
    Then I should see "shipped" in the "order_status" field

