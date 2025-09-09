import re

INPUT_FILE = 'formatted_file.txt'
OUTPUT_FILE = 'engineering_file.txt'

def normalize_text(text: str) -> str:
    """Remove extra spaces and normalize text for better matching"""
    return re.sub(r'\s+', ' ', text.strip().lower())

def contains_engineering_fuzzy(line: str) -> bool:
    """Enhanced detection with fuzzy matching for OCR errors"""
    normalized = normalize_text(line)
    
    # Engineering patterns - handles spaces anywhere within the word
    engineering_patterns = [
        r'e\s*n\s*g\s*i\s*n\s*e\s*e\s*r\s*i\s*n\s*g',  # spaces anywhere in engineering
        r'engiecring',  # character transposition
        r'engicering',  # n->c substitution
    ]
    
    # Computer Science patterns - handles spaces anywhere within words
    cs_patterns = [
        r'c\s*o\s*m\s*p\s*u\s*t\s*e\s*r\s+s\s*c\s*i\s*e\s*n\s*c\s*e',  # spaces anywhere
    ]
    
    # Statistics patterns - handles spaces anywhere within the word
    statistics_patterns = [
        r's\s*t\s*a\s*t\s*i\s*s\s*t\s*i\s*c\s*s',  # spaces anywhere in statistics
    ]
    
    # Information Technology patterns - handles spaces anywhere within words
    it_patterns = [
        r'i\s*n\s*f\s*o\s*r\s*m\s*a\s*t\s*i\s*o\s*n\s+t\s*e\s*c\s*h\s*n\s*o\s*l\s*o\s*g\s*y',  # spaces anywhere
        r'i\s*n\s*f\s*o\s*r\s*m\s*a\s*t\s*i\s*o\s*n\s+s\s*c\s*i\s*e\s*n\s*c\s*e\s*s\s+a\s*n\s*d\s+t\s*e\s*c\s*h\s*n\s*o\s*l\s*o\s*g\s*y',  # Information Sciences and Technology
    ]
    
    # Check engineering patterns
    for pattern in engineering_patterns:
        if re.search(pattern, normalized):
            return True
    
    # Check computer science patterns
    for pattern in cs_patterns:
        if re.search(pattern, normalized):
            return True
    
    # Check statistics patterns
    for pattern in statistics_patterns:
        if re.search(pattern, normalized):
            return True
    
    # Check information technology patterns
    for pattern in it_patterns:
        if re.search(pattern, normalized):
            return True
    
    return False

def contains_engineering(line: str) -> bool:
    """Wrapper to maintain backward compatibility"""
    return contains_engineering_fuzzy(line)

def main():
    count = 0
    with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as fin, \
         open(OUTPUT_FILE, 'w', encoding='utf-8') as fout:
        for raw in fin:
            line = raw.rstrip()
            if not line:
                continue
            if contains_engineering(line):
                fout.write(line + '\n')
                count += 1
    print(f"Total lines with 'engineering' or 'computer science': {count}")

if __name__ == '__main__':
    main()
