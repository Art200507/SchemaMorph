import re

INPUT_FILE = 'file.txt'
OUTPUT_FILE = 'formatted_file.txt'

def format_faculty_entries():
    """
    Simple formatting: combine multi-line entries into single lines.
    Each entry starts with a name (LastName, FirstName pattern).
    """
    with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as fin:
        lines = fin.readlines()
    
    formatted_entries = []
    current_entry = ""
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and page numbers
        if not line or line.isdigit() or 'Faculty Listing' in line:
            continue
        
        # Check if this line starts a new entry (name pattern: LastName, FirstName)
        is_new_entry = re.match(r'^[A-Z][a-z]+,\s+[A-Z]', line)
        
        if is_new_entry:
            # Save previous entry if it exists
            if current_entry:
                formatted_entries.append(current_entry.strip())
            # Start new entry
            current_entry = line
        else:
            # Continue building current entry
            if current_entry:
                current_entry += " " + line
    
    # Don't forget the last entry
    if current_entry:
        formatted_entries.append(current_entry.strip())
    
    return formatted_entries

def main():
    """Main function to format faculty entries and write to output file."""
    try:
        entries = format_faculty_entries()
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as fout:
            for entry in entries:
                fout.write(entry + '\n')
        
        print(f"Successfully formatted {len(entries)} faculty entries.")
        print(f"Output written to: {OUTPUT_FILE}")
        
    except FileNotFoundError:
        print(f"Error: Could not find input file '{INPUT_FILE}'")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()