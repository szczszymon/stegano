from PyPDF2 import PdfWriter, PdfReader
from PyPDF2.generic import NumberObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import random


def create_text_pdf(text, output_filename):
    # Create a PDF with a single page containing the given text
    c = canvas.Canvas(output_filename, pagesize=letter)
    c.drawString(100, 750, text)
    c.save()


def embed(files):
    cover_files = files.split(",")

    # Cover files segmentation and sanitazation
    for i in range(len(cover_files)):
        cover_files[i] = cover_files[i].strip()

    
    secret = input("Enter the secret text: ")

    secret_ascii = []
    last_share = []

    for char in secret:
        secret_ascii.append(ord(char))
        last_share.append(ord(char))

    shares = []

    for i in range(len(cover_files) - 1):
        shares.append([])
        for j in range(len(secret_ascii)):
            shares[i].append(random.randrange(0, 255))
            last_share[j] = last_share[j] ^ shares[i][j]

    shares.append(last_share)

    # Shares creation is finished
    # Last_share is appended to the end of shares
    # Decoding is done by opeartion: Last share XOR share[i] n - 1 times where n is the lenth of shares list
    # TODO:
    # Modify current method_4 for singular page hiding to embed 1 share per file
    # Add extraction func that: reads shares hidden in pdf files and saves to the list then decodes the message by operation mentioned above
    return None

    # Create a new PDF with the secret
    secret_pdf_path = "secret.pdf"
    create_text_pdf(secret, secret_pdf_path)

    cover_reader = PdfReader(cover_pdf_path)

    # Merge the cover and secret PDF - intermediate.pdf
    secret_reader = PdfReader(secret_pdf_path)
    writer = PdfWriter()

    for page in cover_reader.pages:
        writer.add_page(page)
    writer.add_page(secret_reader.pages[0])

    # Write intermediate file to visualize the change
    intermediate_output = "intermediate.pdf"
    with open(intermediate_output, "wb") as f:
        writer.write(f)

    # Page count modification
    pages_dict = writer._root_object["/Pages"]
    current_count = pages_dict["/Count"]
    new_count = NumberObject(current_count - 1)
    pages_dict.update({"/Count": new_count})

    # Write the final stego PDF
    output_pdf_path = "Stego_method4.pdf"
    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    print(f"Stego PDF file created successfully: {output_pdf_path}")


def extract(stego_file):
    return None
    reader = PdfReader(stego_file)

    total_pages = len(reader.pages)  # Includes the hidden page
    visible_pages = reader.trailer["/Root"]["/Pages"]["/Count"]  # Visible page count

    if total_pages > visible_pages:
        hidden_page_index = total_pages - 1
        hidden_page = reader.pages[hidden_page_index]
        secret_text = hidden_page.extract_text()

        return secret_text
    else:
        print("No hidden page detected in the PDF.")
        return None


embed("ref.pdf, przebieg.pdf")
print(f"Extracted secret: {extract("Stego_method4.pdf")}")
