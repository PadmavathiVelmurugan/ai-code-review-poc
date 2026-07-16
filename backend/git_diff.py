import os
from git import Repo

def get_modified_lines_only(repo_path):
    repo = Repo(repo_path)
    
    # Handle initial commit check safely
    try:
        base = repo.commit("HEAD~1")
    except Exception:
        # Fallback if there is no parent commit
        base = "4b825dc642cb6eb9a030e54bf8d69288fbee4904"

    # Generate structured diff against HEAD, creating patch data
    diffs = repo.commit("HEAD").diff(base, create_patch=True)
    
    review_payload = {}

    for diff in diffs:
        # Ensure the file is a Java file and wasn't deleted
        if diff.b_path and diff.b_path.endswith(".java") and diff.change_type in ['A', 'M', 'R']:
            file_path = os.path.normpath(diff.b_path)
            
            # Decode the raw cryptographic patch data into text
            patch_text = diff.diff.decode('utf-8', errors='ignore')
            
            added_lines = []
            current_line_num = 0

            # Parse the unified diff format hunk by hunk
            for line in patch_text.splitlines():
                # Locate the unified diff hunk header, e.g., @@ -10,4 +15,6 @@
                if line.startswith('@@'):
                    # Target the target file line count (the "+15,6" portion)
                    target_info = line.split('+')[1].split(' ')[0]
                    # Set the starting line number for this hunk
                    current_line_num = int(target_info.split(',')[0])
                
                # Identify explicitly added lines (skip '+++' file header)
                elif line.startswith('+') and not line.startswith('+++'):
                    added_lines.append({
                        "line_number": current_line_num,
                        "content": line[1:]  # Strip the leading '+' character
                    })
                    current_line_num += 1
                
                # Track unchanged contextual lines to maintain correct line counting
                elif not line.startswith('-'):
                    current_line_num += 1

            if added_lines:
                review_payload[file_path] = added_lines

    return review_payload
