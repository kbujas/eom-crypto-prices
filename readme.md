Prerequisites

1. Install Python 3.7 or later from the official Python website: https://www.python.org/downloads/.


2. Ensure pip (Python's package manager) is installed.


3. (Optional) Install Git if you plan to clone the repository.


Instructions

Step 1: Get the Project Files

1. Clone the repository using Git:
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

OR

2. Download the repository as a ZIP file from GitHub, extract it, and navigate to the project folder.


Step 2: Set Up a Virtual Environment

1. Open a terminal and navigate to the project folder:
cd path/to/your/project-folder


2. Create a virtual environment:
python -m venv venv


3. Activate the virtual environment:

On Windows: venv\Scripts\activate

On macOS/Linux: source venv/bin/activate



Step 3: Install Dependencies

1. Ensure the virtual environment is active.


2. Install required packages:
pip install -r requirements.txt




---

Step 4: Run the Application

1. Make sure the virtual environment is active.


2. Run the application with:
python main.py


Troubleshooting

If you encounter errors like "command not found," ensure Python and pip are properly installed and added to your system's PATH.

Upgrade pip if needed: pip install --upgrade pip