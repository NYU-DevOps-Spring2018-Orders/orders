Feature: The order microservices back-end
    As a API User
    I need a RESTful catalog service
    So that I can keep track of all orders

Background:
    Given the following orders
        | id | customer_id | date                          | status     |
        |  1 | 7           | Sun, 01 Apr 2018 12:59:00 GMT | processing |
        |  2 | 11          | Fri, 05 Jan 2018 12:59:00 GMT | processing |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: List all orders
    When I visit the "/orders"
    Then I should see "1" in the results
    And I should see "2" in the results
    And I should see "3" in the results

