# Faculty Excel Converter - Project Summary

## 🎯 Project Overview

This web application extracts the core conversion logic from various university faculty analysis scripts and provides a unified, user-friendly web interface for converting faculty data from text files to Excel format.

## 📦 What Was Extracted

The project consolidates functionality from multiple university-specific directories:
- **conversion.py** - Faculty data parsing and comparison logic
- **updater.py** - Excel file update functionality

All extracted from directories like:
- Kansas State University
- Georgia Tech University
- Wayne State University
- And 9+ other university implementations

## ✨ Key Features

### 1. **Faculty Change Analysis**
- Upload two faculty data text files (different years)
- Automatically detect:
  - Resignations
  - New hires
  - Title changes (promotions/demotions)
  - Faculty with multiple titles
- Beautiful visual summary of all changes

### 2. **Excel File Updates**
- Upload an existing Excel file
- Automatically update it with detected changes
- Marks resignations as 'N'
- Updates titles for promoted faculty
- Adds new faculty members
- Downloads updated file

### 3. **Template Generator**
- Create custom Excel templates
- Specify any year columns needed
- Generates properly formatted base file
- Ready to populate with faculty data

## 🔧 Technical Implementation

### Core Components

**converter.py**
- `FacultyConverter` class - Handles parsing and comparison
- Fuzzy name matching (85% similarity default)
- Intelligent change detection
- Filters unusual patterns to avoid false positives

**app.py**
- Flask web application
- File upload handling
- Route management
- Automatic file cleanup

**Templates**
- Responsive, modern UI
- Clean visual design
- Intuitive workflows
- Real-time feedback

## 📊 Input/Output Formats

### Input Format (Text Files)
```
Professor: John Doe, Jane Smith, Bob Johnson
Associate Professor: Alice Brown, Charlie Davis
Assistant Professor: Eve Wilson, Frank Miller
```

### Excel Format
| Faculty name | Department | 2023-2024 | 2024-2025 |
|-------------|------------|-----------|-----------|
| John Doe    | Engineering| Professor | Professor |

Values in year columns:
- Title names (Professor, Associate Professor, etc.)
- 'N' for not employed that year

## 🚀 Quick Start

```bash
# 1. Navigate to project
cd Faculty-Excel-Converter

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run application
python app.py

# 4. Open browser
# Go to http://localhost:5000
```

Or simply run:
```bash
./start.sh
```

## 📁 Project Structure

```
Faculty-Excel-Converter/
├── Core Application Files
│   ├── app.py              - Flask web server
│   ├── converter.py        - Conversion logic
│   └── requirements.txt    - Python dependencies
│
├── Web Interface
│   └── templates/
│       ├── base.html       - Base template
│       ├── index.html      - Home page
│       ├── results.html    - Analysis results
│       └── create_template.html - Template creator
│
├── Documentation
│   ├── README.md           - Full documentation
│   ├── QUICKSTART.md       - Quick start guide
│   └── PROJECT_SUMMARY.md  - This file
│
├── Example Data
│   ├── example_data_2023.txt
│   └── example_data_2024.txt
│
├── Utilities
│   ├── start.sh            - Startup script
│   └── .gitignore          - Git ignore rules
│
└── Storage
    └── uploads/            - Temporary file storage
```

## 🎨 Features Highlights

### Intelligent Matching
- Uses difflib fuzzy matching
- 85% similarity threshold (configurable)
- Handles name variations automatically
- Filters suspicious matches

### User-Friendly Interface
- Drag-and-drop file uploads
- Clear visual feedback
- Detailed change summaries
- Downloadable results

### Robust Processing
- Error handling throughout
- Automatic file cleanup
- Secure file uploads
- Validation at every step

## 🔒 Security Features

- File size limits (16MB)
- File type validation
- Secure filename handling
- Automatic cleanup of temporary files
- Session-based file management

## 📈 Use Cases

1. **Annual Faculty Updates**
   - Compare this year's roster to last year
   - Update master Excel file
   - Track all changes automatically

2. **Department Analysis**
   - Identify hiring trends
   - Track promotion patterns
   - Monitor turnover rates

3. **Record Keeping**
   - Maintain historical faculty data
   - Generate year-over-year reports
   - Archive changes systematically

## 🛠️ Customization Options

### Adjust Matching Sensitivity
In `converter.py`, change the cutoff:
```python
converter = FacultyConverter(cutoff=0.85)  # 0-1 scale
```

### Modify Default Department
In `converter.py`, ExcelUpdater.update_excel():
```python
new_row = {'Faculty name': name, 'Department': 'Your Department', ...}
```

### Change Port
In `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## 📝 Example Workflow

1. User visits web interface
2. Uploads two faculty data text files (2023 and 2024)
3. System analyzes and shows:
   - 3 resignations
   - 5 new hires
   - 2 promotions
4. User uploads existing Excel file
5. Specifies year column "2024-2025"
6. System updates Excel and provides download
7. User has updated faculty roster in seconds!

## 🎓 Benefits Over Original Scripts

| Original Scripts | New Web Application |
|-----------------|---------------------|
| Command-line only | Beautiful web interface |
| Hardcoded file paths | Upload any files |
| Manual data entry | Automatic processing |
| Text output only | Excel file updates |
| One university at a time | Universal solution |
| Technical knowledge needed | Anyone can use |

## 🔮 Future Enhancements (Optional)

- [ ] Database storage for historical data
- [ ] Multi-department support
- [ ] CSV export options
- [ ] Email notifications
- [ ] Batch processing
- [ ] Data visualization charts
- [ ] User authentication
- [ ] API endpoints

## 📞 Support

For issues or questions:
1. Check README.md for detailed docs
2. Review QUICKSTART.md for common tasks
3. Examine example data files
4. Verify input format requirements

## ✅ Testing

Test with provided example files:
- `example_data_2023.txt`
- `example_data_2024.txt`

Expected results:
- 2 promotions detected
- 2 new hires detected
- No resignations

## 🎉 Success Criteria

✅ Extracts core conversion logic from existing scripts
✅ Creates standalone web application
✅ Provides text-to-Excel conversion
✅ Analyzes faculty changes accurately
✅ Updates Excel files automatically
✅ Generates templates for users
✅ Beautiful, intuitive interface
✅ Comprehensive documentation
✅ Example data included
✅ Easy setup and deployment

---

**Project Status**: ✅ Complete and Ready to Use

**Created**: 2025
**Technology Stack**: Python, Flask, pandas, openpyxl
**License**: Internal/Educational Use
