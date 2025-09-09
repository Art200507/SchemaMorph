import re

def filter_faculty(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    
    passed_lines = []
    failed_lines = []
    
    pattern = r',\s*(Assistant Professor|Associate Professor|Professor),\s*([^,]*?(Engineering|Computer Science)[^,]*?),'
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
            
        if re.search(pattern, line, re.IGNORECASE):
            passed_lines.append(line)
        else:
            failed_lines.append((line_num, line))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in passed_lines:
            f.write(line + '\n')
    
    print("Lines that didn't pass the filter:")
    for line_num, line in failed_lines:
        print(f"Line {line_num}: {line}")
    
    print(f"\nFiltered results saved to: {output_file}")
    print(f"Total lines processed: {len(lines)}")
    print(f"Lines that passed: {len(passed_lines)}")
    print(f"Lines that failed: {len(failed_lines)}")

if __name__ == "__main__":
    input_file = "engineering_file.txt"
    output_file = "enhanced_file.txt"
    
    filter_faculty(input_file, output_file)