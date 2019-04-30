Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | id | name       | category | available |
        |  1 | guess      | apparel  | True      |
        |  2 | reebok     | shoe     | True      |
        |  3 | ninewest   | handbag  | True      |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "nike"
    And I set the "Category" to "bag"
    And I press the "Create" button
    Then I should see the message "Success"

Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "guess" in the results
    And I should see "reebok" in the results
    And I should see "ninewest" in the results

Scenario: List all shoes
    When I visit the "Home Page"
    And I set the "Category" to "shoe"
    And I press the "Search" button
    Then I should see "reebok" in the results
    And I should not see "guess" in the results
    And I should not see "ninewest" in the results

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "guess" in the "name" field
    When I change "Name" to "gucci"
    And I press the "Update" button
    Then I should see the message "Success"
    When I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "gucci" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "gucci" in the results
    Then I should not see "guess" in the results

 Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "guess" in the "name" field
    When I set the "Id" to "1"
    And I press the "Delete" button
    Then I should no longer see "guess"
