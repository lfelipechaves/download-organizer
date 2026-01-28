📂 Download Organizer

Automatic download folder organizer built with Python.
This script monitors your Downloads folder in real time and automatically organizes files into folders based on file extension and file name patterns.

✨ Features

📁 Organizes files by extension (Documents, Images, Compressed, etc.)

🧠 Uses simple “AI” logic based on file names (e.g. boleto, nota, print)

⚡ Runs automatically in the background

🛡️ Prevents file overwrite by renaming duplicates

🔒 Thread-safe (one file processed at a time)

🗂 Folder Structure (example)

Downloads/
├── Documentos/
├── Imagens/
├── Compactados/
├── Outros/

Folders are created automatically if they do not exist.

🛠 Requirements

Python 3.10+

watchdog

Install dependencies:

pip install watchdog

▶️ How to Run

Clone the repository:

git clone git clone https://github.com/lfelipechaves/download-organizer.git

Enter the project folder:

cd download-organizer

Run the script:

python main.py

You should see:

📂 Monitorando Downloads...

⏹ How to Stop

Press:
CTRL + C

🧪 Testing

Recommended way to test:

Run the script

Download or copy files into the Downloads folder

The files will be automatically moved

You can also delete the category folders and verify that the script recreates them automatically.

🚀 Future Improvements

Organize existing files on startup (not only new ones)

Configuration file (custom folders and extensions)

Windows service / background app

GUI (desktop app)

Cross-platform support

📌 Notes
Temporary download files (.crdownload, .tmp, .part) are ignored

If a file already exists, the script creates:

file.txt
file_1.txt
file_2.txt

📄 License

This project is open-source and free to use.
