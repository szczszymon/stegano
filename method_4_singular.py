import PyPDF2
from PyPDF2 import PdfWriter, PdfReader
from PyPDF2.generic import NumberObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_text_pdf(text, output_filename):
    """Create a PDF with a single page containing the given text."""
    c = canvas.Canvas(output_filename, pagesize=letter)
    c.drawString(100, 750, text)  # Draw text at coordinates (100, 750)
    c.save()

# Step 1: Read the input PDF
cover_pdf_path = "ref.pdf"
cover_reader = PdfReader(cover_pdf_path)

# Step 2: Take user input for the secret message
secret = input("Enter the secret text: ")

# Step 3: Create a new PDF with the secret text
secret_pdf_path = "secret.pdf"
create_text_pdf(secret, secret_pdf_path)

# Step 4: Merge the cover and secret PDF
secret_reader = PdfReader(secret_pdf_path)
writer = PdfWriter()

# Add all pages from cover.pdf
for page in cover_reader.pages:
    writer.add_page(page)

# Add the single page from secret.pdf
writer.add_page(secret_reader.pages[0])

# Write intermediate file to visualize the change
intermediate_output = "intermediate.pdf"
with open(intermediate_output, "wb") as f:
    writer.write(f)

# Step 5: Modify the page count to simulate removing the last page
# Get the root object for the PDF
pages_dict = writer._root_object["/Pages"]

# Adjust the /Count value
current_count = pages_dict["/Count"]  # This is a PdfObject
new_count = NumberObject(current_count - 1)  # Decrement and wrap it as NumberObject
pages_dict.update({"/Count": new_count})  # Update the dictionary

# Write the final stego PDF
output_pdf_path = "Stego_method4.pdf"
with open(output_pdf_path, "wb") as f:
    writer.write(f)

print(f"PDF with steganography created successfully: {output_pdf_path}")
