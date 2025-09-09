#!/usr/bin/env python3
"""
Multi-line Faculty Format Converter
Converts multi-line faculty entries to single-line format
"""

def convert_multiline_to_single(input_filename='file.txt', output_filename='2003file.txt'):
    """
    Convert multi-line faculty entries to single-line format.
    
    Format:
    Input:
        Name, Degree
        University
        Title, Department (may span multiple lines)
        (blank line separator)
    
    Output:
        Name, Degree, University, Title, Department
    """
    import re
    
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content into lines and filter out empty lines
        all_lines = [line.strip() for line in content.split('\n') if line.strip()]
        converted_entries = []
        
        # Process lines by detecting faculty entry boundaries
        i = 0
        while i < len(all_lines):
            # Look for lines that start with names followed by degrees
            # Pattern: Name, Ph.D. or Name, M.F.A. etc.
            current_line = all_lines[i].strip()
            
            # Check if this line contains a degree (Ph.D., M.F.A., etc.)
            degree_pattern = r'(Ph\.D\.|M\.F\.A\.|M\.S\.|M\.A\.|B\.S\.|B\.A\.|Ed\.D\.|J\.D\.|M\.D\.|D\.Sc\.|Sc\.D\.)'
            
            if re.search(degree_pattern, current_line):
                # This is a faculty name line
                name_degree = current_line
                faculty_entry = [name_degree]
                i += 1
                
                # Collect all lines until we hit the next faculty entry or end of file
                while i < len(all_lines):
                    next_line = all_lines[i].strip()
                    
                    # Check if this line is the start of a new faculty entry
                    if re.search(degree_pattern, next_line):
                        break
                    
                    faculty_entry.append(next_line)
                    i += 1
                
                # Now process the collected faculty entry
                if len(faculty_entry) >= 3:
                    # First element is name/degree, second is university, rest is title/department
                    name_degree = faculty_entry[0]
                    university = faculty_entry[1]
                    title_dept = ', '.join(faculty_entry[2:])  # Join remaining lines as title/dept
                    
                    single_line = f"{name_degree}, {university}, {title_dept}"
                    converted_entries.append(single_line)
                elif len(faculty_entry) == 2:
                    # Handle incomplete entries
                    single_line = f"{faculty_entry[0]}, {faculty_entry[1]}"
                    converted_entries.append(single_line)
            else:
                # Skip lines that don't match faculty entry pattern
                i += 1
        
        # Write converted entries to output file
        with open(output_filename, 'w', encoding='utf-8') as f:
            for entry in converted_entries:
                f.write(entry + '\n')
        
        print(f"Multi-line Faculty Format Converter")
        print(f"=" * 50)
        print(f"Input file: {input_filename}")
        print(f"Output file: {output_filename}")
        print(f"Converted entries: {len(converted_entries)}")
        print(f"✅ Conversion completed successfully!")
        
        # Show first few converted entries as examples
        print(f"\nFirst 3 converted entries:")
        print("-" * 50)
        for i, entry in enumerate(converted_entries[:3]):
            print(f"{i+1}. {entry}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found!")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    convert_multiline_to_single('file.txt', '2003file.txt')