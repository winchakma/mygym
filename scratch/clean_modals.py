import os
import re

def remove_redundant_modal(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all authModal blocks
    # Pattern: <div id="authModal" class="modal-overlay hidden"> ... </div>
    # This is tricky because of nested divs, but the modals usually have a specific structure.
    
    modal_matches = list(re.finditer(r'<div id="authModal" class="modal-overlay hidden">', content))
    
    if len(modal_matches) > 1:
        print(f"Found {len(modal_matches)} modals in {filepath}. Removing redundant ones...")
        
        # We keep the first one and remove the rest.
        # However, we need to find the end of the div.
        # For simplicity, since the redundant ones are usually at the end and follow a pattern:
        # <!-- AUTH MODAL --> ... </div>
        
        # Let's try to find the block starting with <!-- AUTH MODAL --> and remove it if it's redundant.
        blocks = list(re.finditer(r'<!-- AUTH MODAL -->\s*<div id="authModal"', content))
        if len(blocks) > 0:
            # If there's an explicit "AUTH MODAL" comment, and we have multiple modals, 
            # we check if the comment precedes a redundant modal.
            
            # Actually, a simpler way: find the last occurrence of id="authModal" 
            # and remove from its start to the next </div> that closes the modal-overlay.
            
            # Since these files are small enough, we can use a more robust approach.
            last_modal_start = content.rfind('<div id="authModal"')
            first_modal_start = content.find('<div id="authModal"')
            
            if last_modal_start != first_modal_start:
                # Find the start of the block (maybe including the comment)
                block_start = content.rfind('<!-- AUTH MODAL -->', 0, last_modal_start)
                if block_start == -1:
                    block_start = last_modal_start
                
                # Find the end of the modal-overlay div.
                # The modals are usually self-contained. We'll look for the next </div> that matches the depth.
                # Or just look for the </div> that closes the modal-overlay.
                
                # Search for the closing tag of the modal-overlay.
                # We'll look for the next </div> after the last </div> inside the content.
                # This is risky. Let's use a more specific search.
                
                # In these files, the redundant modal usually ends with a specific sequence.
                # For index.html it was: </form>\n    </div>\n  </div>
                
                # Let's try to find the end by counting braces or just looking for the next </div></div>
                end_search = content.find('</div>', last_modal_start)
                if end_search != -1:
                    next_div = content.find('</div>', end_search + 6)
                    if next_div != -1:
                        block_end = next_div + 6
                        new_content = content[:block_start] + content[block_end:]
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Removed redundant modal from {filepath}")
                        return True
    return False

frontend_dir = 'frontend'
for filename in os.listdir(frontend_dir):
    if filename.endswith('.html'):
        remove_redundant_modal(os.path.join(frontend_dir, filename))
