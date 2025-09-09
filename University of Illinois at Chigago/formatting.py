def format_file():
    with open('file.txt', 'r') as f:
        lines = f.readlines()
    
    formatted_entries = []
    current_entry = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip page headers/footers
        if "Faculty List" in line:
            continue
            
        # If line contains "PhD" or "MS", it's degree info
        if "PhD" in line or "MS" in line:
            if current_entry:
                current_entry.append(line)
                formatted_entries.append(", ".join(current_entry))
                current_entry = []
            else:
                # Standalone degree line, skip
                continue
        else:
            # If we have a pending entry, save it first
            if current_entry:
                formatted_entries.append(", ".join(current_entry))
            # Start new entry with name
            current_entry = [line]
    
    # Handle last entry
    if current_entry:
        formatted_entries.append(", ".join(current_entry))
    
    # Write formatted output
    with open('formatted_file.txt', 'w') as f:
        for entry in formatted_entries:
            f.write(entry + '\n')
    
    print(f"Formatted {len(formatted_entries)} entries")

if __name__ == "__main__":
    format_file()