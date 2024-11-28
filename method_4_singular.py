from PyPDF2 import PdfWriter, PdfReader
from PyPDF2.generic import NumberObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def create_text_pdf(text, output_filename):
    # Create a PDF with a single page containing the given text
    c = canvas.Canvas(output_filename, pagesize=letter)
    c.drawString(100, 750, text)
    c.save()


def embed(cover_pdf_path):
    secret = input("Enter the secret text: ")

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


embed("ref.pdf")
print(f"Extracted secret: {extract("Stego_method4.pdf")}")
