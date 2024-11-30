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

    # Shares creation
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

    # Shares preparation for embedding (2-D list to strings)
    shares_txt = []

    for share in shares:
        txt = ""
        for item in share:
            txt += f"{item} "
        shares_txt.append(txt)

    # Embedding shares data into cover files
    if len(cover_files) == 1:
        cover = cover_files[0]
        secret_path = f"secret-{1}.pdf"
        create_text_pdf(shares_txt[0], secret_path)

        cover_reader = PdfReader(cover)

        secret_reader = PdfReader(secret_path)
        writer = PdfWriter()

        for page in cover_reader.pages:
            writer.add_page(page)
        writer.add_page(secret_reader.pages[0])

        intermediate_output = f"intermediate-{1}.pdf"
        with open(intermediate_output, "wb") as f:
            writer.write(f)

        pages_dict = writer._root_object["/Pages"]
        current_count = pages_dict["/Count"]
        new_count = NumberObject(current_count - 1)
        pages_dict.update({"/Count": new_count})

        output_pdf_path = f"Stego_method4-{1}.pdf"
        with open(output_pdf_path, "wb") as f:
            writer.write(f)

        print(f"Stego PDF file created successfully: {output_pdf_path}")

    else:
        for cover, i in zip(cover_files, range(1, len(cover_files) + 1)):
            secret_path = f"secret-{i}.pdf"
            create_text_pdf(shares_txt[i - 1], secret_path)

            cover_reader = PdfReader(cover)

            secret_reader = PdfReader(secret_path)
            writer = PdfWriter()

            for page in cover_reader.pages:
                writer.add_page(page)
            writer.add_page(secret_reader.pages[0])

            intermediate_output = f"intermediate-{i}.pdf"
            with open(intermediate_output, "wb") as f:
                writer.write(f)

            pages_dict = writer._root_object["/Pages"]
            current_count = pages_dict["/Count"]
            new_count = NumberObject(current_count - 1)
            pages_dict.update({"/Count": new_count})

            output_pdf_path = f"Stego_method4-{i}.pdf"
            with open(output_pdf_path, "wb") as f:
                writer.write(f)

            print(f"Stego PDF file created successfully: {output_pdf_path}")
    

def extract(files):
    stego_files = files.split(",")

    # Stego files segmentation and sanitazation
    for i in range(len(stego_files)):
        stego_files[i] = stego_files[i].strip()


    # Reading shares from PDF files
    shares_txt = []

    for file in stego_files:
        reader = PdfReader(file)

        total_pages = len(reader.pages)  # Includes the hidden page
        visible_pages = reader.trailer["/Root"]["/Pages"]["/Count"]  # Visible page count

        if total_pages > visible_pages:
            hidden_page_index = total_pages - 1
            hidden_page = reader.pages[hidden_page_index]
            secret_text = hidden_page.extract_text()

            shares_txt.append(secret_text)
        else:
            print(f"No hidden page detected within {file}")

    # XOR of all shares
    shares = []
    for txt in shares_txt:
        shares.append(txt.split(" ")[:-1:])

    if len(stego_files) != 1:
        for i in range(len(shares) - 1):
            for j in range(len(shares[i])):
                shares[-1][j] = int(shares[-1][j]) ^ int(shares[i][j])
    else:
        for i in range(len(shares[0])):
            shares[0][i] = int(shares[0][i])
        

    # Decoding message
    secret = ""
    for code in shares[-1]:
        secret += chr(code)

    print(f"Extracted secret: {secret}")

embed("ref.pdf")
extract("Stego_method4-1.pdf")
embed("ref.pdf, przebieg.pdf")
extract("Stego_method4-1.pdf, Stego_method4-2.pdf")
