#!/usr/bin/env python3
"""
Faculty 3-Line Format Parser
Converts faculty data from 3-line format to single-line format.

Input format:
Name
Degree University
Rank, Department

Output format:
Name, Degree University, Rank, Department
"""

import re

def parse_faculty_text(text):
    """
    Parse faculty data from 3-line format.
    
    Args:
        text (str): Multi-line faculty data
    
    Returns:
        list: List of faculty dictionaries
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    faculty_list = []
    
    # Process every 3 lines as a faculty entry
    for i in range(0, len(lines), 3):
        if i + 2 < len(lines):
            name = lines[i].strip()
            degree_university = lines[i + 1].strip()
            rank_department = lines[i + 2].strip()
            
            # Simply format as: Name, Degree University, Rank Department
            faculty_list.append(f"{name}, {degree_university}, {rank_department}")
    
    return faculty_list

def parse_degree_university(line):
    """
    Parse degree and university from second line.
    Examples:
    - "Ph.D. Catholic University Louvain"
    - "MFA, University Of Georgia" 
    - "Ph.D. University of Wisconsin, Madison"
    """
    line = line.strip()
    
    # Common degree patterns
    degree_patterns = [
        r'Ph\.D\.?',
        r'M\.F\.A\.?',
        r'MFA',
        r'M\.S\.?',
        r'D\.Phil\.?',
        r'Sc\.D\.?',
        r'M\.Arch\.?',
        r'J\.D\.?'
    ]
    
    # Try to find degree at the beginning
    for pattern in degree_patterns:
        match = re.match(f'({pattern})[\\s,]*(.+)', line, re.IGNORECASE)
        if match:
            degree = match.group(1)
            university = match.group(2).strip()
            # Remove leading comma if present
            university = re.sub(r'^,\s*', '', university)
            return degree, university
    
    # Fallback: split by first space/comma
    parts = re.split(r'[\s,]+', line, 1)
    degree = parts[0] if parts else ''
    university = parts[1] if len(parts) > 1 else ''
    
    return degree, university

def parse_rank_department(line):
    """
    Parse rank and department from third line.
    Examples:
    - "Associate Professor, Industrial and Systems Engineering"
    - "Professor, Mechanical Engineering"
    - "Executive Assistant to the President of the Academic Affairs and Professor, Chemical and Biomolecular Engineering, Chemical and Biomolecular Engineering"
    """
    line = line.strip()
    
    # Find the main rank keywords
    rank_patterns = [
        r'Executive\s+Assistant\s+to\s+the\s+President[^,]*and\s+Professor',
        r'Associate\s+Dean[^,]*',
        r'Regents\'\s+Professor',
        r'Distinguished\s+Professor',
        r'Associate\s+Professor',
        r'Assistant\s+Professor', 
        r'Professor',
        r'Instructor',
        r'Lecturer'
    ]
    
    rank = ''
    department = ''
    
    for pattern in rank_patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            rank = match.group(0)
            
            # Find department after the rank
            # Look for comma after the rank
            after_rank = line[match.end():].strip()
            if after_rank.startswith(','):
                department = after_rank[1:].strip()
                # Handle cases with multiple commas/departments
                # Take everything after first comma as department
                break
            else:
                # No comma found, might be part of a longer title
                continue
    
    # If no standard pattern found, try simple comma split
    if not rank and ',' in line:
        parts = line.split(',', 1)
        rank = parts[0].strip()
        department = parts[1].strip()
    elif not rank:
        rank = line
        department = ''
    
    return rank, department

def format_single_line(faculty):
    """
    Format faculty data into single line format.
    
    Args:
        faculty (dict): Faculty data dictionary
    
    Returns:
        str: Formatted single line
    """
    name = faculty['name']
    degree = faculty['degree']
    university = faculty['university']
    rank = faculty['rank']
    department = faculty['department']
    
    # Format: "Name, Degree University, Rank, Department"
    return f"{name}, {degree} {university}, {rank}, {department}"

def read_faculty_file(input_filename='file.txt'):
    """
    Read faculty data from input file.
    
    Args:
        input_filename (str): Input filename (default: file.txt)
    
    Returns:
        str: Faculty data text or None if error
    """
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"Successfully read faculty data from: {input_filename}")
        return content
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found!")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def process_faculty_file(input_filename='file.txt', output_filename='faculty_output.txt'):
    """
    Process faculty data from input file and save to output file.
    
    Args:
        input_filename (str): Input filename (default: file.txt)
        output_filename (str): Output filename (default: faculty_output.txt)
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Read input file
    faculty_text = read_faculty_file(input_filename)
    
    if faculty_text is None:
        return False
    
    # Parse faculty data
    faculty_list = parse_faculty_text(faculty_text)
    
    if not faculty_list:
        print("No faculty data found or parsed successfully.")
        return False
    
    # Faculty list already contains formatted lines
    formatted_lines = faculty_list
    
    # Write to output file
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for line in formatted_lines:
                f.write(line + '\n')
        
        print(f"Successfully processed {len(faculty_list)} faculty entries")
        print(f"Input file: {input_filename}")
        print(f"Output file: {output_filename}")
        
        # Display sample results
        print("\nFirst 5 converted entries:")
        print("-" * 80)
        for i, line in enumerate(formatted_lines[:5]):
            print(f"{i+1}. {line}")
        
        if len(formatted_lines) > 5:
            print(f"... and {len(formatted_lines) - 5} more entries")
        
        return True
        
    except Exception as e:
        print(f"Error writing to output file: {e}")
        return False

def main():
    """Main function - processes file.txt and creates faculty_output.txt"""
    print("Faculty 3-Line Format Parser")
    print("=" * 50)
    print("Input format:")
    print("  Name")
    print("  Degree University") 
    print("  Rank, Department")
    print("")
    print("Output format:")
    print("  Name, Degree University, Rank, Department")
    print("-" * 50)
    
    success = process_faculty_file('file.txt', 'faculty_output.txt')
    
    if success:
        print("\n✅ Conversion completed successfully!")
    else:
        print("\n❌ Conversion failed. Please check the input file.")

if __name__ == "__main__":
    main()