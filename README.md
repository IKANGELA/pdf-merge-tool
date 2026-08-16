# PDF Merge Tool

A simple desktop application for merging multiple PDF files into one document.

## Features
- select source folder
- choose output folder
- merge all PDFs from a folder or selected files
- sort files by name
- choose output filename
- open the generated PDF or output folder

## Requirements
- Python 3.10+
- pypdf

## Install
```bash
pip install pypdf
```

## Run
```bash
python polacz_pdf.py
```

## Build Windows executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "PDF Merge Tool" polacz_pdf.py
```

The executable will be generated in the `dist` folder.

## Default folders
The application creates a user-friendly default location in the Documents directory:

```text
Documents/
└── PDF Merge Tool/
    ├── Input/
    └── Output/
```

This avoids technical folders such as `__pycache__` and makes the app easier to use.

## Notes
This project is intended for local use and for creating a desktop Windows application for distribution.
