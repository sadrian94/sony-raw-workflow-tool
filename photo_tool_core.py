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

    def find_matching_arw(self, jpg_filename, backup_files):
        base_jpg, ext = os.path.splitext(jpg_filename)
        if ext.lower() not in ['.jpg', '.jpeg']:
            return None
        
        target_base = base_jpg.lower()
        for filename in backup_files:
            backup_base, backup_ext = os.path.splitext(filename)
            if backup_base.lower() == target_base and backup_ext.lower() == '.arw':
                return filename
        return None

    def sync_raws(self):
        if not (os.path.isdir(self.backup_dir) and os.path.isdir(self.jpg_dir) and os.path.isdir(self.arw_dir)):
            return False, 0, 0, 0
            
        jpg_files = os.listdir(self.jpg_dir)
        backup_files = os.listdir(self.backup_dir)
        
        copied = 0
        skipped = 0
        missing = 0
        
        for file in jpg_files:
            if not (file.lower().endswith('.jpg') or file.lower().endswith('.jpeg')):
                continue
                
            matching_arw = self.find_matching_arw(file, backup_files)
            if matching_arw:
                src_path = os.path.join(self.backup_dir, matching_arw)
                dst_path = os.path.join(self.arw_dir, matching_arw)
                
                if os.path.exists(dst_path):
                    skipped += 1
                else:
                    shutil.copy2(src_path, dst_path)
                    copied += 1
            else:
                missing += 1
                
        return True, copied, skipped, missing
