import os
import shutil

class SonyWorkflowManager:
    def __init__(self, base_dir):
        self.base_dir = os.path.abspath(base_dir)
        self.backup_dir = os.path.join(self.base_dir, "backup")
        self.jpg_dir = os.path.join(self.base_dir, "JPG")
        self.arw_dir = os.path.join(self.base_dir, "ARW")
        
    def initialize_album(self):
        # Create directories
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.jpg_dir, exist_ok=True)
        os.makedirs(self.arw_dir, exist_ok=True)
        
        moved_count = 0
        copied_count = 0
        
        # Identify files in root
        for entry in os.listdir(self.base_dir):
            full_path = os.path.join(self.base_dir, entry)
            if os.path.isdir(full_path):
                continue
                
            # Exclude scripts and system files
            if entry.lower().endswith(('.py', '.md')) or entry.startswith('.'):
                continue
                
            shutil.move(full_path, os.path.join(self.backup_dir, entry))
            moved_count += 1
            
        # Copy JPGs to JPG folder
        for entry in os.listdir(self.backup_dir):
            if entry.lower().endswith(('.jpg', '.jpeg')):
                shutil.copy2(
                    os.path.join(self.backup_dir, entry),
                    os.path.join(self.jpg_dir, entry)
                )
                copied_count += 1
                
        return True, moved_count, copied_count
