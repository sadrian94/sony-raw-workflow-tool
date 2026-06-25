# Sony RAW + JPG Photo Workflow CLI Tool

A lightweight, modular, and dependency-free Python command-line utility to automate the organization and culling of Sony RAW (`.ARW`) and `.JPG` photo files.

## 📷 The Workflow

This tool is designed to support a safe, non-destructive, three-step photography workflow:

```
[Camera Import] (Mixed RAW + JPG)
       │
       ▼
 1. Initialize (photo_tool.py init)
       │
       ├─► Move all originals to /backup
       ├─► Copy JPGs to /JPG
       └─► Create empty /ARW
       │
       ▼
 2. Cull (Manual)
       │
       └─► Browse and delete unwanted photos in /JPG
       │
       ▼
 3. Synchronize (photo_tool.py sync)
       │
       └─► Copy matching .ARW raw files from /backup to /ARW
```

1. **Initialize (`init`)**: Start with a single directory containing mixed JPG and RAW files directly imported from your camera. The tool automatically moves all original files to a `backup/` folder (safety archive) and copies all JPGs to a `JPG/` folder.
2. **Cull (Manual)**: You browse and delete unwanted files inside the `JPG/` folder.
3. **Synchronize (`sync`)**: The tool compares the remaining JPG files in `JPG/` with the original files in `backup/` and copies only the matching RAW (`.ARW`) files into the `ARW/` folder for editing in Lightroom, Capture One, etc.

---

## ⚙️ Installation

### Prerequisites
* **Python 3**: The tool is written in Python and does not require any external library dependencies (no `pip install` needed).

### Getting the Tool
1. **Clone the repository**:
   ```bash
   git clone https://github.com/sadrian94/sony-raw-workflow-tool.git
   cd sony-raw-workflow-tool
   ```
2. **Setup**:
   You can either copy `photo_tool.py` and `photo_tool_core.py` directly into the directory of the photo album you want to process, or keep them in a single folder and specify your album path using the `--path` argument.

---

## 🚀 How to Use

### 1. Initialize Folder Structure
Open your terminal in the album folder and run:
```bash
python photo_tool.py init
```
This will:
* Create `backup/`, `JPG/`, and `ARW/` directories.
* Move all images and videos to `backup/` (except `.py`, `.md` and system files).
* Copy all `.JPG` / `.JPEG` files to `JPG/`.

*Note: You can also specify an absolute or relative path:*
```bash
python photo_tool.py init --path /path/to/your/album
```

### 2. Cull Your Photos
Open the `JPG/` folder in your favorite photo viewer. **Delete** any photos you do not want to edit or keep.

### 3. Sync Selected RAWs
Once you're done culling, run:
```bash
python photo_tool.py sync
```
This will:
* Read the remaining files in `JPG/`.
* Perform a **case-insensitive** base-name match.
* Copy corresponding `.ARW` raw files from `backup/` to `ARW/`.
* Preserve original file metadata and creation/modification timestamps.
* Automatically skip files that have already been copied to save time.

---

## 🧪 Testing

The tool includes a robust suite of unit and integration tests. To run the tests, execute:
```bash
python test_photo_tool.py
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository on GitHub.
2. **Create a branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Write clean, modular code and add matching tests to `test_photo_tool.py`.
4. Run the test suite and ensure all tests pass.
5. **Commit** your changes with descriptive commit messages.
6. **Push** to your branch and submit a **Pull Request**.

## 📄 License

This project is licensed under the MIT License.
