import PyPDF2
import os

def split_pdf(input_pdf_path, output_dir, page_ranges):
    """
    Splits a large PDF into smaller PDFs based on the given page ranges.

    :param input_pdf_path: Path to the input PDF file.
    :param output_dir: Directory to save the smaller split PDFs.
    :param page_ranges: List of tuples where each tuple is a range (start_page, end_page).
    """
    with open(input_pdf_path, 'rb') as input_pdf:
        pdf_reader = PyPDF2.PdfReader(input_pdf)
        total_pages = len(pdf_reader.pages)
        
        for idx, (start, end) in enumerate(page_ranges):
            if start < 0 or end > total_pages or start >= end:
                print(f"Invalid page range {start}-{end}. Skipping.")
                continue
            
            pdf_writer = PyPDF2.PdfWriter()

            for page_num in range(start, end):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            
            output_pdf_path = os.path.join(output_dir, f"split_{idx + 1}_{start + 1}_{end}.pdf")
            with open(output_pdf_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
            
            print(f"Created {output_pdf_path}")

def main():
    input_pdf_path = input("Enter the path to the PDF file to split: ")
    output_dir = input("Enter the directory to save split PDFs: ")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    page_ranges = [
        (0, 5),
        (5, 10),
        (10, 15),
    ]
    
    split_pdf(input_pdf_path, output_dir, page_ranges)

if __name__ == "__main__":
    main()
