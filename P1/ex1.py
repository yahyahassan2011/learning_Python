 
def multiply_or_sum(num1, num2):
    if num1 * num2 <= 1000:
        return num1 * num2
    else:
        return num1 + num2


while True:
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    print(multiply_or_sum(num1, num2))
    key = input("Press any key to continue and q to quit...")
    if key == "q":
        break


