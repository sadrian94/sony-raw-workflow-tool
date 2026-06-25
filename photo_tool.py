import argparse
import sys
import os
from photo_tool_core import SonyWorkflowManager

def main():
    parser = argparse.ArgumentParser(
        description="Sony RAW + JPG Photo Workflow CLI Tool Manager"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Init subcommand
    init_parser = subparsers.add_parser(
        "init", help="Initialize album: moves all files to backup/ and copies JPGs to JPG/"
    )
    init_parser.add_argument(
        "--path", default=".", help="Base directory path of the album (default: current directory)"
    )
    
    # Sync subcommand
    sync_parser = subparsers.add_parser(
        "sync", help="Sync raw files: copies matching ARWs from backup/ to ARW/ based on JPG/"
    )
    sync_parser.add_argument(
        "--path", default=".", help="Base directory path of the album (default: current directory)"
    )
    
    args = parser.parse_args()
    
    manager = SonyWorkflowManager(args.path)
    
    if args.command == "init":
        print(f"Initializing folder structure at: {manager.base_dir}")
        success, moved, copied = manager.initialize_album()
        if success:
            print("Initialization Complete:")
            print(f"- Files moved to backup/: {moved}")
            print(f"- JPGs copied to JPG/:    {copied}")
        else:
            print("Error occurred during initialization.")
            sys.exit(1)
            
    elif args.command == "sync":
        print(f"Syncing selected RAW files at: {manager.base_dir}")
        success, copied, skipped, missing = manager.sync_raws()
        if success:
            print("Sync Complete:")
            print(f"- Successfully copied ARWs: {copied}")
            print(f"- Skipped (already exists): {skipped}")
            print(f"- Missing in backup folder: {missing}")
        else:
            print("Error: Missing one of the required folders: backup/, JPG/, or ARW/.")
            sys.exit(1)

if __name__ == "__main__":
    main()
