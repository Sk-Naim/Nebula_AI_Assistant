import re

log_path = "/Users/sknaimuddin/.gemini/antigravity/brain/df98cf83-48f0-4c0b-845f-845ce84d0777/.system_generated/logs/overview.txt"
with open(log_path, "r", encoding="utf-8") as f:
    text = f.read()

# Look for the last or first occurrence of class HudCanvas(QWidget):
# We want the content inside ui.py
# The view_file output looks like: 
# "File Path: `file:///.../ui.py`\nTotal Lines: ...\nShowing lines ...\n...1: import..."
# We can extract the latest valid view_file output.
matches = list(re.finditer(r"File Path: `file:///.*?/ui.py`(.*?)(?=\n[A-Z][a-z]+ |$)", text, re.DOTALL))
if matches:
    print(f"Found {len(matches)} view_file logs for ui.py")
    best_match = matches[0].group(1)
    
    # Extract the HudCanvas code
    hud_match = re.search(r"class HudCanvas\(QWidget\):.*?(?=class MetricBar)", best_match, re.DOTALL)
    if hud_match:
        with open("recovered_hud.py", "w") as out:
            # strip out the line numbers: "123: "
            lines = hud_match.group(0).split('\n')
            clean_lines = []
            for line in lines:
                clean_line = re.sub(r'^\d+:\s', '', line)
                clean_lines.append(clean_line)
            out.write('\n'.join(clean_lines))
        print("Recovered HudCanvas successfully to recovered_hud.py")
    else:
        print("HudCanvas not found in the view_file log.")
else:
    print("No view_file log found for ui.py")
