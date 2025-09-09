#!/usr/bin/env python3
"""
Faculty/Staff Directory Line Merger
Converts multi-line directory entries into single-line format.
Handles both multi-line files and single-line concatenated files.
"""

import re
import sys
import argparse

class FacultyEntryMerger:
    def __init__(self):
        # Comprehensive pattern for detecting faculty/staff names
        # Handles: LASTNAME, FIRSTNAME/INITIALS (allows parens and spaces), Title
        self.name_pattern = re.compile(
            r'^'
            r'(?:'
                r'(?:Mc|Mac)[A-Z][a-zA-Z]+|'           # McADOO, MacARTHUR
                r"(?:O['’`])[A-Z][a-zA-Z]+|"           # O'CONNOR, O’CONNOR, O`CONNOR
                r"[A-Z][A-ZÀ-ÿ\-–—''\s]*[A-ZÀ-ÿ]+"     # Regular all-caps surnames (SMITH, VAN DYKE)
            r')'
            r',\s*'                                      # Comma and space after surname
            r'[A-Z][A-Za-z\.\-\s\(\)]*[A-Za-z\.]'        # First name(s) (allows parens/nicknames/multiword)
            r',\s+'                                      # Comma and space(s)
            r'[A-Za-z]'                                  # Title/position starts with a letter
        )

        # Words that should NOT start an entry (job titles, positions)
        self.exclude_patterns = [
            r'^(Assistant|Associate|Assoc\.|Asst\.)\s+',
            r'^(Director|Dir\.|Manager|Mgr\.)\s+',
            r'^(Specialist|Coordinator|Admin)\s+',
            r'^(Extension|Ext\.|External)\s+',
            r'^(Emeritus|Emerita)\s+',
            r'^(Professor|Prof\.|Instructor|Instr\.)\s+',
            r'^(Engineering|Sciences|Business|Education)\s+',
            r'^(Department|Dept\.|Division|Div\.)\s+',
            r'^(County|Co\.|State|St\.)\s+',
            r'^(Agent|Representative|Rep\.)\s+',
        ]
        
    def is_valid_entry_start(self, line):
        """
        Check if a line starts a new faculty/staff entry.
        Returns True only for valid name patterns.
        """
        line = line.strip()

        # Empty lines are not entries
        if not line:
            return False

        # First check if it matches our name pattern
        if not self.name_pattern.match(line):
            return False

        # Then check it's not a false positive (job title, etc.)
        for exclude in self.exclude_patterns:
            if re.match(exclude, line, re.IGNORECASE):
                return False

        # Additional validation: check the part before first comma
        first_comma = line.find(',')
        if first_comma > 0:
            potential_surname = line[:first_comma].strip()

            # Check for valid surname patterns
            # Mc/Mac prefixes
            if potential_surname.startswith(('Mc', 'Mac')):
                # Should have at least 3 more characters after prefix
                if len(potential_surname) >= 5:
                    return True
            # O' prefixes (including curly and grave apostrophe)
            elif potential_surname.startswith(("O'", "O’", "O`")):
                # Should have at least 2 more characters after O'
                if len(potential_surname) >= 4:
                    return True
            # Regular surnames - should be mostly uppercase
            elif len(potential_surname) >= 2:
                # Count uppercase vs lowercase letters
                upper_count = sum(1 for c in potential_surname if c.isupper())
                alpha_count = sum(1 for c in potential_surname if c.isalpha())
                # At least 70% uppercase letters (allows for hyphens, apostrophes, etc.)
                if alpha_count > 0 and upper_count / alpha_count >= 0.7:
                    return True

        return False

    def extract_entries_from_single_line(self, content):
        """
        Extract entries from a file where everything is on one line.
        Matches multi-word/multi-symbol first names and nicknames in parentheses.
        """
        entries = []

        # Pattern matches surname, first names (with parens, spaces, hyphens, etc.), ending at comma after given names.
        finder_pattern = re.compile(
            r'(?:Mc|Mac)[A-Z][a-zA-Z]+,\s*[A-Z][A-Za-z\.\-\s\(\)]*,|'
            r"(?:O['’`])[A-Z][a-zA-Z]+,\s*[A-Z][A-Za-z\.\-\s\(\)]*,|"
            r'[A-Z][A-ZÀ-ÿ\-–—\'\s]*[A-ZÀ-ÿ]+,\s*[A-Z][A-Za-z\.\-\s\(\)]*,'
        )

        positions = [m.start() for m in finder_pattern.finditer(content)]
        # If the first match isn't at 0, add the beginning
        if positions and positions[0] != 0:
            positions = [0] + positions
        if not positions:
            return [content.strip()]
        for i, start in enumerate(positions):
            end = positions[i + 1] if i + 1 < len(positions) else len(content)
            entry = content[start:end].strip()
            if entry:
                entries.append(entry)
        return entries

    def merge_multiline_entries(self, lines):
        """
        Merge entries that span multiple lines.
        """
        entries = []
        current_entry = []

        for line in lines:
            line = line.rstrip()

            # Skip empty lines when not building an entry
            if not line and not current_entry:
                continue

            # Check if this starts a new entry
            if self.is_valid_entry_start(line):
                # Save previous entry if exists
                if current_entry:
                    merged = ' '.join(current_entry)
                    entries.append(merged)

                # Start new entry
                current_entry = [line]
            else:
                # Continue current entry (only non-empty lines)
                if line:
                    current_entry.append(line)

        # Don't forget the last entry
        if current_entry:
            merged = ' '.join(current_entry)
            entries.append(merged)

        return entries

    def process_file(self, input_file, output_file):
        """
        Main processing function - handles both file formats.
        """
        try:
            # Read the input file
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Determine file format
            lines = content.strip().split('\n')

            # Check if it's a single-line format
            is_single_line = (
                (len(lines) == 1 and len(lines[0]) > 500) or
                (len(lines) <= 3 and len(content) > 1000 and 
                 any(len(line) > 1000 for line in lines))
            )

            # Process accordingly
            if is_single_line:
                print("📄 Detected single-line format")
                entries = self.extract_entries_from_single_line(content)
            else:
                print("📄 Detected multi-line format")
                entries = self.merge_multiline_entries(lines)

            # Write output
            with open(output_file, 'w', encoding='utf-8') as f:
                for entry in entries:
                    f.write(entry + '\n')

            # Report results
            print(f"✅ Successfully processed {len(entries)} entries")
            print(f"📁 Output written to: {output_file}")

            # Show statistics
            self.show_statistics(entries)

            return entries

        except FileNotFoundError:
            print(f"❌ Error: Input file '{input_file}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

    def show_statistics(self, entries):
        """
        Display statistics about processed entries.
        """
        mc_count = sum(1 for e in entries if e.startswith('Mc'))
        mac_count = sum(1 for e in entries if e.startswith('Mac'))
        o_count = sum(1 for e in entries if e.startswith(("O'", "O’", "O`")))

        print(f"\n📊 Statistics:")
        print(f"   • Names starting with 'Mc': {mc_count}")
        print(f"   • Names starting with 'Mac': {mac_count}")
        print(f"   • Names starting with O' (all types): {o_count}")

        # Check for potential issues
        issues = []
        problem_starts = ['Engineering', 'Emeritus', 'Extension', 'Associate', 'Assistant']

        for i, entry in enumerate(entries):
            for prob in problem_starts:
                if entry.startswith(prob):
                    issues.append((i + 1, prob, entry[:50] + '...'))

        if issues:
            print(f"\n⚠️  Potential issues found ({len(issues)}):")
            for line_num, word, excerpt in issues[:5]:  # Show first 5
                print(f"   Line {line_num}: Starts with '{word}' - {excerpt}")
        else:
            print("\n✅ No formatting issues detected!")

    def preview_output(self, output_file, num_lines=5):
        """
        Show preview of output file.
        """
        print(f"\n📋 Preview of first {num_lines} entries:")
        print("─" * 80)

        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i >= num_lines:
                        break
                    line = line.strip()
                    if len(line) > 120:
                        line = line[:117] + "..."
                    print(f"{i+1:3d}. {line}")
        except Exception as e:
            print(f"Could not preview output: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Merge multi-line faculty/staff directory entries into single lines."
    )
    parser.add_argument(
        'input_file',
        nargs='?',
        default='file.txt',
        help='Input file (default: file.txt)'
    )
    parser.add_argument(
        'output_file',
        nargs='?',
        default='faculty_single_line.txt',
        help='Output file (default: faculty_single_line.txt)'
    )
    parser.add_argument(
        '--preview',
        type=int,
        default=5,
        help='Number of entries to preview (default: 5)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run with test data to verify functionality'
    )
    args = parser.parse_args()
    if args.test:
        run_tests()
        return
    print(f"🔄 Processing: {args.input_file}")
    merger = FacultyEntryMerger()
    merger.process_file(args.input_file, args.output_file)
    if args.preview > 0:
        merger.preview_output(args.output_file, args.preview)

def run_tests():
    """
    Run tests to verify the merger works correctly.
    """
    print("🧪 Running tests...\n")
    test_data = """O’CONNOR, MARY J., Prof. of Biology
(1998). BS 1993, MS 1995, PhD 1998, Yale U.
XIN, XIAO JIANG (JACK), Asst. Prof. of Mechanical and Nuclear Engineering (1998). BS 1985, U. of Science and Tech.of China; PhD 1992, U. of Sheffield, UK. (*)
O'CONNOR, JAMES B., Prof. of Mathematics
(1992). BS 1987, MS 1990, PhD 1992, Harvard U.
O`NEILL, PATRICK, Assoc. Prof. of History
(1970). BA 1966, MA 1968, PhD 1970, Oxford U.
MCADOO, ROBERT S., Prof. Emeritus of Consumer
Sciences (1990). BA 1985, MS 1987, PhD 1990, Cornell U."""
    with open('test_input.txt', 'w', encoding='utf-8') as f:
        f.write(test_data)
    merger = FacultyEntryMerger()
    entries = merger.process_file('test_input.txt', 'test_output.txt')
    print("\n✅ Test Results:")
    print(f"   • O' names found: {sum(1 for e in entries if e.startswith(('O\'', 'O’', 'O`')))} (expected: 3)")
    print(f"   • Mc names found: {sum(1 for e in entries if e.startswith('Mc'))} (expected: 1)")
    print(f"   • XIN names found: {sum(1 for e in entries if e.startswith('XIN'))} (expected: 1)")
    for entry in entries:
        print(f"   • {entry[:80]}...")
    import os
    os.remove('test_input.txt')
    os.remove('test_output.txt')
    print("\n🎉 Tests completed!")

if __name__ == "__main__":
    main()
