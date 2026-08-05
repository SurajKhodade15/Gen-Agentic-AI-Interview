def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

def multiply_numbers(a, b):
    return a * b

def divide_numbers(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b

def calculator(a, b, operation):
    if operation == 'add':
        return add_numbers(a, b)
    elif operation == 'subtract':
        return subtract_numbers(a, b)
    elif operation == 'multiply':
        return multiply_numbers(a, b)
    elif operation == 'divide':
        return divide_numbers(a, b)
    else:
        return "Error: Invalid operation. Please choose from 'add', 'subtract', 'multiply', or 'divide'."
    

# This code defines a simple calculator that can perform addition, subtraction, multiplication, and division.
# It includes error handling for division by zero and invalid operations.
# The calculator function takes two numbers and an operation as input and returns the result of the operation.
# The example usage demonstrates how to use the calculator function with different operations.
# The code is structured to be easily extendable for additional operations if needed.
# The main block allows the script to be run directly, providing a simple interface for testing the
# calculator functionality.
# The code is designed to be clear and easy to understand, making it suitable for beginners learning Python.

## Using lambda functions for the same calculator functionality
def add_numbers_lambda(a, b):
    return (lambda x, y: x + y)(a, b)

def subtract_numbers_lambda(a, b):
    return (lambda x, y: x - y)(a, b)

def multiply_numbers_lambda(a, b):
    return (lambda x, y: x * y)(a, b)

def divide_numbers_lambda(a, b):
    return (lambda x, y: "Error: Division by zero is not allowed." if y == 0 else x / y)(a, b)

def calculator_lambda(a, b, operation):
    if operation == 'add':
        return add_numbers_lambda(a, b)
    elif operation == 'subtract':
        return subtract_numbers_lambda(a, b)
    elif operation == 'multiply':
        return multiply_numbers_lambda(a, b)
    elif operation == 'divide':
        return divide_numbers_lambda(a, b)
    else:
        return "Error: Invalid operation. Please choose from 'add', 'subtract', 'multiply', or 'divide'."
    
    
# Example usage:
if __name__ == "__main__":
    a = int(input("Enter the first number: "))
    b = int(input("Enter the second number: "))
    operation = input("Enter the operation (add, subtract, multiply, divide): ").strip().lower()
    result = calculator(a, b, operation)
    print(f"The result of {operation}ing {a} and {b} is: {result} using functions")
    

    result = calculator_lambda(a, b, operation)
    print(f"The result of {operation}ing {a} and {b} is: {result} using lambda functions")
