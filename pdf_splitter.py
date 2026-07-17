import os
import PyPDF2
import argparse
from tqdm import tqdm


def create_output_dir(output_dir):
    """Create the output directory if it doesn't exist."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def parse_page_ranges(range_str, total_pages=None):
    """
    Parse groups of page ranges. 
    Supports 'per:N' to split every N pages.
    Otherwise, semicolons separate files, commas combine pages.
    """
    range_str_lower = range_str.strip().lower()
    
    if range_str_lower.startswith('per:'):
        if total_pages is None:
            raise ValueError("total_pages is required for the 'per:N' format.")
        try:
            chunk_size = int(range_str_lower.split(':')[1])
            if chunk_size <= 0:
                raise ValueError
            
            file_groups = []
            for i in range(0, total_pages, chunk_size):
                end = min(i + chunk_size, total_pages)
                file_groups.append([(i, end)])
            return file_groups
        except (ValueError, IndexError):
            print(f"Invalid range format: {range_str}. Use 'per:N' where N is a number.")
            return []

    file_groups = []
    for group_str in range_str.split(';'):
        page_ranges = []
        for range_item in group_str.split(','):
            range_item = range_item.strip()
            if not range_item:
                continue
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
        if page_ranges:
            file_groups.append(page_ranges)
            
    return file_groups


def parse_split_names(names_str):
    """Parse the semicolon-separated names provided by the user."""
    if not names_str:
        return None
    return [name.strip() for name in names_str.split(';')]


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


def generate_output_filename(output_dir, idx, base_filename, split_name=None, output_filename=None):
    """Generate the output PDF filename based on the provided names or defaults."""
    name_val = split_name if split_name else f"part_{idx + 1}"
    
    if output_filename:
        formatted_name = output_filename.format(base=base_filename, name=name_val, idx=idx + 1)
        if not formatted_name.lower().endswith('.pdf'):
            formatted_name += '.pdf'
        return os.path.join(output_dir, formatted_name)
    
    if split_name:
        return os.path.join(output_dir, f"{base_filename}_{split_name}.pdf")
    
    return os.path.join(output_dir, f"{base_filename}_part_{idx + 1}.pdf")


def split_pdf(input_pdf_path, output_dir, range_str, split_names=None, overwrite=False, output_filename=None, log_file=None):
    """Splits a PDF into smaller PDFs based on ranges and assigns custom names."""
    try:
        base_filename = os.path.splitext(os.path.basename(input_pdf_path))[0]
        
        with open(input_pdf_path, 'rb') as input_pdf:
            pdf_reader = PyPDF2.PdfReader(input_pdf)
            total_pages = len(pdf_reader.pages)

            log = open(log_file, 'a') if log_file else None
            write_log(log, f"Splitting {input_pdf_path} (Total pages: {total_pages}) into smaller files:")

            page_ranges = parse_page_ranges(range_str, total_pages)
            
            if not page_ranges:
                write_log(log, "No valid page ranges to execute. Skipping this file.")
                return

            for idx, file_group in tqdm(enumerate(page_ranges), desc="Processing Files", total=len(page_ranges)):
                pdf_writer = PyPDF2.PdfWriter()
                pages_added = False

                for (start, end) in file_group:
                    if not validate_page_range(start, end, total_pages):
                        write_log(log, f"Invalid page range {start}-{end}. Skipping.")
                        continue
                    
                    for page_num in range(start, end):
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                        pages_added = True
                
                if not pages_added:
                    continue

                current_split_name = None
                if split_names and idx < len(split_names):
                    current_split_name = split_names[idx]

                output_pdf_path = generate_output_filename(output_dir, idx, base_filename, current_split_name, output_filename)

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
            log.close()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Split PDF files into smaller parts by page range or chunk size.")
    
    parser.add_argument('input_pdfs', nargs='+', help="Path to one or more input PDF files to split.")
    parser.add_argument('output_dir', help="Directory to save the split PDF files.")
    
    parser.add_argument('--ranges', type=str, required=True, help="Page ranges (e.g., '1-2,4-5; 3') OR number of pages per chunk (e.g., 'per:2' to split every 2 pages)")

    parser.add_argument('--names', type=str, default=None, help="Semicolon-separated names for each split. E.g., 'health certificate; drug test'")
    
    parser.add_argument('--output_filename', type=str, default=None, help="Custom naming format. Use {base} for original filename, {name} for split names, {idx} for number sequence. Example: '{name}_{base}.pdf'")
    parser.add_argument('--overwrite', action='store_true', help="Overwrite existing files.")
    parser.add_argument('--log_file', type=str, default=None, help="Log file to record created PDFs.")
    
    return parser.parse_args()


def main():
    """Main function to handle argument parsing and PDF splitting."""
    args = parse_args()

    create_output_dir(args.output_dir)
    split_names = parse_split_names(args.names)

    for input_pdf in args.input_pdfs:
        print(f"\n--- Processing: {input_pdf} ---")
        split_pdf(input_pdf, args.output_dir, args.ranges, split_names, args.overwrite, args.output_filename, args.log_file)


if __name__ == "__main__":
    main()