import random
from datetime import date, timedelta
from tabulate import tabulate

def generate_credit_card_number(card_type):
    card_info = get_card_info(card_type)
    card_length = card_info['length']
    card_prefixes = card_info['prefixes']
    card_name = card_info['name']

    card_prefix = random.choice(card_prefixes)

    digits = [int(digit) for digit in card_prefix]
    digits += [random.randint(0, 9) for _ in range(card_length - len(card_prefix) - 1)]

    checksum = calculate_luhn_checksum(digits)

    digits.append(checksum)

    card_number = ''.join(map(str, digits))

    return card_number, card_name


def get_card_info(card_type):
    card_types = {
        'Visa': {
            'length': 16,
            'prefixes': ['4'],
            'cvc_length': 3,
            'name': 'Visa'
        },
        'MasterCard': {
            'length': 16,
            'prefixes': ['51', '52', '53', '54', '55'],
            'cvc_length': 3,
            'name': 'MasterCard'
        },
        'American Express': {
            'length': 15,
            'prefixes': ['34', '37'],
            'cvc_length': 4,
            'name': 'American Express'
        },
        'Discover': {
            'length': 16,
            'prefixes': ['6011'],
            'cvc_length': 3,
            'name': 'Discover'
        },
        'Diners Club': {
            'length': 14,
            'prefixes': ['300', '301', '302', '303', '304', '305', '36', '38'],
            'cvc_length': 3,
            'name': 'Diners Club'
        },
        'JCB': {
            'length': 16,
            'prefixes': ['35', '2131', '1800'],
            'cvc_length': 3,
            'name': 'JCB'
        }
    }

    if card_type not in card_types:
        raise ValueError('Invalid card type')

    return card_types[card_type]


def calculate_luhn_checksum(digits):
    doubled_digits = []

    for index, digit in enumerate(digits[::-1]):
        if index % 2 == 0:
            doubled_digits.append(2 * digit)
        else:
            doubled_digits.append(digit)

    summed_digits = [digit - 9 if digit > 9 else digit for digit in doubled_digits]

    total = sum(summed_digits)

    checksum = (total * 9) % 10

    return checksum


def generate_expiration_date():
    today = date.today()
    expiration_date = today + timedelta(days=random.randint(365, 1825))
    return expiration_date.strftime('%m/%y')


def generate_cvc(card_type):
    card_info = get_card_info(card_type)
    cvc_length = card_info['cvc_length']

    cvc = ''.join(str(random.randint(0, 9)) for _ in range(cvc_length))
    return cvc


def validate_credit_card_number(card_number):
    digits = [int(digit) for digit in str(card_number)]
    checksum = digits.pop()

    doubled_digits = [2 * digit if index % 2 == 0 else digit for index, digit in enumerate(digits[::-1])]

    summed_digits = [digit - 9 if digit > 9 else digit for digit in doubled_digits]

    total = sum(summed_digits)

    return (total + checksum) % 10 == 0


card_types = ['Visa', 'MasterCard', 'American Express', 'Discover', 'Diners Club', 'JCB']
num_cards_per_type = int(input("Enter the number of cards to generate per card type: "))

table = []

for card_type in card_types:
    rows = []

    for _ in range(num_cards_per_type):
        credit_card_number, card_name = generate_credit_card_number(card_type)
        expiration_date = generate_expiration_date()
        cvc = generate_cvc(card_type)
        is_valid = validate_credit_card_number(credit_card_number)

        rows.append([card_name, credit_card_number, expiration_date, cvc, is_valid])

    table.append([card_type, rows])

table_header = ['Card Type', 'Card Number', 'Expiration Date', 'CVC', 'Valid']

for card_table in table:
    card_type = card_table[0]
    rows = card_table[1]

    print(f"---- {card_type} ----")
    print(tabulate(rows, headers=table_header, tablefmt='grid'))
    print()
