INPUT_FILE = 'formatted_file.txt'
OUTPUT_FILE = 'engineering_file.txt'

def contains_engineering(line: str) -> bool:
    return 'engineering' in line.lower() or 'computer science' in line.lower()

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
    print(f"Total lines with 'engineering': {count}")

if __name__ == '__main__':
    main()
