# Faculty Excel Converter - Futuristic 3D UI

A cutting-edge web interface for the Faculty Excel Converter with a stunning 3D holographic design.

## Features

- ✨ **Futuristic 3D Interface**: Holographic morphing reality with animated 3D blob
- 🎨 **Modern Design**: Gradient backgrounds, glass morphism, and smooth animations
- 📊 **Three Main Functions**:
  - Analyze faculty changes between two years
  - Update Excel files with detected changes
  - Create custom Excel templates

## Quick Start

### Option 1: Use the Startup Script (Recommended)

```bash
./start_3d_ui.sh
```

This script will:
1. Create and activate a virtual environment
2. Install all Python dependencies
3. Build the frontend (if needed)
4. Start the server on http://localhost:8080

### Option 2: Manual Setup

#### Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install --legacy-peer-deps

# Build the frontend
npm run build

# Return to root directory
cd ..
```

#### Run the Application

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Start the Flask server
python app_api.py
```

The application will be available at: http://localhost:8080

## Development Mode

To run the frontend in development mode with hot reloading:

```bash
cd frontend
npm run dev
```

This will start the Vite development server on http://localhost:3000

**Note**: In development mode, you'll also need to run the Flask backend separately:

```bash
python app_api.py
```

## Technologies Used

### Frontend
- **React 19**: Modern UI framework
- **TypeScript**: Type-safe development
- **Vite**: Lightning-fast build tool
- **Tailwind CSS**: Utility-first CSS framework
- **React Three Fiber**: 3D graphics with Three.js
- **Drei**: Useful helpers for React Three Fiber
- **Lucide React**: Beautiful icon library

### Backend
- **Flask**: Python web framework
- **Pandas**: Data manipulation
- **OpenPyXL**: Excel file handling
- **Flask-CORS**: Cross-origin resource sharing

## Project Structure

```
Faculty-Excel-Converter/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FloatingBlob.tsx  # 3D animated blob
│   │   │   └── ui/               # UI components
│   │   ├── App.tsx               # Main application
│   │   ├── main.tsx              # Entry point
│   │   └── index.css             # Styles
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
├── app_api.py                    # Flask backend
├── converter.py                  # Core conversion logic
├── requirements.txt              # Python dependencies
└── start_3d_ui.sh               # Startup script
```

## Usage

### 1. Analyze Faculty Changes

- Upload two faculty data files (earlier year and later year)
- Files should be in `.txt` format with structure:
  ```
  Professor: John Doe, Jane Smith
  Associate Professor: Alice Brown
  ```
- View detailed analysis including:
  - New hires
  - Resignations
  - Title changes
  - Faculty with multiple titles

### 2. Update Excel File

- Upload an existing Excel file
- Upload two faculty data files for comparison
- Specify the year column to update (e.g., "2024-2025")
- Download the updated Excel file with changes highlighted

### 3. Create Template

- Specify year columns (comma-separated)
- Example: `2023-2024, 2024-2025, 2025-2026`
- Download a fresh Excel template with your specified columns

## Troubleshooting

### Frontend Build Issues

If you encounter dependency conflicts during `npm install`:

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npm run build
```

### Python Dependencies

If you have issues with Python packages:

```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Port Already in Use

If port 8080 is already in use, you can change it in `app_api.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)  # Change to any available port
```

## Performance Notes

The application uses:
- **3D rendering** which may require decent GPU performance
- **Large JavaScript bundle** (~1MB) - consider code splitting for production
- **Responsive design** that adapts to different screen sizes

## Future Enhancements

- [ ] Add dark/light mode toggle
- [ ] Implement real-time file preview
- [ ] Add drag-and-drop file upload
- [ ] Export analysis results as PDF
- [ ] Add data visualization charts
- [ ] Implement user authentication
- [ ] Add file upload history
- [ ] Progressive Web App (PWA) support

## License

Same as the main Faculty Excel Converter project.

## Credits

UI design inspired by modern holographic and futuristic interfaces.
