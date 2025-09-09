#!/usr/bin/env python3
"""
Faculty Excel Updater with Full Title Support
Automates updating an Excel sheet of faculty with resignations, promotions, and new hires.
Handles all academic titles (including Clinical, Adjunct, Emeritus, etc.).
"""

import pandas as pd
import os
from pathlib import Path

def parse_title_change(change_string):
    """Return new title if change_string is like 'Old -> New'."""
    return change_string.split('->')[-1].strip() if '->' in change_string else change_string.strip()

def update_faculty_excel(excel_path, year_column, resigned, title_changes, new_hires):
    """
    Update Excel with faculty resignations, promotions, and new hires.

    Args:
        excel_path (str): Path to Excel file.
        year_column (str): The year column to update.
        resigned (list): Faculty names who resigned.
        title_changes (dict): name -> "old -> new" or just "new"
        new_hires (dict): name -> full title

    Returns:
        (bool, str, list): Success, message, list of changes
    """
    try:
        print("Reading Excel file...")
        df = pd.read_excel(excel_path, sheet_name='Sheet1')

        if df.empty:
            return False, "Excel file is empty or could not be read properly.", []

        if 'Faculty name' not in df.columns or year_column not in df.columns:
            missing = 'Faculty name' if 'Faculty name' not in df.columns else year_column
            return False, f"Error: '{missing}' column not found.", []

        changes = []

        # 1. Process resignations and title changes
        for idx, row in df.iterrows():
            name = row['Faculty name']
            if pd.isna(name): continue

            current_value = row[year_column]

            if name in resigned:
                df.at[idx, year_column] = 'N'
                changes.append(f"RESIGNED: {name}: {current_value} → N")
            elif name in title_changes:
                new_title = parse_title_change(title_changes[name])
                df.at[idx, year_column] = new_title
                changes.append(f"TITLE CHANGE: {name}: {current_value} → {new_title}")

        # 2. Add/update new hires
        duplicates = []
        for name, full_title in new_hires.items():
            found = df[df['Faculty name'] == name]
            if not found.empty:
                idx = found.index[0]
                old = df.at[idx, year_column]
                df.at[idx, year_column] = full_title
                changes.append(f"UPDATED: {name}: {old} → {full_title}")
                duplicates.append(name)
            else:
                new_row = {'Faculty name': name, 'Department': 'Engineering', year_column: full_title}
                for col in df.columns:
                    if col not in ('Faculty name', 'Department', year_column):
                        new_row[col] = 'N'
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                changes.append(f"NEW HIRE: {name} as {full_title}")

        # Save file
        p = Path(excel_path)
        new_file = p.parent / f"{p.stem}_updated_{year_column.replace('-', '_')}{p.suffix}"
        df.to_excel(new_file, index=False)
        return True, f"File updated. Saved as {new_file}", changes

    except Exception as e:
        return False, f"Error processing file: {e}", []

def main():
    # Example usage (replace data as needed)
    excel_file = "Kansas State University.xlsx"
    year_col = "2019-2020"

# RESIGNED FACULTY
    resigned_faculty = [
    "TIMOTHY L. BOWER",  # was Associate Professor
    "WILLIAM E. GENEREUX",  # was Associate Professor
    "TROY HARDING",  # was Associate Professor
    "THOMAS MERTZ",  # was Associate Professor
    "JULIA MORSE",  # was Associate Professor
    "EDUARD PLETT",  # was Associate Professor
    "RAJU DANDU",  # was Professor
    "SAEED KHAN"  # was Professor
]

# TITLE CHANGES
    title_changes = {
    "AJAY SHARDA": "Assistant Professor -> Associate Professor",
    "BIN LIU": "Assistant Professor -> Associate Professor",
    "JEREMY A. ROBERTS": "Assistant Professor -> Associate Professor",
    "MELANIE M. DERBY": "Assistant Professor -> Associate Professor",
    "STACEY E. KULESZA": "Assistant Professor -> Associate Professor"
}

# NEW HIRES
    new_hires = {
}





    print("Faculty Data Excel Updater - Full Title Support")
    print("=" * 50)
    print(f"Processing: {excel_file} | Updating column: {year_col}")

    if not os.path.exists(excel_file):
        print(f"ERROR: File '{excel_file}' not found!")
        return

    success, msg, changes = update_faculty_excel(
        excel_file, year_col, resigned_faculty, title_changes, new_hires
    )

    if success:
        print("\n✅ SUCCESS!")
        print(msg)
        print(f"\nTotal changes: {len(changes)}")
        for change in changes[:15]:
            print(f"  - {change}")
        if len(changes) > 15:
            print(f"  ...and {len(changes)-15} more changes")

        # Stats
        print("\nSummary:")
        print(f"  Resignations: {len([c for c in changes if c.startswith('RESIGNED:')])}")
        print(f"  Title Changes: {len([c for c in changes if c.startswith('TITLE CHANGE:')])}")
        print(f"  Updated: {len([c for c in changes if c.startswith('UPDATED:')])}")
        print(f"  New Hires: {len([c for c in changes if c.startswith('NEW HIRE:')])}")

        # New hire title distribution
        hire_titles = {}
        for c in changes:
            if c.startswith("NEW HIRE:"):
                title = c.split(" as ")[-1]
                hire_titles[title] = hire_titles.get(title, 0) + 1
        if hire_titles:
            print("\nNew Hire Titles:")
            for title, count in hire_titles.items():
                print(f"  {title}: {count}")

    else:
        print("\n❌ ERROR!")
        print(msg)

if __name__ == "__main__":
    main()
