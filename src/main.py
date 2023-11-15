import cv2
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import tkinter as tk
from PIL import Image, ImageTk
import os

outline_ratio = 4 / 3

cap = None
panel = None
picture_queue = []
picture_canvas = None
picture_listbox = None
pic_counter = 0
photo_images = []
photo_path = "photos"


def get_camera_list():
    camera_list = []
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camera_list.append(i)
            cap.release()
    return camera_list


def select_camera():
    global cap
    cap = cv2.VideoCapture(int(camera_var.get()))
    show_frame()


def get_crop_rect(frame):
    width, height = frame.shape[1], frame.shape[0]
    if width / height > outline_ratio:
        crop_width = int(height * outline_ratio)
        crop_height = height
    else:
        crop_width = width
        crop_height = int(width / outline_ratio)

    x = int((frame.shape[1] - crop_width) / 2)
    y = int((frame.shape[0] - crop_height) / 2)
    return (x, y, x + crop_width, y + crop_height)


def show_frame():
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    x, y, x2, y2 = get_crop_rect(frame)
    # Draw the outline on the preview window
    cv2.rectangle(
        frame,
        (x, y),
        (x2, y2),
        (0, 255, 0),
        2,
    )
    image = Image.fromarray(frame)
    photo = ImageTk.PhotoImage(image)
    global panel
    if panel is None:
        panel = tk.Label(image=photo)
        panel.image = photo
        panel.pack()
    else:
        panel.configure(image=photo)
        panel.image = photo
    root.after(10, show_frame)  # Refresh after 10ms


def redrawCanvas():
    global picture_canvas
    gap = 5
    picture_canvas.delete("all")
    for i, photo in enumerate(photo_images):
        image_item = picture_canvas.create_image(
            0 + i * (photo.width() + gap), 0, image=photo, anchor=tk.NW
        )

        def deleteImage(event):
            # picture_canvas.delete(image_item)
            picture_queue.remove(picture_queue[i])
            photo_images.remove(photo)
            redrawCanvas()

        picture_canvas.tag_bind(image_item, "<Button-1>", deleteImage)
    picture_canvas.config(
        scrollregion=(0, 0, len(photo_images) * (photo.width() + gap), photo.height())
    )


def take_picture():
    global pic_counter, picture_canvas
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    x, y, x2, y2 = get_crop_rect(frame)
    resized_image = frame[y:y2, x:x2]
    image = Image.fromarray(resized_image)
    picture_name = f"pic{pic_counter}.jpg"
    pic_counter += 1
    # cv2.imwrite(picture_name, resized_image)  # wrong colors
    image.save(photo_path + "/" + picture_name)
    picture_queue.append(picture_name)

    # Open the image, resize it, and add it to the Canvas
    # image = Image.open(picture_name)
    scaled_width = int((x2 - x) * 0.2)
    scaled_height = int((y2 - y) * 0.2)
    image = image.resize(
        (scaled_width, scaled_height), Image.LANCZOS
    )  # Resize the image
    photo = ImageTk.PhotoImage(image)
    photo_images.append(photo)

    redrawCanvas()
    return

    image_item = picture_canvas.create_image(
        0 + photo_images.__len__() * scaled_width, 0, image=photo, anchor=tk.NW
    )

    def deleteImage(event):
        picture_canvas.delete(image_item)
        photo_images.remove(photo)

    picture_canvas.tag_bind(image_item, "<Button-1>", deleteImage)

    # # Calculate the position to center the image on the page
    # x = (A4[0] - 48 * mm) / 2
    # y = (A4[1] - 38 * mm) / 2
    # pdf.drawImage("pic.jpg", x, y, 48 * mm, 38 * mm)
    # pdf.save()
    # root.destroy()


def save_pictures_to_pdf():
    margin = 5 * mm
    gap = 2 * mm
    width = 48 * mm
    height = 38 * mm
    pdf = canvas.Canvas("output.pdf", pagesize=A4)
    x = margin
    y = margin
    for picture in picture_queue:
        pdf.drawImage(photo_path + "/" + picture, x, y, width, height)
        x += width + gap
        if x > A4[0] - width - margin:
            x = margin
            y += height + gap
        if y > A4[1] - height - margin:
            pdf.showPage()
            x = margin
            y = margin
    pdf.save()
    os.system("output.pdf")


# Create a GUI window
root = tk.Tk()
# root.geometry("800x600")
root.title("RT-TV Picture Maker")

# make a folder for the photos
if not os.path.exists(photo_path):
    os.makedirs(photo_path)

# Create a dropdown menu to select the camera
camera_var = tk.StringVar()
camera_var.set(str(get_camera_list()[0]))
camera_dropdown = tk.OptionMenu(root, camera_var, *get_camera_list())
camera_dropdown.pack()

# Create a button to select the camera
select_button = tk.Button(root, text="Select Camera", command=select_camera)
select_button.pack()

# Create a button to take a picture
take_picture_button = tk.Button(root, text="Take Picture", command=take_picture)
take_picture_button.pack()

save_button = tk.Button(root, text="Save Pictures", command=save_pictures_to_pdf)
save_button.pack()

picture_canvas = tk.Canvas(
    root, width=800, height=100, bg="white", scrollregion=(0, 0, 0, 0)
)
picture_canvas.pack()
hbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
hbar.pack(fill=tk.X)
hbar.config(command=picture_canvas.xview)
picture_canvas.config(xscrollcommand=hbar.set)

# Create a new PDF document with an A4 page
# pdf = canvas.Canvas("output.pdf", pagesize=A4)

# Start the GUI loop
root.mainloop()


# Release the webcam
if cap is not None:
    cap.release()

# delete the photos folder with all the pictures without shutil
for file in os.listdir(photo_path):
    os.remove(photo_path + "/" + file)
os.rmdir(photo_path)

# Close the preview window
cv2.destroyAllWindows()
