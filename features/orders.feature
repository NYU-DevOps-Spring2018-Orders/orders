Feature: The order microservices back-end
    As a API User
    I need a RESTful catalog service
    So that I can keep track of all orders

Background:
    Given the following orders
        | id | customer_id | date             | status     |
        |  1 | 72          | 2017-12-24T09:29 | returned   |
        |  2 | 11          | 2018-01-25T09:30 | processing |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: List all orders
    When I visit the "/orders"
    Then I should see "72" in the results
    And I should see "returned" in the results