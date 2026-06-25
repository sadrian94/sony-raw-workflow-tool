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

import shutil
import sys

def copy_matched_files(base_dir):
    missing_dirs = validate_dirs(base_dir)
    if missing_dirs:
        print(f"Error: Missing required folders: {', '.join(missing_dirs)}")
        return False

    jpg_dir = os.path.join(base_dir, 'JPG')
    backup_dir = os.path.join(base_dir, 'backup')
    arw_dir = os.path.join(base_dir, 'ARW')

    jpg_files = os.listdir(jpg_dir)
    backup_files = os.listdir(backup_dir)

    copied_count = 0
    skipped_count = 0
    missing_count = 0
    total_jpg = 0

    print("Starting matching and copy process...")
    print("-" * 50)

    for file in jpg_files:
        if not (file.lower().endswith('.jpg') or file.lower().endswith('.jpeg')):
            continue
        
        total_jpg += 1
        matching_arw = find_matching_arw(file, backup_files)
        
        if matching_arw:
            src_path = os.path.join(backup_dir, matching_arw)
            dst_path = os.path.join(arw_dir, matching_arw)
            
            if os.path.exists(dst_path):
                print(f"[SKIP] {matching_arw} already exists in ARW folder.")
                skipped_count += 1
            else:
                try:
                    shutil.copy2(src_path, dst_path)
                    print(f"[COPY] {matching_arw} copied successfully.")
                    copied_count += 1
                except Exception as e:
                    print(f"[ERROR] Failed to copy {matching_arw}: {e}")
        else:
            print(f"[MISSING] No matching ARW file found in backup for {file}.")
            missing_count += 1

    print("-" * 50)
    print("Process Finished Summary:")
    print(f"Total selected JPGs processed: {total_jpg}")
    print(f"Successfully copied ARWs:     {copied_count}")
    print(f"Skipped (already exists):     {skipped_count}")
    print(f"Missing in backup folder:     {missing_count}")
    return True

if __name__ == '__main__':
    base_path = os.path.dirname(os.path.abspath(__file__))
    copy_matched_files(base_path)
