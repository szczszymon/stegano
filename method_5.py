# method_5.py

import math
from itertools import permutations
import re


def parse_css(css_file_path):
    # Saving css file content as dict in format: selector: [declarations]
    css_rules = {}
    with open(css_file_path, 'r') as file:
        content = file.read()
        rules = re.findall(r'([^{]+)\{([^}]+)\}', content)  # Match selectors and declarations
        for selector, declarations in rules:
            selector = selector.strip()
            declarations = [decl.strip() for decl in declarations.split(';') if decl.strip()]
            css_rules[selector] = declarations
    return css_rules


def write_css(css_rules, output_file_path):
    # Saving dict of css rules as .css file
    with open(output_file_path, 'w') as file:
        for selector, declarations in css_rules.items():
            file.write(f"{selector} {{\n")
            for decl in declarations:
                file.write(f"    {decl};\n")
            file.write("}\n\n")


def embed_message(css_file_path, base_n_factorial_number, output_file_path):
    css_rules = parse_css(css_file_path)
    selectors = sorted(css_rules.keys())

    n = len(selectors)
    rearranged_selectors = []

    remainder = base_n_factorial_number

    # Embedding procedure
    for i in range(n, 0, -1):
        fact = math.factorial(i - 1)
        index = remainder // fact
        rearranged_selectors.append(selectors.pop(index))
        remainder %= fact

    # Rearrange the rules according to the new order
    new_rules = {selector: css_rules[selector] for selector in rearranged_selectors}
    write_css(new_rules, output_file_path)
    print(f"Embedding complete. Modified CSS saved to {output_file_path}")


def extract_message(css_file_path):
    css_rules = parse_css(css_file_path)
    selectors = sorted(css_rules.keys())
    current_order = list(css_rules.keys())

    n = len(selectors)
    base_n_factorial_number = 0

    # Extraction procedure
    for i in range(n):
        current_selector = current_order[i]
        index = selectors.index(current_selector)
        base_n_factorial_number += index * math.factorial(n - i - 1)
        selectors.pop(index)

    return base_n_factorial_number


input_css = "test.css"  # Path to your input CSS file
output_css = "output.css"  # Path to save modified CSS

message = int(input("Enter secret number: "))

embed_message(input_css, message, output_css)
extracted_message = extract_message(output_css)
print("Extracted Base-(n!) number:", extracted_message)
