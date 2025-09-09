import sys
from collections import defaultdict
from difflib import get_close_matches

def setToDict(filename):
    """Parse faculty data from file into a dictionary."""
    faculty_dict = {}
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if ":" in line:
                parts = line.split(":", 1)
                title = parts[0].strip()
                names_string = parts[1].strip()
                if names_string:
                    names_list = [name.strip() for name in names_string.split(',') if name.strip()]
                else:
                    names_list = []
                faculty_dict[title] = names_list
    return faculty_dict

def match_name(name, name_set, cutoff=0.85):
    """Find a matching name using fuzzy matching (full name, unaltered)."""
    matches = get_close_matches(name.strip(), [n.strip() for n in name_set], n=1, cutoff=cutoff)
    return matches[0] if matches else None

def find_unusual_patterns(dict1, dict2, cutoff=0.75):
    """Find names that are very similar but not exact matches."""
    names1 = {name.strip() for names in dict1.values() for name in names}
    names2 = {name.strip() for names in dict2.values() for name in names}
    unusual = defaultdict(list)
    for name1 in names1:
        close_matches = get_close_matches(name1, names2, n=3, cutoff=cutoff)
        for match in close_matches:
            if name1 != match:
                unusual[name1].append(match)
    return unusual

def compare_faculty(dict1, dict2):
    """Compare two faculty dictionaries to find changes (keep full names)."""
    new_hires = defaultdict(list)
    resigned = defaultdict(list)
    title_changes = {}
    multiple_titles = defaultdict(list)

    # Create reverse lookup maps (name -> title)
    title_map_1 = {}
    title_map_2 = {}
    for title, names in dict1.items():
        for name in names:
            if name in title_map_1:
                if isinstance(title_map_1[name], list):
                    title_map_1[name].append(title)
                else:
                    title_map_1[name] = [title_map_1[name], title]
            else:
                title_map_1[name] = title
    for title, names in dict2.items():
        for name in names:
            if name in title_map_2:
                if isinstance(title_map_2[name], list):
                    title_map_2[name].append(title)
                else:
                    title_map_2[name] = [title_map_2[name], title]
            else:
                title_map_2[name] = title

    matched_map_2 = {}
    unmatched_names_2 = set(title_map_2.keys())

    for name1 in title_map_1:
        match = match_name(name1, unmatched_names_2)
        if match:
            for name2 in unmatched_names_2:
                if name2.strip() == match:
                    matched_map_2[name1] = name2
                    unmatched_names_2.remove(name2)
                    break
        else:
            matched_map_2[name1] = None

    # Detect title changes
    for name1, match_name2 in matched_map_2.items():
        if match_name2:
            title1 = title_map_1[name1]
            title2 = title_map_2[match_name2]
            if isinstance(title1, list) or isinstance(title2, list):
                multiple_titles[name1] = {
                    "year1": title1 if isinstance(title1, list) else [title1],
                    "year2": title2 if isinstance(title2, list) else [title2]
                }
            elif title1 != title2:
                title_changes[name1] = {
                    "from": title1,
                    "to": title2
                }

    changed_names = set(title_changes.keys())
    multiple_title_names = set(multiple_titles.keys())

    # Detect new hires and resignations (excluding title changes)
    all_names_1 = set(name.strip() for names in dict1.values() for name in names)
    all_names_2 = set(name.strip() for names in dict2.values() for name in names)

    # Find new hires
    for title, names in dict2.items():
        for name in names:
            match = match_name(name, all_names_1)
            if not match:
                new_hires[title].append(name)

    # Find resignations
    for title, names in dict1.items():
        for name in names:
            matched_name = match_name(name, all_names_2)
            if not matched_name and name not in changed_names and name not in multiple_title_names:
                resigned[title].append(name)

    # Detect unusual patterns
    unusual_patterns = find_unusual_patterns(dict1, dict2)
    unusual_names = set()
    for name, matches in unusual_patterns.items():
        unusual_names.add(name)
        for match in matches:
            unusual_names.add(match)

    def filter_names(name_list):
        return [name for name in name_list if name not in unusual_names]

    new_hires = {title: filter_names(names) for title, names in new_hires.items() if filter_names(names)}
    resigned = {title: filter_names(names) for title, names in resigned.items() if filter_names(names)}

    # Create output
    print("="*70)
    print("FACULTY CHANGES REPORT")
    print("="*70)

    # Resigned Faculty
    print("\n# RESIGNED FACULTY")
    print("resigned_faculty = [")
    resigned_list = []
    for title, names in sorted(resigned.items()):
        for name in names:
            resigned_list.append(f'    "{name}",  # was {title}')
    if resigned_list:
        if len(resigned_list) > 0:
            last_item = resigned_list[-1].replace(',  #', '  #')
            resigned_list[-1] = last_item
        print("\n".join(resigned_list))
        print("]")

    # Title Changes (includes all promotions, demotions, and lateral moves)
    print("\n# TITLE CHANGES")
    print("title_changes = {")
    changes_list = []
    for name, change in sorted(title_changes.items()):
        changes_list.append(f'    "{name}": "{change["from"]} -> {change["to"]}"')
    if changes_list:
        print(",\n".join(changes_list))
    print("}")

    # Multiple Titles
    if multiple_titles:
        print("\n# FACULTY WITH MULTIPLE TITLES")
        print("multiple_titles = {")
        multi_list = []
        for name, titles in sorted(multiple_titles.items()):
            year1_titles = ", ".join(titles["year1"]) if isinstance(titles["year1"], list) else titles["year1"]
            year2_titles = ", ".join(titles["year2"]) if isinstance(titles["year2"], list) else titles["year2"]
            multi_list.append(f'    "{name}": "Year1: [{year1_titles}], Year2: [{year2_titles}]"')
        print(",\n".join(multi_list))
        print("}")

    # New Hires
    print("\n# NEW HIRES")
    print("new_hires = {")
    hires_list = []
    for title, names in sorted(new_hires.items()):
        for name in names:
            hires_list.append(f'    "{name}": "{title}"')
    if hires_list:
        print(",\n".join(hires_list))
    print("}")

    # Summary Statistics
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)

    total_resigned = sum(len(names) for names in resigned.values())
    total_new_hires = sum(len(names) for names in new_hires.values())

    print(f"\nTotal Resignations: {total_resigned}")
    print(f"Total New Hires: {total_new_hires}")
    print(f"Total Title Changes: {len(title_changes)}")
    print(f"Faculty with Multiple Titles: {len(multiple_titles)}")

    if title_changes:
        print("\nTitle Change Breakdown:")
        change_types = defaultdict(int)
        for name, change in title_changes.items():
            change_type = f"{change['from']} -> {change['to']}"
            change_types[change_type] += 1
        for change_type, count in sorted(change_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {change_type}: {count}")

    if new_hires:
        print("\nNew Hires by Title:")
        for title, names in sorted(new_hires.items()):
            print(f"  {title}: {len(names)}")

    if resigned:
        print("\nResignations by Title:")
        for title, names in sorted(resigned.items()):
            print(f"  {title}: {len(names)}")

def main():
    filename1 = "sampledata1.txt"
    filename2 = "sampledata2.txt"
    try:
        SET1 = setToDict(filename1)
        SET2 = setToDict(filename2)
        compare_faculty(SET1, SET2)
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
