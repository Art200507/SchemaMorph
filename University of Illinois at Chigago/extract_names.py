def extract_names():
    names = []
    
    with open('tenureTrackFilterCleaned.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                # Split by comma and get the first element (name)
                parts = line.split(',')
                if parts:
                    name = parts[0].strip()
                    names.append(name)
    
    # Print in the requested format
    print("Professor: " + ", ".join(names))

if __name__ == "__main__":
    extract_names()