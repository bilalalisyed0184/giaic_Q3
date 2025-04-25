def print_one_digit(num):
    print("The one digit is", num % 10)

def main():
    num = int(input("Enter a number: "))
    print_one_digit(num)

if __name__ == "__main__":
    main()