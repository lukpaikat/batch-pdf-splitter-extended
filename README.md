# batch-pdf-splitter

`batch-pdf-splitter` is a Python utility for splitting one or more PDF files into smaller, more manageable outputs based on user-defined page groups. It supports precise control over page extraction, custom naming, and batch processing for documents such as books, reports, academic papers, and administrative files.

## Key features

- **Batch processing:** Split multiple input PDFs in a single run.
- **Flexible page grouping:** Use semicolons to create separate output files and commas to combine multiple page ranges into one output.
- **Non-contiguous page grouping:** Create files from non-sequential pages such as `1-3,5-6` or `2,4,6`.
- **Custom naming:** Assign friendly names to each output using `--names`.
- **Dynamic output formatting:** Use `--output_filename` to generate structured filenames such as `part_{0}.pdf`.
- **Logging:** Record split activity in a log file for traceability.
- **Overwrite control:** Safely overwrite existing files with `--overwrite` when needed.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic example

Split a single PDF into multiple output files based on page ranges:

```bash
python pdf_splitter.py test/input.pdf output/ --ranges "1-5,6-10,11-15" --overwrite --log_file "output/split_log.txt"
```

### Advanced Examples

**1. Custom Naming Format:**
Process multiple PDFs and reverse the naming format to `[split_name]_[original_filename].pdf`:

```bash
python pdf_splitter.py input1.pdf input2.pdf output/ --ranges "1-3,5-6; 7-9" --names "chapter-one; chapter-two" --output_filename "{name}_{base}.pdf" --overwrite --log_file "output/split_log.txt"
```

**2. Split Every Page (1-Page per File) from a Folder:**
Scan a directory for all PDFs and split every single page into separate files, dynamically numbered:

```bash
python pdf_splitter.py ./my_pdf_folder/ output/ --ranges "all" --output_filename "{base}_page_{idx}.pdf"
```

### Arguments

- `input_pdfs`: One or more input PDF files OR folders containing PDFs.
- `output_dir`: Directory where the split PDF files will be saved.
- `--ranges`: Semicolon-separated file groups and comma-separated page ranges (e.g., "1-3,5-6; 7-9"). Use "all" to automatically split every page into a separate file.
- `--names`: Semicolon-separated custom names for each generated output file.
- `--output_filename`: Custom format for the output filename. Supports placeholders: {base} (original filename), {name} (from --names), and {idx} (sequence number). Example: "{name}_{base}.pdf".
- `--overwrite`: Overwrite existing output files.
- `--log_file`: Path to a file where split activity will be recorded.

## Attribution

This repository is an enhanced fork of the original `batch-pdf-splitter` created by [Max Base](https://github.com/max-base). The core PDF parsing foundation belongs to the original author. This version, maintained by Lukpaikat, adds advanced batch processing, custom dynamic naming, and non-contiguous page grouping capabilities.

## License

Copyright 2025 Max Base

License MIT
