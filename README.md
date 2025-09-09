# Faculty Analysis Code

This repository contains Python scripts for analyzing faculty data across multiple universities. The codebase automates the process of extracting, formatting, filtering, and comparing faculty information from university directories.

## 📋 Overview

The project analyzes faculty data from the following universities:
- George Mason University
- Georgia Tech University  
- John's Hopkins University
- Kansas State University
- Purdue University
- University of Alabama
- University of Illinois at Chicago
- University of Maryland
- University of Minnesota
- University of South Carolina
- University of Wisconsin Madison
- Wayne State University

## 🏗️ Project Structure

Each university directory contains similar scripts for processing faculty data:

```
University Directory/
├── *.xlsx                    # Original faculty data in Excel format
├── conversion.py            # Converts 3-line format to single-line format
├── formatting.py            # Formats and structures faculty data
├── updater.py              # Updates Excel files with faculty changes
├── filter.py               # Filters faculty by specific criteria
├── EngineeringFilter.py    # Filters engineering faculty specifically
├── organise.py             # Organizes and processes faculty data
├── file.txt               # Raw faculty data input
├── formatted_file.txt     # Processed faculty data output
└── sampledata1.txt        # Sample data for comparison
└── sampledata2.txt        # Sample data for comparison
```

## 🔧 Core Scripts and Their Functions

### Data Processing Scripts

#### `conversion.py`
**Purpose**: Converts faculty data from 3-line format to single-line format
- **Input Format**: 
  ```
  Name
  Degree University  
  Rank, Department
  ```
- **Output Format**: `Name, Degree University, Rank, Department`
- **Key Functions**:
  - `parse_faculty_text()` - Parses multi-line faculty data
  - `parse_degree_university()` - Extracts degree and university information
  - `parse_rank_department()` - Separates academic rank from department
  - `process_faculty_file()` - Main processing function

#### `formatting.py` / `formating.py`
**Purpose**: Advanced faculty data parser that converts 3-line format to single-line with enhanced parsing
- **Features**:
  - Handles complex academic titles (Clinical, Adjunct, Emeritus, etc.)
  - Supports multiple degree formats (Ph.D., M.F.A., etc.)
  - Processes administrative roles and joint appointments
  - **Key Functions**:
    - `parse_degree_university()` - Smart degree/university parsing with regex
    - `parse_rank_department()` - Complex rank and department extraction
    - `format_single_line()` - Standardized output formatting

#### `updater.py`
**Purpose**: Automates Excel file updates with faculty changes (resignations, promotions, new hires)
- **Features**:
  - Case-insensitive name matching
  - Handles title changes with "Old -> New" format parsing
  - Processes resignations, promotions, and new hires
  - Creates backup files with safe naming
  - **Key Functions**:
    - `update_faculty_excel()` - Main Excel update function
    - `parse_title_change()` - Extracts new titles from change strings
    - `normalize_name()` - Standardizes names for comparison
    - `find_available_filename()` - Prevents file overwriting

### Filtering Scripts

#### `filter.py` / `TenureTrackFilter.py`
**Purpose**: Filters out non-tenure-track faculty and administrative positions
- **Filters**: Emeritus, Emerita, and other non-tenure positions
- **Output**: Clean list of tenure-track faculty only
- **Key Functions**:
  - `filter_tenure_track()` - Main filtering function
  - Keyword-based filtering system
  - Detailed reporting of eliminated entries

#### `EngineeringFilter.py`
**Purpose**: Specifically filters faculty members in engineering disciplines
- **Features**:
  - Case-insensitive 'engineering' keyword search
  - Counts total engineering faculty
  - **Key Functions**:
    - `contains_engineering()` - Engineering keyword detection
    - File I/O with encoding handling

#### `Faculty_filter.py` (Wayne State University)
**Purpose**: Custom filtering for specific faculty criteria
- Similar functionality to other filters but tailored to specific university needs

### Data Analysis Scripts

#### `organise.py` / `organiseNew.py` / `organise100.py`
**Purpose**: Organizes and processes faculty data with various approaches
- **Features**:
  - Data validation and cleaning
  - Faculty categorization
  - Statistical analysis preparation
  - Different versions for specific processing needs

#### `extract_names.py` (University of Illinois at Chicago)
**Purpose**: Specialized script for extracting faculty names from complex data formats

### Comparison and Analysis

The codebase includes sophisticated faculty comparison functionality (primarily in `conversion.py`):

#### Faculty Change Detection
- **New Hires**: Identifies faculty not present in previous year
- **Resignations**: Finds faculty who left the institution  
- **Title Changes**: Tracks promotions, demotions, and lateral moves
- **Multiple Titles**: Handles faculty with joint appointments

#### Advanced Matching
- **Fuzzy Matching**: Uses `difflib.get_close_matches()` for name variations
- **Threshold-based Matching**: Configurable similarity cutoffs (default 0.85)
- **Pattern Detection**: Identifies unusual naming patterns and variations

## 📊 Data Flow

1. **Raw Data Input** (`file.txt`, Excel files)
2. **Format Conversion** (`conversion.py`, `formatting.py`)
3. **Filtering** (`filter.py`, `EngineeringFilter.py`)
4. **Organization** (`organise.py`)
5. **Analysis and Updates** (`updater.py`)
6. **Output** (Formatted files, Updated Excel sheets)

## 🚀 Usage

### Basic Faculty Data Processing
```bash
# Convert 3-line format to single-line
python conversion.py

# Filter engineering faculty
python EngineeringFilter.py

# Update Excel with faculty changes
python updater.py
```

### Typical Workflow
1. Place raw faculty data in `file.txt`
2. Run `conversion.py` to format data
3. Apply filters as needed (`filter.py`, `EngineeringFilter.py`)
4. Organize data with `organise.py`
5. Update master Excel file with `updater.py`

## 📁 File Types

- **`.py`** - Python processing scripts
- **`.xlsx`** - Excel spreadsheets with faculty data
- **`.txt`** - Text files containing faculty information
- **`.json`** - Configuration files (n8n.json for workflow automation)

## 🔍 Key Features

- **Multi-format Support**: Handles various input formats and structures
- **Fuzzy Matching**: Intelligent name matching for tracking faculty changes
- **Comprehensive Filtering**: Multiple criteria for faculty categorization  
- **Excel Integration**: Direct Excel file updating and management
- **Error Handling**: Robust error handling and validation
- **Backup Creation**: Automatic backup file generation
- **Statistical Reporting**: Detailed change summaries and statistics

## 🛠️ Dependencies

- `pandas` - Excel file manipulation and data analysis
- `openpyxl` - Excel file reading/writing
- `difflib` - Fuzzy string matching for faculty name comparison
- `pathlib` - File path handling
- `logging` - Error and process logging

## 📈 Output Examples

### Faculty Changes Report
```
==================================================
FACULTY CHANGES REPORT  
==================================================

# RESIGNED FACULTY
resigned_faculty = [
    "John Smith",  # was Associate Professor
    "Jane Doe"     # was Assistant Professor  
]

# TITLE CHANGES
title_changes = {
    "Robert Johnson": "Assistant Professor -> Associate Professor",
    "Mary Wilson": "Associate Professor -> Professor"
}

# NEW HIRES  
new_hires = {
    "David Brown": "Assistant Professor",
    "Sarah Davis": "Associate Professor"
}
```

### Summary Statistics
- Total Resignations: 15
- Total New Hires: 12  
- Total Title Changes: 23
- Faculty with Multiple Titles: 3

This comprehensive faculty analysis system enables efficient tracking and management of academic personnel changes across multiple university systems.