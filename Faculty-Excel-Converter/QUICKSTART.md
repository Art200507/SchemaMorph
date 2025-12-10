# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
cd Faculty-Excel-Converter
pip install -r requirements.txt
```

Or use the startup script:
```bash
./start.sh
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
Navigate to: **http://localhost:5000**

---

## 📝 Example Usage

### Analyze Faculty Changes

1. Go to the home page
2. Under "Analyze Faculty Changes":
   - Upload `example_data_2023.txt` as File 1
   - Upload `example_data_2024.txt` as File 2
3. Click "Analyze Changes"
4. View the results showing:
   - New hires (James Moore, Sarah Lee)
   - Title changes (Michael Wilson: Associate → Professor, David Thomas: Assistant → Associate)

### Update Excel File

1. Under "Update Excel File":
   - Upload your Excel file (must have 'Faculty name' column)
   - Upload two faculty data files
   - Enter the year column name (e.g., "2024-2025")
2. Click "Update Excel File"
3. Download the updated file

### Create Template

1. Click "Create Template" in the navigation
2. Enter year columns: `2023-2024, 2024-2025, 2025-2026`
3. Click "Generate Template"
4. Download and use the template

---

## 📁 File Formats

### Input Text File
```
Professor: John Doe, Jane Smith
Associate Professor: Bob Johnson
Assistant Professor: Alice Brown
```

### Excel File Structure
| Faculty name | Department | 2023-2024 | 2024-2025 |
|-------------|------------|-----------|-----------|
| John Doe    | Engineering| Professor | Professor |
| Jane Smith  | Engineering| N         | Assistant Professor |

---

## 🔧 Common Issues

**Error: "Column not found"**
- Make sure your Excel has a column named exactly "Faculty name"
- Check that the year column exists

**Names not matching**
- The system uses 85% fuzzy matching
- Check for typos or special characters

**Can't upload files**
- Max file size: 16MB
- Allowed formats: .txt, .xlsx, .xls

---

## 🎯 What Gets Detected

✅ **Resignations** - Faculty who left between years
✅ **New Hires** - Faculty who joined
✅ **Promotions** - Title changes (Assistant → Associate → Professor)
✅ **Multiple Titles** - Faculty holding multiple positions

---

## 💡 Tips

- Keep faculty names consistent across files
- Use standard title names (Professor, Associate Professor, Assistant Professor)
- Excel column names are case-sensitive
- The system automatically handles minor name variations

---

## 📊 Project Structure

```
Faculty-Excel-Converter/
├── app.py                    # Main web application
├── converter.py              # Core conversion logic
├── requirements.txt          # Dependencies
├── start.sh                 # Startup script
├── example_data_2023.txt    # Sample data file
├── example_data_2024.txt    # Sample data file
└── templates/               # Web interface
    ├── index.html
    ├── results.html
    └── create_template.html
```

---

For detailed documentation, see [README.md](README.md)
