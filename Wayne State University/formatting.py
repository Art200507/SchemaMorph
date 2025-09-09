#!/usr/bin/env python3
"""
Wayne State University Faculty Format Converter
Converts multi-line faculty entries to single-line format
"""

def convert_wayne_state_format(input_filename='file.txt', output_filename='formatted_file.txt'):
    """
    Convert Wayne State University multi-line faculty entries to single-line format.
    
    Format:
    Input:
        LASTNAME, FIRSTNAME: degree, institution; degree, institution; Position, Department
        Additional departments (continuation lines)
    
    Output:
        LASTNAME, FIRSTNAME: degree, institution; degree, institution; Position, Department, Additional departments
    """
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        converted_entries = []
        current_entry = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                # Empty line - save current entry if exists
                if current_entry:
                    converted_entries.append(current_entry)
                    current_entry = ""
                continue
            
            # Check if this line starts a new faculty entry (contains a colon after name)
            if ':' in line and line[0].isupper():
                # This is a new faculty entry
                if current_entry:
                    # Save previous entry
                    converted_entries.append(current_entry)
                current_entry = line
            else:
                # This is a continuation line
                if current_entry:
                    current_entry += ", " + line
        
        # Don't forget the last entry
        if current_entry:
            converted_entries.append(current_entry)
        
        # Write converted entries to output file
        with open(output_filename, 'w', encoding='utf-8') as f:
            for entry in converted_entries:
                f.write(entry + '\n')
        
        print(f"Wayne State University Faculty Format Converter")
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
    convert_wayne_state_format('file.txt', 'formatted_file.txt')