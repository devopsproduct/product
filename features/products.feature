Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products

        | name       | category | available | price    |
        | guess      | apparel  | True      | 25.12    |
        | reebok     | shoe     | True      | 31.15    |
        | ninewest   | handbag  | False     | 100.12   |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Products Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "nike"
    And I set the "Category" to "bag"
    And I set the "Price" to "39.99"
    And I select "True" in the "Available" dropdown
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

 Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "guess"
    And I press the "Search" button
    Then I should see "guess" in the "name" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should not see "guess"

 Scenario: Update a Product: Unavailable Action
    When I visit the "Home Page"
    And I set the "Name" to "guess"
    And I press the "Search" button
    Then I should see "guess" in the "name" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    And I select "False" in the "Available" dropdown
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "False" in the "Available" dropdown
  
Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "guess"
    And I press the "Search" button
    Then I should see "guess" in the results
    When I copy line "1" and row "1"
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "False" in the "Available" dropdown