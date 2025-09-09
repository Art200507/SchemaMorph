input_file = 'engineering_file.txt'

profs = []
assoc_profs = []
asst_profs = []

with open(input_file, encoding='utf-8') as f:
    for line in f:
        parts = [p.strip() for p in line.strip().split(',')]
        if len(parts) < 3:
            continue
        title = parts[2]
        name = f"{parts[1]} {parts[0]}"
        if title == "Professor":
            profs.append(name)
        elif title == "Associate Professor":
            assoc_profs.append(name)
        elif title == "Assistant Professor":
            asst_profs.append(name)

print("Professor:", ', '.join(profs))
print("Associate Professor:", ', '.join(assoc_profs))
print("Assistant Professor:", ', '.join(asst_profs))
