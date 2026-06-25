import os

def find_matching_arw(jpg_filename, backup_files):
    base_jpg, ext = os.path.splitext(jpg_filename)
    if ext.lower() not in ['.jpg', '.jpeg']:
        return None
    
    target_base = base_jpg.lower()
    for filename in backup_files:
        backup_base, backup_ext = os.path.splitext(filename)
        if backup_base.lower() == target_base and backup_ext.lower() == '.arw':
            return filename
    return None

def validate_dirs(base_dir):
    required = ['JPG', 'backup', 'ARW']
    missing = [d for d in required if not os.path.isdir(os.path.join(base_dir, d))]
    return missing
