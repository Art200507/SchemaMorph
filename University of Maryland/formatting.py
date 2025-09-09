INPUT_FILE = 'file.txt'
OUTPUT_FILE = 'formatted_file.txt'

import re

def format_faculty_entries():
    """
    Formats University of Maryland faculty entries by combining multi-line entries into single lines.
    Format: Name starts with capital letter and ends with period, followed by position/degree info.
    """
    with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as fin:
        lines = fin.readlines()
    
    formatted_entries = []
    current_entry = ""
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Check if this line is a new name
        # A name should: 1) Have surname, firstname format with comma
        #                2) Not be a continuation of degree/institution info
        #                3) Not start with common position/degree words
        is_new_name = False
        
        # First check if line contains typical institution words that would indicate it's NOT a name
        institution_indicators = [
            'University', 'College', 'Institute', 'School', 'Academy', 'Seminary',
            'Polytechnic', 'Technology', 'Medical Center', 'Hospital', 'Laboratory'
        ]
        
        is_institution_line = any(indicator in line for indicator in institution_indicators)
        
        if line and ',' in line and not is_institution_line:
            # Split on first comma to get potential surname
            parts = line.split(',', 1)
            surname = parts[0].strip()
            remainder = parts[1].strip() if len(parts) > 1 else ""
            
            # Check if this looks like a surname (not a degree, institution, or position)
            is_surname = (
                re.match(r'^[A-Z][A-Za-z\'\-\s]+$', surname) and  # Starts with capital, only letters/apostrophes/hyphens
                not surname.startswith('B.') and
                not surname.startswith('M.') and
                not surname.startswith('Ph.D') and
                not surname.startswith('Professor') and
                not surname.startswith('Associate') and
                not surname.startswith('Assistant') and
                not surname.startswith('Lecturer') and
                not surname.startswith('Chair') and
                not surname.startswith('Distinguished') and
                not surname.startswith('Adjunct') and
                not surname.startswith('Visiting') and
                not surname.startswith('Affiliate') and
                not surname.startswith('Dean') and
                not surname.startswith('University') and
                not surname.startswith('College') and
                not surname.startswith('Institute') and
                not surname.startswith('School') and
                len(surname.split()) <= 3  # Surnames shouldn't be too long
            )
            
            # Check if remainder looks like a first name (not a position or institution)
            is_firstname = (
                remainder and
                re.match(r'^[A-Z][A-Za-z\.\s]*', remainder) and  # Starts with capital letter
                not remainder.startswith('Professor') and
                not remainder.startswith('Associate') and
                not remainder.startswith('Assistant') and
                not remainder.startswith('Lecturer') and
                not remainder.startswith('University') and
                not remainder.startswith('College') and
                not remainder.startswith('Institute') and
                not remainder.startswith('School')
            )
            
            # Additional checks for the full line
            if is_surname and is_firstname:
                is_new_name = (
                    not line.endswith('Ph.D.,') and
                    not line.endswith('Ph.D.') and
                    not line.endswith('M.A.,') and
                    not line.endswith('M.S.,') and
                    not line.endswith('B.A.,') and
                    not line.endswith('B.S.,') and
                    not line.endswith('D.M.A.,') and
                    # Should not be just a degree line
                    not re.match(r'^[A-Z]\..*[,.]?$', line)
                )
        
        if is_new_name:
            # Save previous entry if it exists and clean it up
            if current_entry:
                # Remove trailing commas and clean up double commas
                cleaned_entry = re.sub(r',+', ',', current_entry.strip())
                cleaned_entry = cleaned_entry.rstrip(',')
                formatted_entries.append(cleaned_entry)
            # Start new entry with the name
            current_entry = line
        else:
            # Continue building current entry
            if current_entry:
                # Add space before appending, but handle commas properly
                if line.startswith(','):
                    current_entry += line
                else:
                    current_entry += ", " + line
    
    # Don't forget the last entry
    if current_entry:
        # Remove trailing commas and clean up double commas
        cleaned_entry = re.sub(r',+', ',', current_entry.strip())
        cleaned_entry = cleaned_entry.rstrip(',')
        formatted_entries.append(cleaned_entry)
    
    # Final cleanup of all entries
    final_entries = []
    for entry in formatted_entries:
        # Fix awkward comma spacing issues
        cleaned = re.sub(r',\s*,', ',', entry)  # Remove double commas with spaces
        cleaned = re.sub(r';\s*,', ';', cleaned)  # Remove comma after semicolon
        cleaned = re.sub(r',\s+([A-Z][a-z])', r', \1', cleaned)  # Ensure space after comma before words
        final_entries.append(cleaned)
    
    return final_entries

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