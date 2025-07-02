import random

def generate_credit_card_numbers(num_cards):
    """
    Generates multiple credit card numbers that pass the Luhn algorithm,
    starting with either 4 or 5, and with 16 digits, along with a random expiry date and CVV code for each card.
    Returns:
        List of generated credit card numbers in the format "cards|month|year|cvv".
    """
    generated_cards = []
    prefixes = ["4", "5"]
    
    for _ in range(num_cards):
        # Choose a random prefix (either 4 or 5)
        prefix = random.choice(prefixes)
        
        # Generate the rest of the card number (13 digits)
        card_number = prefix + ''.join(str(random.randint(0, 9)) for _ in range(12))
        
        # Calculate the check digit using the Luhn algorithm
        checksum = 0
        for i, digit in enumerate(card_number):
            if i % 2 == 0:
                # Double every second digit from the right
                double_digit = int(digit) * 2
                if double_digit > 9:
                    # Subtract 9 from double-digit numbers greater than 9
                    double_digit -= 9
                checksum += double_digit
            else:
                # Add every other digit from the right
                checksum += int(digit)
        check_digit = (10 - (checksum % 10)) % 10
        
        # Append the check digit to the card number
        card_number += str(check_digit)
        
        # Add 2 random digits to make the card number 16 digits long
        card_number += ''.join(str(random.randint(0, 9)) for _ in range(2))
        
        # Generate a random expiry date
        expiry_month = random.randint(1, 12)
        expiry_year = random.randint(2022, 2027)
        
        # Generate a random CVV code
        cvv = ''.join(str(random.randint(0, 9)) for _ in range(3))
        
        # Append the generated card number, expiry date, and CVV code to the list
        generated_cards.append(f"{card_number}|{expiry_month:02d}|{expiry_year}|{cvv}")
    
    return generated_cards

# Example usage
num_cards = int(input("Enter number of cards to generate: "))
generated_cards = generate_credit_card_numbers(num_cards)
for card_info in generated_cards:
    print(card_info)
