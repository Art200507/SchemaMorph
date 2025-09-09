#!/usr/bin/env python3
"""
Johns Hopkins University Faculty Format Converter
Simple approach: Name (Year) + next line with title/department
"""

import re

def convert_johns_hopkins_format(input_filename='file.txt', output_filename='formatted_file.txt'):
    """
    Convert Johns Hopkins University faculty entries to simple format:
    Each Name (Year) line combined with all following lines until the next Name (Year).
    """
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        converted_entries = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Check if this line has Name (Year) format
            if re.match(r'^[A-Z][a-zA-Z\s\.\-\(\)\']+\s\(\d{4}\)$', line):
                # This is a name line, start collecting all lines for this faculty
                faculty_lines = [line]
                i += 1
                
                # Collect all lines until we hit another Name (Year) or end of file
                while i < len(lines):
                    next_line = lines[i]
                    
                    # If we hit another Name (Year), stop collecting
                    if re.match(r'^[A-Z][a-zA-Z\s\.\-\(\)\']+\s\(\d{4}\)$', next_line):
                        break
                    
                    # Add this line to the current faculty entry
                    faculty_lines.append(next_line)
                    i += 1
                
                # Join all lines for this faculty member
                combined = ', '.join(faculty_lines)
                converted_entries.append(combined)
            else:
                i += 1
        
        # Write converted entries to output file
        with open(output_filename, 'w', encoding='utf-8') as f:
            for entry in converted_entries:
                f.write(entry + '\n')
        
        print(f"Johns Hopkins University Faculty Format Converter")
        print(f"=" * 55)
        print(f"Input file: {input_filename}")
        print(f"Output file: {output_filename}")
        print(f"Converted entries: {len(converted_entries)}")
        print(f"✅ Conversion completed successfully!")
        
        # Show first few converted entries as examples
        if converted_entries:
            print(f"\nFirst 5 converted entries:")
            print("-" * 55)
            for i, entry in enumerate(converted_entries[:5]):
                print(f"{i+1}. {entry}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found!")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    convert_johns_hopkins_format('file.txt', 'formatted_file.txt')