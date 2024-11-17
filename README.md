## Dev

1. Install uv 
    ```
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
2. Install Visual Studio Code with "Desktop development with C++" component
3. In Windows > System > For developers, enable developer mode.
5. In VS Code, install Flutter extension. Put the Flutter SDK in `C:\dev` or something
6. Install Tesseract OCR for Windows ([download](https://github.com/UB-Mannheim/tesseract/wiki))
7. `pip install -r requirements.txt`

### Visual Studio Code

`Ctrl + Shift + P` and select `Ptyhon: Select Interpreter` so that Visual Studio can see packages.


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

