# SchemaMorph - Faculty Excel Converter

A unified web application with a stunning 3D UI to convert faculty data from text files to Excel format, track changes between years, and automatically update Excel files with new hires, resignations, and title changes.

## Features

- **Modern 3D UI**: Beautiful React + Three.js interface with animated backgrounds
- **Analyze Faculty Changes**: Compare two faculty data files to identify changes
- **Update Excel Files**: Automatically update Excel spreadsheets with detected changes
- **Create Templates**: Generate base Excel templates with custom year columns
- **Fuzzy Matching**: Intelligent name matching to handle minor spelling variations
- **Unified Application**: Single app combining Flask backend with React 3D frontend

## Quick Start

### Automated Setup

Simply run the startup script:
```bash
chmod +x start.sh
./start.sh
```

This will automatically:
- Create a Python virtual environment
- Install Python dependencies
- Install npm dependencies
- Build the React frontend
- Start the unified application

The application will be available at `http://localhost:5001`

### Manual Setup (Advanced)

If you prefer manual setup:

1. **Install Python dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Build the frontend:**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

### Input File Format

Your faculty data text files should follow this format:

```
Professor: John Doe, Jane Smith, Bob Johnson
Associate Professor: Alice Brown, Charlie Davis
Assistant Professor: Eve Wilson, Frank Miller
```

Each line should contain:
- A faculty title
- A colon `:`
- Comma-separated faculty names

### Features Guide

#### 1. Analyze Faculty Changes

- Upload two faculty data files (earlier year and later year)
- The system will identify:
  - **Resignations**: Faculty who left
  - **New Hires**: Faculty who joined
  - **Title Changes**: Faculty who were promoted/demoted
  - **Multiple Titles**: Faculty holding multiple positions

#### 2. Update Excel File

- Upload an existing Excel file
- Upload two faculty data files for comparison
- Specify the year column to update (e.g., "2024-2025")
- The system will:
  - Mark resigned faculty as 'N'
  - Update titles for promoted faculty
  - Add new hires to the spreadsheet
  - Download the updated Excel file

#### 3. Create Template

- Specify year columns (comma-separated)
- Generate a base Excel template with:
  - Faculty name column
  - Department column
  - Year columns as specified

## Excel File Requirements

Your Excel file must have:
- A sheet named `Sheet1`
- A column named `Faculty name`
- Year columns matching your input (e.g., `2023-2024`, `2024-2025`)

## Project Structure

```
Faculty-Excel-Converter/
├── app.py                  # Flask web application
├── converter.py            # Core conversion logic
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── results.html      # Analysis results
│   └── create_template.html  # Template creator
├── uploads/              # Temporary file storage
└── static/               # Static assets (if needed)
```

## How It Works

### 1. Data Parsing
The system parses text files with the format `Title: Name1, Name2, Name3` into structured dictionaries.

### 2. Faculty Comparison
Using fuzzy matching (85% similarity by default), the system compares two datasets to identify:
- Who left (resignations)
- Who joined (new hires)
- Who changed titles (promotions/demotions)
- Who holds multiple positions

### 3. Excel Updates
The system updates Excel files by:
- Marking resigned faculty with 'N' in the target year column
- Updating titles for promoted/demoted faculty
- Adding new rows for new hires with appropriate defaults

## Example Workflow

1. **Prepare your data files:**
   - `faculty_2023.txt` - Faculty list from 2023-2024
   - `faculty_2024.txt` - Faculty list from 2024-2025

2. **Analyze changes:**
   - Upload both files via the web interface
   - Review the detected changes

3. **Update Excel:**
   - Upload your existing Excel file
   - Upload both data files
   - Specify year column (e.g., "2024-2025")
   - Download the updated file

## Configuration

You can adjust fuzzy matching sensitivity in `converter.py`:

```python
converter = FacultyConverter(cutoff=0.85)  # Default 85% similarity
```

## Security Notes

- Change the Flask secret key in production:
  ```python
  app.secret_key = 'your-secure-random-key'
  ```
- Files are automatically cleaned up after processing
- Maximum upload size: 16MB

## Netlify Deployment

The futuristic React frontend that lives in the `frontend/` directory is ready to be deployed as a static site on Netlify. The backend (Flask) still needs to be hosted separately (Render, Fly.io, EC2, etc.) and exposed through HTTPS.

1. **Configure the API URL**
   - Update the `.env` file inside `frontend/` or add a Netlify environment variable named `VITE_API_BASE_URL` pointing to your backend (example: `https://faculty-api.example.com`).
   - When the variable is left blank, the UI calls the same origin (useful for local development with the Flask server running behind a proxy).

2. **Connect the Repository to Netlify**
   - Netlify will detect the `netlify.toml` file in the repo root and automatically run the build from the `frontend/` directory.
   - The relevant settings in `netlify.toml` are:
     - `base = "frontend"`
     - `command = "npm run build"`
     - `publish = "build"`

3. **Deploy**
   - Push your changes to the default branch and trigger a deploy in the Netlify dashboard.
   - After the site builds, requests such as `/analyze` or `/update-excel` will be routed to the backend defined by `VITE_API_BASE_URL`.

You can also run `netlify dev` locally to emulate the production build pipeline using the configuration provided in `netlify.toml`.

## Troubleshooting

### "Column not found" error
- Ensure your Excel file has a column named exactly `Faculty name`
- Verify the year column name matches your input (case-sensitive)

### Names not matching correctly
- Adjust the `cutoff` parameter in `FacultyConverter` (lower = more lenient)
- Check for unusual characters or formatting in names

### Template not downloading
- Check browser download settings
- Verify you have write permissions in the uploads folder

## License

This project is provided as-is for educational and internal use.

## Support

For issues or questions, please check:
1. This README file
2. Input file format examples
3. Excel file requirements
