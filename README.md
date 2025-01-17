# batch-pdf-splitter

Create a tool that splits large PDF files into smaller parts by page range. (python)

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

Copyright 2025

License MIT
