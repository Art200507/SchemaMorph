#!/usr/bin/env python3
"""
Simple Faculty Organizer by Rank
Organizes faculty by Professor, Associate Professor, Assistant Professor
"""

def organize_faculty(filename='TenureTrackFilterCleaned.txt'):
    """
    Organize faculty by rank from comma-separated file.
    """
    professors = []
    associate_professors = []
    assistant_professors = []
    unmatched_lines = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            parts = line.split(',')
            if len(parts) >= 4:
                # New format: Last name, First name, PhD info, Title, Department
                last_name = parts[0].strip()
                first_name = parts[1].strip()
                full_name = f"{first_name} {last_name}"
                
                # Check all parts for the titles (university names may have commas)
                found_title = False
                for part in parts[2:]:  # Skip name parts, check from index 2 onwards
                    part = part.strip()
                    if part == "Assistant Professor":
                        assistant_professors.append(full_name)
                        found_title = True
                        break
                    elif part == "Associate Professor":
                        associate_professors.append(full_name)
                        found_title = True
                        break
                    elif part == "Professor":
                        professors.append(full_name)
                        found_title = True
                        break
                    elif "Assistant Professor" in part:
                        assistant_professors.append(full_name)
                        found_title = True
                        break
                    elif "Associate Professor" in part:
                        associate_professors.append(full_name)
                        found_title = True
                        break
                    elif "Professor" in part and part not in ["Assistant Professor", "Associate Professor"]:
                        professors.append(full_name)
                        found_title = True
                        break
                
                if not found_title:
                    unmatched_lines.append(line)
            else:
                unmatched_lines.append(line)
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Output results in comma-separated format
    print("Professor: " + ", ".join(professors))
    print("\nAssociate Professor: " + ", ".join(associate_professors))
    print("\nAssistant Professor: " + ", ".join(assistant_professors))
    
    if unmatched_lines:
        print(f"\nUNMATCHED ENTRIES:")
        print("=" * 50)
        for line in unmatched_lines:
            print(line)
    
    print(f"\n--- SUMMARY ---")
    print(f"Professors: {len(professors)}")
    print(f"Associate Professors: {len(associate_professors)}")
    print(f"Assistant Professors: {len(assistant_professors)}")
    print(f"Unmatched: {len(unmatched_lines)}")

if __name__ == "__main__":
    organize_faculty()