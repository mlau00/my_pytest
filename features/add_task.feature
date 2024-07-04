Feature: Add a task
  Scenario: Successfully add a new task
    Given task payload
    When the client posts the payload to "/tasks/add"
    Then the response status code should be 200
    And the response should contain message "Task added"
