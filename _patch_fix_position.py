#!/usr/bin/env python3
"""Fix: Move the Control de Repartidores script block from wrong location to the correct </body> at end of file."""

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the start of the wrongly inserted block
start_marker = '<!-- ═══════════════════════════════════════════════════════════════\n'
start_idx = None
for i, line in enumerate(lines):
    if '     MÓDULO CONTROL DE REPARTIDORES — Script' in line:
        # The comment block starts one line before
        start_idx = i - 1
        break

if start_idx is None:
    print("ERROR: Could not find start of script block")
    exit(1)

# Find the end: the empty line after </script> (the block ends with </script>\n\n)
end_idx = None
for i in range(start_idx, min(start_idx + 500, len(lines))):
    if lines[i].strip() == '</script>' and i > start_idx + 5:
        # The block ends at the </script> line, next line is blank
        end_idx = i + 1
        # Skip any blank lines after </script>
        while end_idx < len(lines) and lines[end_idx].strip() == '':
            end_idx += 1
        break

if end_idx is None:
    print("ERROR: Could not find end of script block")
    exit(1)

print(f"Found script block at lines {start_idx+1} to {end_idx}")
print(f"Line before block: {lines[start_idx-1].rstrip()}")
print(f"Line after block: {lines[end_idx].rstrip()}")

# Extract the block (without the </body> since we'll add it back properly)
script_block = lines[start_idx:end_idx]

# The block ends with a blank line + </body>, remove the </body> since it was part of the original template string
# Actually, the original had '</body></html>`;' and our patch replaced '</body>' with the script + '</body>'
# So after our block, the line should be '</html>`;' but instead it's '</body></html>`;'
# Let me check what's on end_idx line
print(f"Line at end_idx: {lines[end_idx].rstrip()}")

# Remove the script block from its wrong position
# But we need to restore the original '</body>' that was there before
# The original line was: '</body></html>`;'  
# Our patch replaced '</body>' with [script]\n</body>
# So after the block, the next line should start with '</html>`;'
# Let's check

remaining_after = lines[end_idx].rstrip() if end_idx < len(lines) else ''
print(f"After block: '{remaining_after}'")

# Remove the block from wrong location
del lines[start_idx:end_idx]

# Now find the REAL </body> at the end of file (which should still be '</body>')
real_body_idx = None
for i in range(len(lines) - 1, max(len(lines) - 20, 0), -1):
    if lines[i].strip() == '</body>':
        real_body_idx = i
        break

if real_body_idx is None:
    print("ERROR: Could not find real </body> at end of file")
    exit(1)

print(f"Real </body> found at line {real_body_idx + 1}")

# Insert the script block before the real </body>
# The script block already has </script> at the end
script_to_insert = list(script_block)
# Add a newline before </body>
if script_to_insert and script_to_insert[-1].strip() != '':
    script_to_insert.append('\n')

for i, line in enumerate(script_to_insert):
    lines.insert(real_body_idx + i, line)

with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nFIX APPLIED SUCCESSFULLY!")
print(f"Script block moved from line ~{start_idx+1} to line ~{real_body_idx+1}")
