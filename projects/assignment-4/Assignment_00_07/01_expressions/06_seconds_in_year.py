DAYS_IN_YEAR = 365
HOURS_IN_DAY = 24
MIN_PER_HOUR = 60
SEC_PER_MIN = 60

def main():

    total_seconds = DAYS_IN_YEAR * HOURS_IN_DAY * MIN_PER_HOUR * SEC_PER_MIN

    print(f"there are {total_seconds} seconds in a year")

if __name__ == "__main__":
    main()
