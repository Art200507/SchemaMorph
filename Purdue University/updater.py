#!/usr/bin/env python3
"""
Faculty Excel Updater with Full Title Support (FIXED VERSION)
Automates updating an Excel sheet of faculty with resignations, promotions, and new hires.
Handles all academic titles (including Clinical, Adjunct, Emeritus, etc.).
"""

import pandas as pd
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_title_change(change_string):
    """Return new title if change_string is like 'Old -> New'."""
    if not isinstance(change_string, str):
        return str(change_string).strip()
    return change_string.split('->')[-1].strip() if '->' in change_string else change_string.strip()

def normalize_name(name):
    """Normalize name for case-insensitive comparison."""
    if pd.isna(name) or not isinstance(name, str):
        return ""
    return name.strip().lower()

def find_available_filename(base_path):
    """Find an available filename by adding a counter if needed."""
    path = Path(base_path)
    if not path.exists():
        return str(path)
    
    counter = 1
    while True:
        new_name = f"{path.stem}_{counter}{path.suffix}"
        new_path = path.parent / new_name
        if not new_path.exists():
            return str(new_path)
        counter += 1

def update_faculty_excel(excel_path, year_column, resigned, title_changes, new_hires, default_department="Engineering"):
    """
    Update Excel with faculty resignations, promotions, and new hires.

    Args:
        excel_path (str): Path to Excel file.
        year_column (str): The year column to update.
        resigned (list): Faculty names who resigned.
        title_changes (dict): name -> "old -> new" or just "new"
        new_hires (dict): name -> full title
        default_department (str): Default department for new hires

    Returns:
        (bool, str, list): Success, message, list of changes
    """
    try:
        logger.info("Reading Excel file...")
        
        # Try to read the Excel file, handle different sheet scenarios
        try:
            # First try to read all sheets to see what's available
            xl_file = pd.ExcelFile(excel_path)
            sheet_names = xl_file.sheet_names
            logger.info(f"Available sheets: {sheet_names}")
            
            # Use the first sheet if Sheet1 doesn't exist
            sheet_name = 'Sheet1' if 'Sheet1' in sheet_names else sheet_names[0]
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            logger.info(f"Using sheet: {sheet_name}")
            
        except Exception as e:
            return False, f"Error reading Excel file: {e}", []

        if df.empty:
            return False, "Excel file is empty or could not be read properly.", []

        # Check for required columns
        if 'Faculty name' not in df.columns:
            # Try alternative column names
            possible_names = ['Faculty Name', 'Name', 'faculty name', 'faculty_name']
            found_col = None
            for col in possible_names:
                if col in df.columns:
                    df = df.rename(columns={col: 'Faculty name'})
                    found_col = col
                    break
            
            if not found_col:
                return False, "Error: No faculty name column found. Expected 'Faculty name' or similar.", []

        if year_column not in df.columns:
            return False, f"Error: '{year_column}' column not found. Available columns: {list(df.columns)}", []

        # Create name mapping for case-insensitive lookup
        name_to_index = {}
        for idx, row in df.iterrows():
            name = row['Faculty name']
            if pd.notna(name) and isinstance(name, str):
                normalized = normalize_name(name)
                if normalized:
                    name_to_index[normalized] = idx

        changes = []
        
        # Normalize input names for matching
        resigned_normalized = {normalize_name(name): name for name in resigned}
        title_changes_normalized = {normalize_name(name): (name, change) for name, change in title_changes.items()}
        new_hires_normalized = {normalize_name(name): (name, title) for name, title in new_hires.items()}

        # 1. Process resignations and title changes
        for idx, row in df.iterrows():
            name = row['Faculty name']
            if pd.isna(name) or not isinstance(name, str):
                continue

            normalized_name = normalize_name(name)
            current_value = row[year_column]

            if normalized_name in resigned_normalized:
                original_name = resigned_normalized[normalized_name]
                df.at[idx, year_column] = 'N'
                changes.append(f"RESIGNED: {name}: {current_value} → N")
                
            elif normalized_name in title_changes_normalized:
                original_name, change = title_changes_normalized[normalized_name]
                new_title = parse_title_change(change)
                df.at[idx, year_column] = new_title
                changes.append(f"TITLE CHANGE: {name}: {current_value} → {new_title}")

        # 2. Collect new hires that aren't already in the DataFrame
        new_rows_data = []
        for normalized_name, (original_name, full_title) in new_hires_normalized.items():
            if normalized_name in name_to_index:
                # Update existing faculty member
                idx = name_to_index[normalized_name]
                old_value = df.at[idx, year_column]
                df.at[idx, year_column] = full_title
                changes.append(f"UPDATED: {df.at[idx, 'Faculty name']}: {old_value} → {full_title}")
            else:
                # Prepare new row data
                new_row = {'Faculty name': original_name, year_column: full_title}
                
                # Add default department if Department column exists
                if 'Department' in df.columns:
                    new_row['Department'] = default_department
                
                # Fill other columns with 'N' if they exist
                for col in df.columns:
                    if col not in new_row:
                        new_row[col] = 'N'
                
                new_rows_data.append(new_row)
                changes.append(f"NEW HIRE: {original_name} as {full_title}")

        # Add all new rows at once (more efficient)
        if new_rows_data:
            new_df = pd.DataFrame(new_rows_data)
            df = pd.concat([df, new_df], ignore_index=True)

        # Save file with safe filename
        p = Path(excel_path)
        suggested_name = p.parent / f"{p.stem}_updated_{year_column.replace('-', '_')}{p.suffix}"
        new_file = find_available_filename(suggested_name)
        
        df.to_excel(new_file, index=False, sheet_name=sheet_name if 'sheet_name' in locals() else 'Sheet1')
        
        return True, f"File updated successfully. Saved as {new_file}", changes

    except FileNotFoundError:
        return False, f"Error: File '{excel_path}' not found.", []
    except PermissionError:
        return False, f"Error: Permission denied accessing '{excel_path}'. File may be open in another application.", []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False, f"Error processing file: {e}", []

def main():
    # Example usage (replace data as needed)
    excel_file = "Purdue University.xlsx"
    year_col = "2009-2011" 



# RESIGNED FACULTY
    resigned_faculty = [
    "I. Hrbud",  # was Assistant Professor
    "P. K. Imbrie",  # was Assistant Professor
    "H. A. Diefes-Dux",  # was Assistant Professor
    "K. E. Ileleji",  # was Assistant Professor
    "J. S. Hovis",  # was Assistant Professor
    "H. Ochoa-Acuna",  # was Assistant Professor
    "T. P. Seager",  # was Assistant Professor
    "M. S. Sepulveda",  # was Assistant Professor
    "G. Lebanon",  # was Assistant Professor
    "M. Muthuraman",  # was Assistant Professor
    "L. Ozsen",  # was Assistant Professor
    "J. P. Richard",  # was Assistant Professor
    "M. Koslowskik",  # was Assistant Professor
    "K. S. Peterson",  # was Assistant Professor
    "N. J. Carroll",  # was Associate Professor
    "G. U. Lee",  # was Associate Professor
    "L. M. Chang",  # was Associate Professor
    "S. P. Midkiff",  # was Associate Professor
    "M. A. Lawley",  # was Associate Professor
    "T. Jevremovic",  # was Associate Professor
    "T. N. Farris",  # was Professor
    "M. A. Rotea",  # was Professor
    "L. F. Huggins",  # was Professor
    "R. Bashir",  # was Professor
    "P. Guo",  # was Professor
    "E. Bertino",  # was Professor
    "P. C. Doerschuk",  # was Professor
    "P. C. Krause",  # was Professor
    "G. W. Neudeck",  # was Professor
    "R. J. Schwartz",  # was Professor
    "N. B. Shroff",  # was Professor
    "E. H. Spafford",  # was Professor
    "P. H. Swain",  # was Professor
    "T. C. Chang",  # was Professor
    "R. L. Rardin",  # was Professor
    "G. Salvendy",  # was Professor
    "R. M. Uzsoy",  # was Professor
    "R. J. Bernhard",  # was Professor
    "N. M. Laurendeau",  # was Professor
    "M. W. Plesniak",  # was Professor
    "W. Soedel"  # was Professor
]

# TITLE CHANGES
    title_changes = {
    "A. Bobet": "Associate Professor -> Professor",
    "A. H. Varma": "Assistant Professor -> Associate Professor",
    "A. Ivanisevic": "Assistant Professor -> Associate Professor",
    "A. P. Tarko": "Associate Professor -> Professor",
    "A. Raman": "Associate Professor -> Professor",
    "B. Yao": "Associate Professor -> Professor",
    "B. Ziaie": "Associate Professor -> Professor",
    "D. E. Adams": "Associate Professor -> Professor",
    "D. J. Love": "Assistant Professor -> Associate Professor",
    "D. Jiao": "Assistant Professor -> Associate Professor",
    "D. Peroulis": "Assistant Professor -> Associate Professor",
    "E. B. Slamovich": "Associate Professor -> Professor",
    "E. Nauman": "Assistant Professor -> Associate Professor",
    "G. B. King": "Associate Professor -> Professor",
    "G. Shaver": "Associate Professor -> Assistant Professor",
    "G. T. C. Chiu": "Associate Professor -> Professor",
    "H. W. Hillhouse": "Assistant Professor -> Associate Professor",
    "H. Yokota": "Associate Professor -> Professor",
    "I. Hua": "Associate Professor -> Professor",
    "J. Irudayaraj": "Assistant Professor -> Professor",
    "J. L. Rickus": "Assistant Professor -> Associate Professor",
    "J. Liu": "Assistant Professor -> Associate Professor",
    "J. P. Youngblood": "Assistant Professor -> Associate Professor",
    "J. X. Cheng": "Assistant Professor -> Associate Professor",
    "L. F. Nies": "Associate Professor -> Professor",
    "M. A. Capano": "Associate Professor -> Professor",
    "M. C. Santagata": "Assistant Professor -> Associate Professor",
    "M. Hastak": "Associate Professor -> Professor",
    "M. Prezzi": "Assistant Professor -> Associate Professor",
    "N. S. Mosier": "Assistant Professor -> Associate Professor",
    "P. H. Meckl": "Associate Professor -> Professor",
    "R. J. Frosch": "Associate Professor -> Professor",
    "S. Bagchi": "Assistant Professor -> Associate Professor",
    "S. D. Pekarek": "Associate Professor -> Professor",
    "S. Mohammadi": "Assistant Professor -> Associate Professor",
    "S. T. Revankar": "Associate Professor -> Professor",
    "T-M. G. Chu": "Assistant Professor -> Associate Professor",
    "T. Fisher": "Associate Professor -> Professor",
    "T. H. Siegmund": "Associate Professor -> Professor",
    "V. S. Pai": "Assistant Professor -> Associate Professor",
    "W. A. Crossley": "Associate Professor -> Professor",
    "W. E. Anderson": "Assistant Professor -> Associate Professor",
    "W. J. Chappell": "Assistant Professor -> Associate Professor",
    "W. J. Weiss": "Associate Professor -> Professor",
    "Y-Y. Won": "Assistant Professor -> Associate Professor",
    "Y. C. Hu": "Assistant Professor -> Associate Professor",
    "Y.-H. Lu": "Assistant Professor -> Associate Professor"
}

# NEW HIRES
    new_hires = {
    "K. Marais": "Assistant Professor",
    "L. Qiao": "Assistant Professor",
    "D. Sun": "Assistant Professor",
    "V. Tomar": "Assistant Professor",
    "D. M. Umulis": "Assistant Professor",
    "J. Y. Ji": "Assistant Professor",
    "Y. L. Kim": "Assistant Professor",
    "N. Kong": "Assistant Professor",
    "C. P. Neu": "Assistant Professor",
    "Z. Ouyang": "Assistant Professor",
    "Y. Yeo": "Assistant Professor",
    "K. Yoshida": "Assistant Professor",
    "R. Chakrabarti": "Assistant Professor",
    "Y. Wu": "Assistant Professor",
    "C. Yuan": "Assistant Professor",
    "H. Cai": "Assistant Professor",
    "G. Haikal": "Assistant Professor",
    "W. T. Horton": "Assistant Professor",
    "A. Kandil": "Assistant Professor",
    "P. Karava": "Assistant Professor",
    "V. M. Merwade": "Assistant Professor",
    "A. Prakash": "Assistant Professor",
    "C. Troy": "Assistant Professor",
    "A. Tzempelikos": "Assistant Professor",
    "P. Zavattieri": "Assistant Professor",
    "A. Boltasseva": "Assistant Professor",
    "C. M. Brown": "Assistant Professor",
    "L. N. E. Elmqvist": "Assistant Professor",
    "B. K. Jesiek": "Assistant Professor",
    "M. Kulkarni": "Assistant Professor",
    "O. Nohadani": "Assistant Professor",
    "J. Wachs": "Assistant Professor",
    "J. S. Yi": "Assistant Professor",
    "C. Martinez": "Assistant Professor",
    "K. B. Ariyur": "Assistant Professor",
    "X. Deng": "Assistant Professor",
    "B. Han": "Assistant Professor",
    "N. L. Key": "Assistant Professor",
    "A. M. Martini": "Assistant Professor",
    "J. F. Rhoads": "Assistant Professor",
    "J. Seipel": "Assistant Professor",
    "I. Jovanovic": "Assistant Professor",
    "I. Chaubey": "Associate Professor",
    "J. C. Martinez": "Associate Professor",
    "S. Ukkusuri": "Associate Professor",
    "M. J. Manfra": "Associate Professor",
    "A. J. Heber": "Professor",
    "J. Chmielewski": "Professor",
    "B. N. Doebbeling": "Professor",
    "R. Agrawal": "Professor",
    "J. Appenzeller": "Professor",
    "J. M. Woodall": "Professor",
    "A. Hassanein": "Professor"
}
    print("Faculty Data Excel Updater - Full Title Support (FIXED VERSION)")
    print("=" * 60)
    print(f"Processing: {excel_file} | Updating column: {year_col}")

    if not os.path.exists(excel_file):
        print(f"ERROR: File '{excel_file}' not found!")
        print("Please ensure the Excel file is in the same directory as this script.")
        return

    success, msg, changes = update_faculty_excel(
        excel_file, year_col, resigned_faculty, title_changes, new_hires
    )

    if success:
        print("\n✅ SUCCESS!")
        print(msg)
        print(f"\nTotal changes: {len(changes)}")
        
        # Show first 15 changes
        for change in changes[:15]:
            print(f"  - {change}")
        if len(changes) > 15:
            print(f"  ...and {len(changes)-15} more changes")

        # Stats
        resignations = len([c for c in changes if c.startswith('RESIGNED:')])
        title_changes_count = len([c for c in changes if c.startswith('TITLE CHANGE:')])
        updates = len([c for c in changes if c.startswith('UPDATED:')])
        new_hires_count = len([c for c in changes if c.startswith('NEW HIRE:')])
        
        print("\nSummary:")
        print(f"  Resignations: {resignations}")
        print(f"  Title Changes: {title_changes_count}")
        print(f"  Updated Existing: {updates}")
        print(f"  New Hires: {new_hires_count}")

        # New hire title distribution
        hire_titles = {}
        for c in changes:
            if c.startswith("NEW HIRE:"):
                try:
                    title = c.split(" as ")[-1]
                    hire_titles[title] = hire_titles.get(title, 0) + 1
                except IndexError:
                    continue
                    
        if hire_titles:
            print("\nNew Hire Title Distribution:")
            for title, count in sorted(hire_titles.items()):
                print(f"  {title}: {count}")

    else:
        print("\n❌ ERROR!")
        print(msg)
        print("\nTroubleshooting tips:")
        print("- Ensure the Excel file is not open in another application")
        print("- Check that the year column name matches exactly")
        print("- Verify the file has the expected structure")

if __name__ == "__main__":
    main()