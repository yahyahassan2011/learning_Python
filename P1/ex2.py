previous_number = 0

stop = int(input("Enter the stop number: "))

for i in range(1, stop+1):
    sum = previous_number + i
    print(f"Current Number {i} Previous Number {previous_number} Sum: {sum}")
    previous_number = i