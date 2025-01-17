import os
import PyPDF2
import argparse
from tqdm import tqdm


def create_output_dir(output_dir):
    """Create the output directory if it doesn't exist."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def parse_page_ranges(range_str):
    """Parse a comma-separated page range string into a list of tuples."""
    page_ranges = []
    for range_item in range_str.split(','):
        try:
            if '-' in range_item:
                start, end = map(int, range_item.split('-'))
                page_ranges.append((start - 1, end))
            else:
                page = int(range_item)
                page_ranges.append((page - 1, page))
        except ValueError:
            print(f"Invalid range format: {range_item}. Skipping.")
            continue
    return page_ranges


def validate_page_range(start, end, total_pages):
    """Validate if the page range is within bounds."""
    if start < 0 or end > total_pages or start >= end:
        return False
    return True


def write_log(log, message):
    """Write a message to the log file if it's provided."""
    if log:
        log.write(message + '\n')
    print(message)


def split_pdf(input_pdf_path, output_dir, page_ranges, overwrite=False, output_filename=None, log_file=None):
    """
    Splits a large PDF into smaller PDFs based on the given page ranges.
    """
    try:
        with open(input_pdf_path, 'rb') as input_pdf:
            pdf_reader = PyPDF2.PdfReader(input_pdf)
            total_pages = len(pdf_reader.pages)

            log = open(log_file, 'a') if log_file else None
            write_log(log, f"Splitting {input_pdf_path} into smaller files:")

            for idx, (start, end) in tqdm(enumerate(page_ranges), desc="Processing Pages", total=len(page_ranges)):
                if not validate_page_range(start, end, total_pages):
                    write_log(log, f"Invalid page range {start}-{end}. Skipping.")
                    continue
                
                pdf_writer = PyPDF2.PdfWriter()

                for page_num in range(start, end):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                
                output_pdf_path = generate_output_filename(output_dir, idx, start, end, output_filename)

                if os.path.exists(output_pdf_path) and not overwrite:
                    write_log(log, f"File {output_pdf_path} already exists. Skipping...")
                    continue
                
                with open(output_pdf_path, 'wb') as output_pdf:
                    pdf_writer.write(output_pdf)

                write_log(log, f"Created {output_pdf_path}")

            if log:
                log.close()
    
    except Exception as e:
        error_message = f"Error processing {input_pdf_path}: {e}"
        print(error_message)
        if log:
            log.write(error_message + '\n')
        if log:
            log.close()


def generate_output_filename(output_dir, idx, start, end, output_filename=None):
    """Generate the output PDF filename based on the custom format or default format."""
    if output_filename:
        return os.path.join(output_dir, output_filename.format(idx + 1, start + 1, end))
    return os.path.join(output_dir, f"split_{idx + 1}_{start + 1}_{end}.pdf")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Split a large PDF file into smaller parts by page range.")
    
    parser.add_argument('input_pdf', help="Path to the input PDF file to split.")
    parser.add_argument('output_dir', help="Directory to save the split PDF files.")
    
    parser.add_argument('--ranges', type=str, required=True, help="Comma-separated page ranges, e.g. '1-5,6-10' or single pages '1,3,5'.")
    
    parser.add_argument('--output_filename', type=str, default=None, 
                        help="Custom output filename format, e.g. 'output_{0}_{1}_{2}.pdf'.")
    
    parser.add_argument('--overwrite', action='store_true', help="Overwrite existing files.")
    
    parser.add_argument('--log_file', type=str, default=None, help="Log file to record created PDFs.")
    
    return parser.parse_args()


def main():
    """Main function to handle argument parsing and PDF splitting."""
    args = parse_args()

    create_output_dir(args.output_dir)

    page_ranges = parse_page_ranges(args.ranges)

    split_pdf(args.input_pdf, args.output_dir, page_ranges, args.overwrite, args.output_filename, args.log_file)


if __name__ == "__main__":
    main()
