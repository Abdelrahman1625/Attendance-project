import tkinter as tk
from tkinter import filedialog
import face_recognition
import os


def load_student_images(dataset_folder):
    student_images = {}
    for folder_name in os.listdir(dataset_folder):
        folder_path = os.path.join(dataset_folder, folder_name)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(folder_path, filename)
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)
                if len(face_encodings) > 0:
                    encoding = face_encodings[0]
                    student_images[name] = (encoding, folder_name)
    return student_images


def mark_attendance(attendance_image, student_images):
    attendance_img = face_recognition.load_image_file(attendance_image)
    attendance_encodings = face_recognition.face_encodings(attendance_img)

    present_students = set()

    for attendance_encoding in attendance_encodings:
        for name, (student_encoding, folder_name) in student_images.items():
            match = face_recognition.compare_faces(
                [student_encoding], attendance_encoding)
            if match[0]:
                present_students.add(folder_name)

    return present_students


def browse_dataset_folder():
    dataset_folder = filedialog.askdirectory()
    dataset_folder_entry.delete(0, tk.END)
    dataset_folder_entry.insert(0, dataset_folder)


def browse_attendance_image():
    attendance_image = filedialog.askopenfilename()
    attendance_image_entry.delete(0, tk.END)
    attendance_image_entry.insert(0, attendance_image)


def process_attendance():
    dataset_folder = dataset_folder_entry.get()
    attendance_image = attendance_image_entry.get()
    student_images = load_student_images(dataset_folder)
    present_students = mark_attendance(attendance_image, student_images)
    result_label.config(text="Present folders: " +
                        ", ".join(present_students))


# GUI setup
root = tk.Tk()
root.title("Attendance System")

dataset_folder_label = tk.Label(root, text="Student Dataset Folder:")
dataset_folder_label.grid(row=0, column=0)

dataset_folder_entry = tk.Entry(root)
dataset_folder_entry.grid(row=0, column=1)

browse_dataset_button = tk.Button(
    root, text="Browse", command=browse_dataset_folder)
browse_dataset_button.grid(row=0, column=2)

attendance_image_label = tk.Label(root, text="Attendance Image:")
attendance_image_label.grid(row=1, column=0)

attendance_image_entry = tk.Entry(root)
attendance_image_entry.grid(row=1, column=1)

browse_attendance_button = tk.Button(
    root, text="Browse", command=browse_attendance_image)
browse_attendance_button.grid(row=1, column=2)

process_button = tk.Button(
    root, text="Process Attendance", command=process_attendance)
process_button.grid(row=2, column=1)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=3)

root.mainloop()
