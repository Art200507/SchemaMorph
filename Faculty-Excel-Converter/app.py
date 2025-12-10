#!/usr/bin/env python3
"""
Faculty Excel Converter Web Application
Flask app for converting faculty txt data to Excel format
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from converter import FacultyConverter, ExcelUpdater
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'txt', 'xlsx', 'xls'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze two txt files and show faculty changes"""
    if 'file1' not in request.files or 'file2' not in request.files:
        flash('Please upload both data files', 'error')
        return redirect(url_for('index'))

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        flash('Please select both files', 'error')
        return redirect(url_for('index'))

    if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
        flash('Only .txt files are allowed for faculty data', 'error')
        return redirect(url_for('index'))

    # Save uploaded files
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file1_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{timestamp}_1_{secure_filename(file1.filename)}')
    file2_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{timestamp}_2_{secure_filename(file2.filename)}')

    file1.save(file1_path)
    file2.save(file2_path)

    try:
        # Parse and compare
        converter = FacultyConverter()
        dict1 = converter.parse_txt_to_dict(file1_path)
        dict2 = converter.parse_txt_to_dict(file2_path)
        new_hires, resigned, title_changes, multiple_titles = converter.compare_faculty(dict1, dict2)

        # Prepare data for display
        resigned_list = []
        for title, names in sorted(resigned.items()):
            for name in names:
                resigned_list.append({'name': name, 'title': title})

        title_changes_list = []
        for name, change in sorted(title_changes.items()):
            title_changes_list.append({
                'name': name,
                'from': change['from'],
                'to': change['to']
            })

        new_hires_list = []
        for title, names in sorted(new_hires.items()):
            for name in names:
                new_hires_list.append({'name': name, 'title': title})

        multiple_titles_list = []
        for name, titles in sorted(multiple_titles.items()):
            year1_titles = ", ".join(titles["year1"]) if isinstance(titles["year1"], list) else titles["year1"]
            year2_titles = ", ".join(titles["year2"]) if isinstance(titles["year2"], list) else titles["year2"]
            multiple_titles_list.append({
                'name': name,
                'year1': year1_titles,
                'year2': year2_titles
            })

        # Store file paths in session for later use
        summary = {
            'resignations': len(resigned_list),
            'new_hires': len(new_hires_list),
            'title_changes': len(title_changes_list),
            'multiple_titles': len(multiple_titles_list)
        }

        return render_template('results.html',
                             resigned=resigned_list,
                             title_changes=title_changes_list,
                             new_hires=new_hires_list,
                             multiple_titles=multiple_titles_list,
                             summary=summary)

    except Exception as e:
        flash(f'Error analyzing files: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        # Clean up uploaded files
        try:
            os.remove(file1_path)
            os.remove(file2_path)
        except:
            pass


@app.route('/update-excel', methods=['POST'])
def update_excel():
    """Update Excel file with faculty changes"""
    if 'excel_file' not in request.files or 'data_file1' not in request.files or 'data_file2' not in request.files:
        flash('Please upload all required files', 'error')
        return redirect(url_for('index'))

    excel_file = request.files['excel_file']
    data_file1 = request.files['data_file1']
    data_file2 = request.files['data_file2']
    year_column = request.form.get('year_column', '').strip()

    if not year_column:
        flash('Please specify the year column', 'error')
        return redirect(url_for('index'))

    if excel_file.filename == '' or data_file1.filename == '' or data_file2.filename == '':
        flash('Please select all files', 'error')
        return redirect(url_for('index'))

    # Save uploaded files
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{timestamp}_{secure_filename(excel_file.filename)}')
    data1_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{timestamp}_1_{secure_filename(data_file1.filename)}')
    data2_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{timestamp}_2_{secure_filename(data_file2.filename)}')

    excel_file.save(excel_path)
    data_file1.save(data1_path)
    data_file2.save(data2_path)

    try:
        # Parse and compare
        converter = FacultyConverter()
        dict1 = converter.parse_txt_to_dict(data1_path)
        dict2 = converter.parse_txt_to_dict(data2_path)
        new_hires, resigned, title_changes, multiple_titles = converter.compare_faculty(dict1, dict2)

        # Convert to format expected by ExcelUpdater
        resigned_list = []
        for title, names in resigned.items():
            resigned_list.extend(names)

        title_changes_dict = {}
        for name, change in title_changes.items():
            title_changes_dict[name] = f"{change['from']} -> {change['to']}"

        new_hires_dict = {}
        for title, names in new_hires.items():
            for name in names:
                new_hires_dict[name] = title

        # Update Excel
        success, message, changes, output_path = ExcelUpdater.update_excel(
            excel_path, year_column, resigned_list, title_changes_dict, new_hires_dict
        )

        if success:
            # Return the updated file
            return send_file(output_path, as_attachment=True, download_name=Path(output_path).name)
        else:
            flash(f'Error: {message}', 'error')
            return redirect(url_for('index'))

    except Exception as e:
        flash(f'Error updating Excel: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        # Clean up uploaded files (keep output file for download)
        try:
            os.remove(excel_path)
            os.remove(data1_path)
            os.remove(data2_path)
        except:
            pass


@app.route('/create-template', methods=['GET', 'POST'])
def create_template():
    """Create a base Excel template"""
    if request.method == 'POST':
        year_columns_str = request.form.get('year_columns', '')
        year_columns = [y.strip() for y in year_columns_str.split(',') if y.strip()]

        if not year_columns:
            flash('Please specify at least one year column', 'error')
            return redirect(url_for('create_template'))

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'faculty_template_{timestamp}.xlsx')

        try:
            success, message = ExcelUpdater.create_base_template(output_path, year_columns)
            if success:
                return send_file(output_path, as_attachment=True, download_name='faculty_template.xlsx')
            else:
                flash(f'Error: {message}', 'error')
                return redirect(url_for('create_template'))
        except Exception as e:
            flash(f'Error creating template: {str(e)}', 'error')
            return redirect(url_for('create_template'))

    return render_template('create_template.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
