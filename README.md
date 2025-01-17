# batch-pdf-splitter

`batch-pdf-splitter` is a Python tool designed to efficiently split large PDF files into smaller, more manageable parts based on specified page ranges. Ideal for users who need to process and manage extensive PDF documents, this tool allows for precise control over the division of content, making it easy to extract specific sections, chapters, or pages from a larger PDF file. Whether you're working with books, reports, or academic papers, `batch-pdf-splitter` streamlines the process of breaking down PDFs for easier sharing, editing, or analysis.

## Key features

- **Batch splitting:** Split large PDFs into multiple parts based on user-defined page ranges.
- **Custom naming:** Optionally specify custom output filenames to match your organization needs.
- **Logging:** Generate detailed logs to track the progress and results of the splitting process.
- **Overwrite control:** Safely handle file overwriting with an optional flag.
- **Support for both range and individual pages:** Flexibility to define splitting ranges or extract single pages.

### Perfect for

- Extracting chapters from eBooks
- Splitting long reports into smaller sections for better manageability
- Managing academic papers or textbooks
- Automating the PDF splitting process in batch tasks

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To split a large PDF file into smaller PDFs based on page ranges, run the following command:

```bash
python pdf_splitter.py test/input.pdf output/ --ranges "1-5,6-10,11-15" --overwrite --log_file "output/split_log.txt"
```

### Arguments:

- `input_pdf`: Path to the input PDF file to split.
- `output_dir`: Directory to save the split PDF files.
- `--ranges`: Comma-separated page ranges, e.g. '1-5,6-10,11-15'.
- `--overwrite`: Optional flag to overwrite existing files.
- `--log_file`: Path to a log file where the split info will be recorded.

### License

Copyright 2025 Max Base

License MIT
