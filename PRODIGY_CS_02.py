import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

def encrypt_image(image_path, key):
    # Open the image
    img = Image.open(image_path)
    
    # Convert the image to a NumPy array
    img_array = np.array(img)

    # Ensure key has the same shape as img_array
    key = np.resize(key, img_array.shape)

    # Encrypt each pixel using XOR with the key
    encrypted_array = np.bitwise_xor(img_array, key)
    
    # Convert the encrypted array back to an image
    encrypted_img = Image.fromarray(encrypted_array)
    
    # Save the encrypted image
    encrypted_img.save("encrypted_image.png")
    print("Image encrypted successfully.")

def decrypt_image(encrypted_image_path, key):
    # Open the encrypted image
    encrypted_img = Image.open(encrypted_image_path)
    
    # Convert the encrypted image to a NumPy array
    encrypted_array = np.array(encrypted_img)

    # Ensure key has the same shape as encrypted_array
    key = np.resize(key, encrypted_array.shape)

    # Decrypt each pixel using XOR with the key
    decrypted_array = np.bitwise_xor(encrypted_array, key)
    
    # Convert the decrypted array back to an image
    decrypted_img = Image.fromarray(decrypted_array)
    
    # Save the decrypted image
    decrypted_img.save("decrypted_image.png")
    print("Image decrypted successfully.")

def select_image():
    global image_path
    image_path = filedialog.askopenfilename()
    if image_path:
        load_image(image_path, original_image_label)

def load_image(image_path, image_label):
    img = Image.open(image_path)
    img = img.resize((250, 250), Image.LANCZOS)  # Updated to Image.LANCZOS
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

def encrypt_image_gui():
    if not image_path:
        messagebox.showerror("Error", "Please select an image first.")
        return
    
    key = np.random.randint(0, 256, size=(3,), dtype=np.uint8)
    encrypt_image(image_path, key)
    load_image("encrypted_image.png", encrypted_image_label)
    global encryption_key
    encryption_key = key

def decrypt_image_gui():
    if encryption_key is None or encryption_key.size == 0:
        messagebox.showerror("Error", "No encryption key found. Please encrypt an image first.")
        return
    
    decrypt_image("encrypted_image.png", encryption_key)
    load_image("decrypted_image.png", decrypted_image_label)

root = tk.Tk()
root.title("Image Encryption and Decryption")
root.configure(background="#000000")
root.resizable(False, False)

style = ttk.Style()
style.configure("TFrame", background="#000000")
style.configure("TLabel", background="#000000", foreground="white", font=("Arial", 12))
style.configure("TButton", background="#2e7d32", foreground="white", font=("Arial", 12, "bold"))
style.map("TButton", background=[('active', '#1b5e20')])

frame = ttk.Frame(root, padding="10", style="TFrame")
frame.grid(row=0, column=0, sticky="nsew")

image_path = ""
encryption_key = None

ttk.Button(frame, text="Select Image", command=select_image, style="TButton").grid(row=0, column=0, pady=10)

ttk.Button(frame, text="Encrypt Image", command=encrypt_image_gui, style="TButton").grid(row=1, column=0, pady=10)

ttk.Button(frame, text="Decrypt Image", command=decrypt_image_gui, style="TButton").grid(row=2, column=0, pady=10)

original_image_label = ttk.Label(frame, style="TLabel")
original_image_label.grid(row=3, column=0, pady=10)

encrypted_image_label = ttk.Label(frame, style="TLabel")
encrypted_image_label.grid(row=4, column=0, pady=10)

decrypted_image_label = ttk.Label(frame, style="TLabel")
decrypted_image_label.grid(row=5, column=0, pady=10)

root.mainloop()