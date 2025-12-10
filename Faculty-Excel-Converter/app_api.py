#!/usr/bin/env python3
"""
Faculty Excel Converter API
Flask API backend for the SchemaMorph React frontend
"""

from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from converter import FacultyConverter, ExcelUpdater
from datetime import datetime

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)
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
    return send_from_directory('frontend/build', 'index.html')


@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('frontend/build/assets', path)


@app.route('/analyze', methods=['POST'])
def api_analyze():
    """API endpoint to analyze two txt files and return faculty changes"""
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'error': 'Please upload both data files'}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        return jsonify({'error': 'Please select both files'}), 400

    if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
        return jsonify({'error': 'Only .txt files are allowed for faculty data'}), 400

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

        # Prepare data for response
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

        summary = {
            'resignations': len(resigned_list),
            'new_hires': len(new_hires_list),
            'title_changes': len(title_changes_list),
            'multiple_titles': len(multiple_titles_list)
        }

        return jsonify({
            'resigned': resigned_list,
            'title_changes': title_changes_list,
            'new_hires': new_hires_list,
            'multiple_titles': multiple_titles_list,
            'summary': summary
        })

    except Exception as e:
        return jsonify({'error': f'Error analyzing files: {str(e)}'}), 500
    finally:
        # Clean up uploaded files
        try:
            os.remove(file1_path)
            os.remove(file2_path)
        except:
            pass


@app.route('/update-excel', methods=['POST'])
def api_update_excel():
    """API endpoint to update Excel file with faculty changes"""
    if 'excel_file' not in request.files or 'data_file1' not in request.files or 'data_file2' not in request.files:
        return jsonify({'error': 'Please upload all required files'}), 400

    excel_file = request.files['excel_file']
    data_file1 = request.files['data_file1']
    data_file2 = request.files['data_file2']
    year_column = request.form.get('year_column', '').strip()

    if not year_column:
        return jsonify({'error': 'Please specify the year column'}), 400

    if excel_file.filename == '' or data_file1.filename == '' or data_file2.filename == '':
        return jsonify({'error': 'Please select all files'}), 400

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
            return jsonify({'error': message}), 500

    except Exception as e:
        return jsonify({'error': f'Error updating Excel: {str(e)}'}), 500
    finally:
        # Clean up uploaded files (keep output file for download)
        try:
            os.remove(excel_path)
            os.remove(data1_path)
            os.remove(data2_path)
        except:
            pass


@app.route('/create-template', methods=['POST'])
def api_create_template():
    """API endpoint to create a base Excel template"""
    year_columns_str = request.form.get('year_columns', '')
    year_columns = [y.strip() for y in year_columns_str.split(',') if y.strip()]

    if not year_columns:
        return jsonify({'error': 'Please specify at least one year column'}), 400

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'faculty_template_{timestamp}.xlsx')

    try:
        success, message = ExcelUpdater.create_base_template(output_path, year_columns)
        if success:
            return send_file(output_path, as_attachment=True, download_name='faculty_template.xlsx')
        else:
            return jsonify({'error': message}), 500
    except Exception as e:
        return jsonify({'error': f'Error creating template: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
