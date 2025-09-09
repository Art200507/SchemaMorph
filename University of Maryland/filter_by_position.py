import re

INPUT_FILE = 'TenureTrackFilterCleaned.txt'
OUTPUT_FILE = 'final.txt'

def contains_engineering_or_cs(text: str) -> bool:
    """Check if text contains engineering or computer science"""
    if not text:
        return False
    
    text_lower = text.lower()
    
    # Check for engineering (with fuzzy matching for OCR errors)
    engineering_patterns = [
        r'engineering',
        r'engicering',  # n->c substitution
        r'engiecring',  # character transposition
        r'engi\s*neering',  # space in between
        r'engin\s*eering',  # space in between
    ]
    
    # Check for computer science
    cs_patterns = [
        r'computer\s+science',
        r'computer\s*science',
    ]
    
    # Check engineering patterns
    for pattern in engineering_patterns:
        if re.search(pattern, text_lower):
            return True
    
    # Check computer science patterns
    for pattern in cs_patterns:
        if re.search(pattern, text_lower):
            return True
    
    return False

def main():
    passed_count = 0
    eliminated_count = 0
    
    print("Eliminated entries:")
    print("-" * 80)
    
    with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as fin, \
         open(OUTPUT_FILE, 'w', encoding='utf-8') as fout:
        
        for line_num, line in enumerate(fin, 1):
            line = line.strip()
            if not line:
                continue
            
            # Split by comma
            parts = line.split(',')
            
            # Check if we have at least 3 parts (index 2 exists)
            if len(parts) >= 3:
                third_part = parts[3].strip()
                
                if contains_engineering_or_cs(third_part):
                    # Entry passes - save to output file
                    fout.write(line + '\n')
                    passed_count += 1
                else:
                    # Entry eliminated - print to terminal
                    print(f"Line {line_num}: {line}")
                    eliminated_count += 1
            else:
                # Not enough parts - eliminate
                print(f"Line {line_num} (insufficient parts): {line}")
                eliminated_count += 1
    
    print("-" * 80)
    print(f"Total entries passed: {passed_count}")
    print(f"Total entries eliminated: {eliminated_count}")
    print(f"Output saved to: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()