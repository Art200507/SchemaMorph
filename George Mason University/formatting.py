#!/usr/bin/env python3
import re

def format_faculty_entries(input_file, output_file):
    """
    Formats faculty entries from multi-line format to single-line format.
    Each faculty member's information is combined into one line.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by lines and clean up
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    formatted_entries = []
    current_entry = ""
    
    for line in lines:
        # Pattern to match start of new faculty entry:
        # "Lastname, Firstname [Middle], Title/Position..."
        # Must start with capital letter, have comma, then name, then comma and position
        name_pattern = r'^[A-Z][a-zA-Z\'\-]+,\s+[A-Z][a-zA-Z\.\s\-]+,\s+'
        
        if re.match(name_pattern, line) and current_entry:
            # Save the previous entry
            formatted_entries.append(current_entry.strip())
            current_entry = line
        elif re.match(name_pattern, line):
            # First entry
            current_entry = line
        else:
            # This is a continuation line
            if current_entry:
                current_entry += " " + line
            else:
                current_entry = line
    
    # Add the last entry
    if current_entry:
        formatted_entries.append(current_entry.strip())
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in formatted_entries:
            f.write(entry + '\n')
    
    print(f"Formatted {len(formatted_entries)} entries from {input_file} to {output_file}")

if __name__ == "__main__":
    input_file = "file.txt"
    output_file = "formatted_file.txt"
    format_faculty_entries(input_file, output_file)