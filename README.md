## Dev

1. Install uv
2. Install Visual Studio Code with "Desktop development with C++" component
3. In VS Code, install Flutter


## Production and 

1. Install Tesseract OCR for Windows ([download](https://github.com/UB-Mannheim/tesseract/wiki))


### Visual Studio

Ctrl + Shift + P and select `Ptyhon: Select Interpreter` so that Visual Studio can see packages.


### Working with uv

``` bash
# Activate the environment
source .venv/Scripts/activate

# Install something
uv pip install flet
uv pip install pytesseract

# Run a flet application
flet run ./revit-assist/counter.py

# Building a flet windows application
cd src
flet build windows -o ../build --module-name counter

```

