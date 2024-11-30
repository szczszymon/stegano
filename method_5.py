import math
from itertools import permutations

def factorial(n):
    """Calculates factorial of n."""
    return math.factorial(n)

def lexicographical_order(sequence):
    """Generates lexicographical permutations of a sequence."""
    return sorted(permutations(sequence))

def embed(css_content, base_n_factorial_number):
    """
    Embeds a Base-(n!) number into the selectors of a CSS file.
    
    Args:
        css_content (list): List of CSS selectors (strings).
        base_n_factorial_number (int): Base-(n!) number to embed.0
    
    Returns:
        list: Modified selectors with embedded data.
    """
    n = len(css_content)
    selectors = sorted(css_content)
    rearranged_selectors = []
    
    remainder = base_n_factorial_number
    
    for i in range(n, 0, -1):
        fact = factorial(i - 1)
        index = remainder // fact
        rearranged_selectors.append(selectors.pop(index))
        remainder %= fact
    
    return rearranged_selectors

def extract(css_content):
    """
    Extracts a Base-(n!) number from the selectors of a CSS file.
    
    Args:
        css_content (list): List of lexicographically rearranged selectors.
    
    Returns:
        int: Extracted Base-(n!) number.
    """
    n = len(css_content)
    selectors = sorted(css_content)
    base_n_factorial_number = 0
    
    for i in range(n):
        current_selector = css_content[i]
        index = selectors.index(current_selector)
        base_n_factorial_number += index * factorial(n - i - 1)
        selectors.pop(index)
    
    return base_n_factorial_number

# Example Usage:
if __name__ == "__main__":
    # Original selectors in CSS
    original_selectors = ["header", "footer", "main", "aside"]

    # Message to embed: Base-(4!) number
    message = 23  # Example value

    # Embedding process
    embedded_selectors = embed(original_selectors, message)
    print("Selectors after embedding:", embedded_selectors)

    # Extraction process
    extracted_message = extract(embedded_selectors)
    print("Extracted Base-(n!) number:", extracted_message)
