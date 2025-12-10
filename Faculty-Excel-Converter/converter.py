#!/usr/bin/env python3
"""
Faculty Data Converter Module
Converts txt input files to Excel format with faculty changes tracking
"""

from collections import defaultdict
from difflib import get_close_matches
import pandas as pd
from pathlib import Path


class FacultyConverter:
    """Handles faculty data parsing and comparison"""

    def __init__(self, cutoff=0.85):
        self.cutoff = cutoff

    def parse_txt_to_dict(self, file_path):
        """
        Parse faculty data from txt file into a dictionary.
        Format: Title: Name1, Name2, Name3
        """
        faculty_dict = {}
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if ":" in line:
                    parts = line.split(":", 1)
                    title = parts[0].strip()
                    names_string = parts[1].strip()
                    if names_string:
                        names_list = [name.strip() for name in names_string.split(',') if name.strip()]
                    else:
                        names_list = []
                    faculty_dict[title] = names_list
        return faculty_dict

    def match_name(self, name, name_set, cutoff=None):
        """Find a matching name using fuzzy matching"""
        if cutoff is None:
            cutoff = self.cutoff
        matches = get_close_matches(name.strip(), [n.strip() for n in name_set], n=1, cutoff=cutoff)
        return matches[0] if matches else None

    def find_unusual_patterns(self, dict1, dict2, cutoff=0.75):
        """Find names that are very similar but not exact matches"""
        names1 = {name.strip() for names in dict1.values() for name in names}
        names2 = {name.strip() for names in dict2.values() for name in names}
        unusual = defaultdict(list)
        for name1 in names1:
            close_matches = get_close_matches(name1, names2, n=3, cutoff=cutoff)
            for match in close_matches:
                if name1 != match:
                    unusual[name1].append(match)
        return unusual

    def compare_faculty(self, dict1, dict2):
        """
        Compare two faculty dictionaries to find changes.
        Returns: new_hires, resigned, title_changes, multiple_titles
        """
        new_hires = defaultdict(list)
        resigned = defaultdict(list)
        title_changes = {}
        multiple_titles = defaultdict(list)

        # Create reverse lookup maps (name -> title)
        title_map_1 = {}
        title_map_2 = {}

        for title, names in dict1.items():
            for name in names:
                if name in title_map_1:
                    if isinstance(title_map_1[name], list):
                        title_map_1[name].append(title)
                    else:
                        title_map_1[name] = [title_map_1[name], title]
                else:
                    title_map_1[name] = title

        for title, names in dict2.items():
            for name in names:
                if name in title_map_2:
                    if isinstance(title_map_2[name], list):
                        title_map_2[name].append(title)
                    else:
                        title_map_2[name] = [title_map_2[name], title]
                else:
                    title_map_2[name] = title

        matched_map_2 = {}
        unmatched_names_2 = set(title_map_2.keys())

        for name1 in title_map_1:
            match = self.match_name(name1, unmatched_names_2)
            if match:
                for name2 in unmatched_names_2:
                    if name2.strip() == match:
                        matched_map_2[name1] = name2
                        unmatched_names_2.remove(name2)
                        break
            else:
                matched_map_2[name1] = None

        # Detect title changes
        for name1, match_name2 in matched_map_2.items():
            if match_name2:
                title1 = title_map_1[name1]
                title2 = title_map_2[match_name2]
                if isinstance(title1, list) or isinstance(title2, list):
                    multiple_titles[name1] = {
                        "year1": title1 if isinstance(title1, list) else [title1],
                        "year2": title2 if isinstance(title2, list) else [title2]
                    }
                elif title1 != title2:
                    title_changes[name1] = {
                        "from": title1,
                        "to": title2
                    }

        changed_names = set(title_changes.keys())
        multiple_title_names = set(multiple_titles.keys())

        # Detect new hires and resignations
        all_names_1 = set(name.strip() for names in dict1.values() for name in names)
        all_names_2 = set(name.strip() for names in dict2.values() for name in names)

        # Find new hires
        for title, names in dict2.items():
            for name in names:
                match = self.match_name(name, all_names_1)
                if not match:
                    new_hires[title].append(name)

        # Find resignations
        for title, names in dict1.items():
            for name in names:
                matched_name = self.match_name(name, all_names_2)
                if not matched_name and name not in changed_names and name not in multiple_title_names:
                    resigned[title].append(name)

        # Detect unusual patterns and filter
        unusual_patterns = self.find_unusual_patterns(dict1, dict2)
        unusual_names = set()
        for name, matches in unusual_patterns.items():
            unusual_names.add(name)
            for match in matches:
                unusual_names.add(match)

        def filter_names(name_list):
            return [name for name in name_list if name not in unusual_names]

        new_hires = {title: filter_names(names) for title, names in new_hires.items() if filter_names(names)}
        resigned = {title: filter_names(names) for title, names in resigned.items() if filter_names(names)}

        return new_hires, resigned, title_changes, multiple_titles


class ExcelUpdater:
    """Handles Excel file updates with faculty changes"""

    @staticmethod
    def parse_title_change(change_string):
        """Return new title if change_string is like 'Old -> New'"""
        return change_string.split('->')[-1].strip() if '->' in change_string else change_string.strip()

    @staticmethod
    def update_excel(excel_path, year_column, resigned_list, title_changes_dict, new_hires_dict):
        """
        Update Excel with faculty resignations, promotions, and new hires.

        Args:
            excel_path (str): Path to Excel file
            year_column (str): The year column to update
            resigned_list (list): Faculty names who resigned
            title_changes_dict (dict): name -> "old -> new" or just "new"
            new_hires_dict (dict): name -> full title

        Returns:
            (bool, str, list, str): Success, message, list of changes, output_path
        """
        try:
            df = pd.read_excel(excel_path, sheet_name='Sheet1')

            if df.empty:
                return False, "Excel file is empty or could not be read properly.", [], None

            if 'Faculty name' not in df.columns or year_column not in df.columns:
                missing = 'Faculty name' if 'Faculty name' not in df.columns else year_column
                return False, f"Error: '{missing}' column not found.", [], None

            changes = []

            # Process resignations and title changes
            for idx, row in df.iterrows():
                name = row['Faculty name']
                if pd.isna(name):
                    continue

                current_value = row[year_column]

                if name in resigned_list:
                    df.at[idx, year_column] = 'N'
                    changes.append(f"RESIGNED: {name}: {current_value} → N")
                elif name in title_changes_dict:
                    new_title = ExcelUpdater.parse_title_change(title_changes_dict[name])
                    df.at[idx, year_column] = new_title
                    changes.append(f"TITLE CHANGE: {name}: {current_value} → {new_title}")

            # Add/update new hires
            for name, full_title in new_hires_dict.items():
                found = df[df['Faculty name'] == name]
                if not found.empty:
                    idx = found.index[0]
                    old = df.at[idx, year_column]
                    df.at[idx, year_column] = full_title
                    changes.append(f"UPDATED: {name}: {old} → {full_title}")
                else:
                    new_row = {'Faculty name': name, 'Department': 'Engineering', year_column: full_title}
                    for col in df.columns:
                        if col not in ('Faculty name', 'Department', year_column):
                            new_row[col] = 'N'
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    changes.append(f"NEW HIRE: {name} as {full_title}")

            # Save file
            p = Path(excel_path)
            output_path = p.parent / f"{p.stem}_updated_{year_column.replace('-', '_')}{p.suffix}"
            df.to_excel(output_path, index=False)

            return True, f"File updated successfully", changes, str(output_path)

        except Exception as e:
            return False, f"Error processing file: {e}", [], None

    @staticmethod
    def create_base_template(output_path, year_columns=None):
        """
        Create a base Excel template for faculty data.

        Args:
            output_path (str): Path to save the template
            year_columns (list): List of year columns (e.g., ['2018-2019', '2019-2020'])
        """
        if year_columns is None:
            year_columns = ['2023-2024', '2024-2025']

        columns = ['Faculty name', 'Department'] + year_columns
        df = pd.DataFrame(columns=columns)

        # Add sample data
        sample_data = [
            {'Faculty name': 'Sample Professor', 'Department': 'Engineering',
             year_columns[0]: 'Professor', year_columns[-1]: 'Professor'},
        ]
        df = pd.DataFrame(sample_data)

        df.to_excel(output_path, index=False)
        return True, f"Template created at {output_path}"
