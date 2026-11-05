# RT-TV_Picture_Maker
This software is used to create images for the RT Lab's small TVs. It can take photos via a USB cam and merge all the images into a PDF in the correct size. 
## Usage
You can start the executable file without preparation. The start may take a while.
- Select a cam from the drop-down menu. Only numbers are displayed so far.
- Confirm your selection with "Select camera".
- Now you can take photos with "Take photo" and the photos will be displayed in the list below
- You can remove photos you have taken by clicking on them
- To save the file as a PDF, simply click on the "Save images"-button. The PDF file will be generated and then opened.
## Building on Windows

Open PowerShell in the project folder (the folder containing `src` and
`RT-TV_Picture_Maker.spec`). Install Python 3 and then install the required
packages:

```powershell
python -m pip install -r requirements.txt
```

Build the executable using the PyInstaller spec file:

```powershell
python -m PyInstaller .\RT-TV_Picture_Maker.spec
```

The executable is created at `dist\RT-TV_Picture_Maker.exe`. The spec file
builds a single-file application without a console window. To run the app
directly from source instead, use:

```powershell
python .\src\main.py
```
