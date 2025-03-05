# ABOUT:

Initially this project is created to run as a script on backends of any organisation related to storing and processing of documents containing personal identifiable information. Currently this script is embeded with graphic user interface. 

# INSTALLATION AND SET-UP:

--clone this repo in your system
--download Teseract-OCR-setup.exe from https://github.com/UB-Mannheim/tesseract/wiki
--run the setup and choose the file location of this repository.(or change the file locations of the same in python-script files)
--create a virtual enviroment "envirnment_venv"(optional){note: if you are not using venv then change the file locations of the same
  in python-script files accordingly}     
--install required dependencies/libraries
  -pip install tk
  -pip install customtkinter
  -pip install pillow
  -pip install pytesseract
  -pip install langchain
  -pip install langchain-experimental
  -pip install presidio-analyser
  -pip install presidio-anonymizer
  -pip install pymupdf
  -pip install faker
  -pip install opencv-python
  -pip install pyzbar
--create a folder "temp" in the same repository
--working directory should be repository itself, run code/gui.py

FILE STRUCTURE:
  [
    PII MASKING TOOL
      code
        gui.py
        pii_check.py
        pii_mask.py
      temp
      Tesseract-OCR
      environment-venv(optional)
      readme.md
  ]
