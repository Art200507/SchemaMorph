#!/usr/bin/env python3
"""
Tenure Track Filter
Filters out non-tenure-track faculty and administrative positions
"""

def filter_tenure_track(input_filename='engineering_file.txt', output_filename='TenureTrackFilterCleaned.txt'):
    """
    Filter out faculty with administrative roles or non-tenure-track positions.
    
    Args:
        input_filename (str): Input file with faculty data
        output_filename (str): Output file for cleaned data
    """
    # Keywords to filter out
    filter_keywords = [
        'Lecturer',
        'Emeritus',
        'Engineering Technology',
        'Visting'
    ]
    
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        filtered_lines = []
        removed_count = 0
        
        print("ELIMINATED LINES:")
        print("-" * 50)
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if any filter keyword is in the line
            should_filter = False
            for keyword in filter_keywords:
                if keyword in line:
                    should_filter = True
                    removed_count += 1
                    print(f"ELIMINATED: {line}")
                    break
            
            # If no filter keywords found, keep the line
            if not should_filter:
                filtered_lines.append(line)
        
        # Write filtered results to output file
        with open(output_filename, 'w', encoding='utf-8') as f:
            for line in filtered_lines:
                f.write(line + '\n')
        
        print(f"Tenure Track Filter Results:")
        print(f"=" * 50)
        print(f"Input file: {input_filename}")
        print(f"Output file: {output_filename}")
        print(f"Original entries: {len(lines)}")
        print(f"Filtered out: {removed_count}")
        print(f"Remaining entries: {len(filtered_lines)}")
        print(f"✅ Filtering completed successfully!")
        
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found!")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    filter_tenure_track()