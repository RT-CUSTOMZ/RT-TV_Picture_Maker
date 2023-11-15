from distutils.core import setup
import py2exe

import cv2
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import tkinter as tk
from PIL import Image, ImageTk
import os

# setup(console=["src/main.py"])

setup(
    options={"py2exe": {"bundle_files": 1, "compressed": True}},
    windows=[{"script": "src/main.py"}],
    zipfile=None,
)
