Feature: monadic evaluator
    Evaluate a formula using parser based on monad

    Scenario: evaluate a good formula
        Given we have a formula
        When we give it to the parser
        Then the parser should give us the answer

    Scenario: evaluate a bad formula
        Given we have a formula with a letter
        When we give it to the parser
        Then the parser should give us an error

    Scenario: evaluate a formula with a division by 0
        Given we have a formula with a division by 0
        When we give it to the parser
        Then the parser should give us an error division by 0
