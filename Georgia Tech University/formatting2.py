import re

def find_second_name_in_line(line):
    """Find if there's a second name-degree pattern in the same line"""
    
    # Skip the header lines
    if line.startswith("Total entries") or line.startswith("--- ALL ENTRIES ---") or line.strip() == "":
        return None, None
    
    # Pattern to find Name, Degree - but we need to find the SECOND occurrence
    name_degree_pattern = r'([A-Z][A-Za-z\s\.\-\']+(?:Jr\.|Sr\.|III|II|IV)?),?\s+(Ph\.D\.|M\.F\.A\.|M\.S\.|D\.B\.A\.|M\.L\.A\.|M\.A\.)'
    
    # Find all matches in the line
    matches = list(re.finditer(name_degree_pattern, line))
    
    if len(matches) < 2:
        return None, None  # Less than 2 matches, line is fine
    
    # We found multiple matches - split at the second match
    second_match_start = matches[1].start()
    
    # The first entry ends just before the second match
    first_entry = line[:second_match_start].strip()
    
    # The second entry starts from the second match
    second_entry = line[second_match_start:].strip()
    
    # Clean up - remove trailing commas and extra spaces
    first_entry = first_entry.rstrip(',').strip()
    second_entry = second_entry.rstrip(',').strip()
    
    return first_entry, second_entry

def post_process_faculty_file(input_filename, output_filename):
    """Post-process the faculty output to split any remaining concatenated entries"""
    
    try:
        # Read the input file
        with open(input_filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        processed_lines = []
        entries_split = 0
        
        for line in lines:
            line = line.strip()
            
            # Check if this line contains multiple entries
            first_entry, second_entry = find_second_name_in_line(line)
            
            if first_entry and second_entry:
                # Split found - add both entries separately
                processed_lines.append(first_entry)
                processed_lines.append(second_entry)
                entries_split += 1
                print(f"Split entry: '{first_entry[:50]}...' | '{second_entry[:50]}...'")
            else:
                # No split needed, keep original line
                processed_lines.append(line)
        
        # Write the processed output
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            # Update the count
            if processed_lines and processed_lines[0].startswith("Total entries"):
                # Calculate new total
                entry_count = len([line for line in processed_lines[2:] if line.strip()])  # Skip header lines
                output_file.write(f"Total entries found: {entry_count}\n")
                output_file.write("\n--- ALL ENTRIES (POST-PROCESSED) ---\n")
                
                # Write all non-header lines
                for line in processed_lines[2:]:
                    if line.strip():
                        output_file.write(line + '\n')
            else:
                # Just write everything as-is
                for line in processed_lines:
                    if line.strip():
                        output_file.write(line + '\n')
        
        print(f"\nPost-processing complete!")
        print(f"Entries split: {entries_split}")
        print(f"Cleaned output saved to: {output_filename}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")
        print("Make sure you've run the original faculty extraction script first.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    input_filename = 'faculty_output.txt'      # Output from your original script
    output_filename = 'faculty_output_clean.txt'  # Final clean output
    
    print("Post-processing faculty entries to split any concatenated entries...")
    post_process_faculty_file(input_filename, output_filename)

if __name__ == "__main__":
    main()