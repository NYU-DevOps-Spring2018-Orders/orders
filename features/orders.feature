Feature: The order microservices back-end
    As a API User
    I need a RESTful catalog service
    So that I can keep track of all orders

Background:
    Given the following orders
        | id | customer_id | date             | status     | item_id | order_id | product_id | name  | quantity | price |
        |  1 | 72          | 2017-12-24T09:29 | returned   | 1       | 1        | 14         | cup   | 2        | 10.12 |
        |  2 | 11          | 2018-01-25T09:30 | processing | 1       | 2        | 7          | box   | 1        | 5.32  |

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
