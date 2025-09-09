#!/usr/bin/env python3

import re

def format_faculty_data(input_file, output_file):
    """
    Format faculty data so each entry occupies only one line.
    Combines multi-line entries into single lines.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by double newlines or lines that start with a name (capital letters)
    # Pattern: Look for lines that start with capital letters (likely names)
    lines = content.split('\n')
    
    formatted_entries = []
    current_entry = ""
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Check if this line starts a new entry (contains a name pattern)
        # Names are "Lastname, Firstname" format
        if re.match(r'^[A-Z][a-zA-Zöüäøåæé\'-]+,\s*[A-Z]', line):
            # Save previous entry if exists
            if current_entry:
                formatted_entries.append(current_entry.strip())
            # Start new entry
            current_entry = line
        else:
            # Continue current entry
            if current_entry:
                current_entry += " " + line
    
    # Don't forget the last entry
    if current_entry:
        formatted_entries.append(current_entry.strip())
    
    # Write formatted data
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in formatted_entries:
            f.write(entry + '\n')
    
    print(f"Formatted {len(formatted_entries)} entries")
    print(f"Output written to {output_file}")

# Usage example:
if __name__ == "__main__":
    input_file = "file.txt"
    output_file = "formatted_file.txt"
    
    try:
        format_faculty_data(input_file, output_file)
    except FileNotFoundError:
        print(f"Error: {input_file} not found")
    except Exception as e:
        print(f"Error: {e}")