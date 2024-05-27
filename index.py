from initialization import *
from ocr import *

def play_animation_and_extract():
    def update_animation(frame_number):
        frame = gif_frames[frame_number]
        frame = frame.resize((640, 360), Image.LANCZOS)
        frame_photo = ImageTk.PhotoImage(frame)
        gif_label.configure(image=frame_photo)
        gif_label.image = frame_photo

        root.after(10, update_animation, (frame_number + 1) % len(gif_frames))

    def extract_after_animation():
        extract_data_from_image()
        gif_label.pack_forget()

    gif_label = tk.Label(root)
    gif_label.pack(pady= 50)

    gif_path = extractGif
    gif = Image.open(gif_path)

    gif_frames = []

    try:
        while True:
            gif_frames.append(gif.copy())
            gif.seek(len(gif_frames))
    except EOFError:
        pass

    question_label.pack_forget()
    extract_frame.pack_forget()
    image_label.pack_forget()
    title_label.config(text="Extracting Data...")
    update_animation(0)
    root.after(1000, extract_after_animation)

def reset_interface():
    global left_value_frame, right_value_frame, num_converted_files, jpg_counter
    image = Image.open(resetIMG)
    image = image.resize((150, 150), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.photo = photo
    image_label.pack(pady=30)
    title_label = tk.Label(root, text="Invoice Processing Tool", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
    title_label.pack(pady=20)
    num_converted_files = 0
    jpg_counter = 0

    question_label.config(text="Select a file/folder with the extension .pdf or .jpg in order to proceed with the processing", font=("Helvetica", 14), bg="#f0f0f0", fg="#7d7d7d", wraplength=500)
    question_label.pack(pady=20)
    start_frame.pack(pady=50)

    if left_value_frame is not None:
        left_value_frame.pack_forget()
    if right_value_frame is not None:
        right_value_frame.pack_forget()
    if scroll_y is not None:
        scroll_y.pack_forget()
    if canvas is not None:
        canvas.pack_forget()

    if  separator is not None:
        separator.pack_forget()

    title_label.pack_forget()
    file_loc_frame.pack_forget()
    button_frame.pack_forget()
    extract_frame.pack_forget()
    CSV_frame.pack_forget()

def extract_data_after_conversion():
    global selected_image_filename, selected_pdf_name, num_converted_files, selected_item

    if selected_image_filename or num_converted_files > 0:
        data_image_path = dataIMG
        data_image = Image.open(data_image_path)
        data_image = data_image.resize((150, 150), Image.LANCZOS)
        data_photo = ImageTk.PhotoImage(data_image)

        image_label.config(image=data_photo)
        image_label.photo = data_photo

        image_name = os.path.basename(selected_image_filename)

        if selected_pdf_name:
            question_label.config(text=f"Do you want to extract the data of {image_name}?")
            selected_item = selected_image_filename
        else:
            question_label.config(text=f"Do you want to extract the data of the {num_converted_files} converted files?")
 
        file_loc_frame.pack_forget()
        extract_frame.pack(pady=50)

def convert_pdf_to_jpg():
    global pdf_directory, selected_pdf_name, jpg_filename, selected_image_filename, num_converted_files

    if selected_pdf_name:
        jpg_filename = selected_pdf_name.replace(".pdf", "") + ".jpg"
        jpg_filepath = filedialog.asksaveasfilename(defaultextension=".jpg", initialfile=jpg_filename, filetypes=[("JPEG Files", "*.jpg")],  title="Select a folder to save converted JPG")

        if jpg_filepath:
            pdf_path = os.path.join(pdf_directory, selected_pdf_name)
            images = convert_from_path(pdf_path)
            
            if images:
                image = images[0]
                image.save(jpg_filepath, "JPEG")

                selected_image_filename = jpg_filepath

                question_label.config(text=f"{jpg_filename} has been successfully converted and saved in the selected folder.")
                button_frame.pack_forget()
                file_loc_frame.pack(side=tk.TOP, pady=50)

    else:
        if jpg_counter == 0:  # No JPGs in the folder, so it's likely a folder with only PDFs
            jpg_folder = filedialog.askdirectory(title="Select a folder to save converted JPGs")

            if jpg_folder:
                pdf_files = [file for file in os.listdir(pdf_directory) if file.lower().endswith(".pdf")]

                for pdf_filename in pdf_files:
                    pdf_path = os.path.join(pdf_directory, pdf_filename)
                    images = convert_from_path(pdf_path)

                    if images:
                        jpg_filename = pdf_filename.replace(".pdf", "") + ".jpg"
                        jpg_filepath = os.path.join(jpg_folder, jpg_filename)

                        for i, image in enumerate(images):
                            jpg_filepath = os.path.join(jpg_folder, f"{jpg_filename.replace('.jpg', '')}_{i + 1}.jpg")
                            image.save(jpg_filepath, "JPEG")
                            num_converted_files += 1

                question_label.config(text="All PDF files have been successfully converted into JPG inside the selected folder.")
                button_frame.pack_forget()
                file_loc_frame.pack(side=tk.TOP, pady=50)
        else:  # Folder contains both PDFs and JPGs, convert PDFs to JPGs in the same folder
            pdf_files = [file for file in os.listdir(pdf_directory) if file.lower().endswith(".pdf")]
            pdf_counter = 0

            for pdf_filename in pdf_files:
                pdf_path = os.path.join(pdf_directory, pdf_filename)
                images = convert_from_path(pdf_path)

                if images:
                    jpg_filename = pdf_filename.replace(".pdf", "") + ".jpg"
                    jpg_filepath = os.path.join(pdf_directory, jpg_filename)

                    for i, image in enumerate(images):
                        jpg_filepath = os.path.join(pdf_directory, f"{jpg_filename.replace('.jpg', '')}_{i + 1}.jpg")
                        image.save(jpg_filepath, "JPEG")
                        pdf_counter += 1

            question_label.config(text=f"{pdf_counter} PDF files have been converted into JPG inside the {selected_folder_name} folder.")
            button_frame.pack_forget()
            file_loc_frame.pack(side=tk.TOP, pady=50)
            num_converted_files = pdf_counter + jpg_counter

def select_file_image_file(is_folder=False):
    global pdf_directory, selected_pdf_name, image_label, selected_image_filename, jpg_files, pdf_files, pdf_counter, jpg_counter, selected_folder_name, selected_item

    if is_folder:
        selected_item = filedialog.askdirectory(title="Select a folder")
        if selected_item:
            folder_contents = os.listdir(selected_item)
            jpg_files = [file for file in folder_contents if os.path.splitext(file)[-1].lower() == ".jpg"]
            pdf_files = [file for file in folder_contents if os.path.splitext(file)[-1].lower() == ".pdf"]

            if len(jpg_files) == 0 and len(pdf_files) == 0:
                show_message_popup("The selected folder does not contain any PDF or JPG files.", success=False)
            elif len(jpg_files) > 0 and len(pdf_files) > 0:
                jpg_counter = len(jpg_files)
                pdf_counter = len(pdf_files)
                selected_pdf_name = None
                selected_folder_name = os.path.basename(selected_item)
                pdf_directory = selected_item

                pdf_image_path = pdftojpgIMG
                pdf_image = Image.open(pdf_image_path)
                pdf_image = pdf_image.resize((300, 150), Image.LANCZOS)
                pdf_photo = ImageTk.PhotoImage(pdf_image)

                image_label.config(image=pdf_photo)
                image_label.photo = pdf_photo

                start_frame.pack_forget()
                button_frame.pack(side=tk.TOP, pady=50)

                question_label.config(text=f"A total of {pdf_counter} PDF and {jpg_counter} JPG files have been found in this folder. Do you want to convert the PDF files into JPG?")
            elif len(pdf_files) > 0:  
                pdf_directory = selected_item
                selected_pdf_name = None
                pdf_image_path = pdftojpgIMG
                pdf_image = Image.open(pdf_image_path)
                pdf_image = pdf_image.resize((300, 150), Image.LANCZOS)
                pdf_photo = ImageTk.PhotoImage(pdf_image)

                image_label.config(image=pdf_photo)
                image_label.photo = pdf_photo

                start_frame.pack_forget()
                button_frame.pack(side=tk.TOP, pady=50)

                question_label.config(text=f"Select a folder in which you want to convert all the PDF files.")
            elif len(jpg_files) > 0:  
                global num_converted_files  
                num_converted_files = len(jpg_files)

                data_image_path = dataIMG
                data_image = Image.open(data_image_path)
                data_image = data_image.resize((150, 150), Image.LANCZOS)
                data_photo = ImageTk.PhotoImage(data_image)

                image_label.config(image=data_photo)
                image_label.photo = data_photo

                start_frame.pack_forget()
                extract_frame.pack(pady=50)
                question_label.config(text=f"Do you want to extract the data of {num_converted_files} JPG files?")
    else:
        selected_item = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("PDF / JPG files", ".pdf .jpg")]
        )

        if selected_item:
            file_extension = os.path.splitext(selected_item)[-1]

            if file_extension.lower() == ".pdf":
                pdf_directory = os.path.dirname(selected_item)
                selected_pdf_name = os.path.basename(selected_item)

                pdf_image_path = pdftojpgIMG
                pdf_image = Image.open(pdf_image_path)
                pdf_image = pdf_image.resize((300, 150), Image.LANCZOS)
                pdf_photo = ImageTk.PhotoImage(pdf_image)

                image_label.config(image=pdf_photo)
                image_label.photo = pdf_photo

                start_frame.pack_forget()
                button_frame.pack(side=tk.TOP, pady=50)

                question_label.config(text=f"Do you want to convert {selected_pdf_name} into a JPG file?")

            elif file_extension.lower() == ".jpg":
                selected_image_filename = os.path.basename(selected_item)
                data_image_path = dataIMG
                data_image = Image.open(data_image_path)
                data_image = data_image.resize((150, 150), Image.LANCZOS)
                data_photo = ImageTk.PhotoImage(data_image)

                image_label.config(image=data_photo)
                image_label.photo = data_photo

                image_name = os.path.basename(selected_item)

                question_label.config(text=f"Do you want to extract the data of {image_name}?")
                start_frame.pack_forget()
                extract_frame.pack(pady=50)

def show_message_popup(message, success=True):
    popup = tk.Toplevel()
    popup.geometry("300x150")
    popup.title("Message")
    popup.resizable(False, False)

    icon_path = ""
    if success:
        icon_path = confirmIconIMG
    else:
        icon_path = errorIconIMG

    popup.iconbitmap(icon_path)

    message_label = tk.Label(popup, text=message, font=("Helvetica", 10), wraplength=250)
    message_label.pack(pady=20)

    ok_image = Image.open(okButtonIMG)
    ok_image = ok_image.resize((33, 32), Image.LANCZOS)
    ok_photo = ImageTk.PhotoImage(ok_image)

    ok_button = tk.Button(popup, image=ok_photo, command=popup.destroy, borderwidth=0, highlightthickness=0)
    ok_button.photo = ok_photo
    ok_button.pack(pady=15)

def save_to_csv():
    global left_value_example_values, right_value_example_values, selected_image_filename, left_value_areas, right_value_areas, num_converted_files
    
    try:
        csv_filename = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="data.csv", filetypes=[("CSV files", "*.csv")])
        if not csv_filename:
            return
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            header_row = left_value_areas + right_value_areas
            csv_writer.writerow(header_row)
            
            if num_converted_files == 0:
                example_values_row = left_value_example_values + right_value_example_values
                csv_writer.writerow(example_values_row)
            else:
                for i in range(num_converted_files):
                    example_values_row = left_value_example_values[i*len(left_value_areas):(i+1)*len(left_value_areas)] + right_value_example_values[i*len(right_value_areas):(i+1)*len(right_value_areas)]
                    csv_writer.writerow(example_values_row)

        show_message_popup(f"The CSV file has been created and saved successfully!", success=True)
    except Exception as e:
        show_message_popup(f"Error creating or saving CSV file: {e}", success=False)



def extract_data_from_image():
    global left_value_frame, right_value_frame, left_value_areas, right_value_areas, left_value_example_values, right_value_example_values, num_converted_files, left_value_labels, right_value_labels, canvas, canvas_frame, scroll_y, separator, combined_text, example_label, value_label, left_value_example_values_list, right_value_example_values_list, left_value_areas, right_value_areas, unique_areas

    CSV_frame.pack(pady=30)

    title_label.config(text="Data extracted from the image:")
    question_label.pack_forget()  
    start_frame.pack_forget()
    extract_frame.pack_forget()
    file_loc_frame.pack_forget()
    button_frame.pack_forget()
    extract_frame.pack_forget()

    if num_converted_files == 0:

        num_converted_files = 1

        left_value_frame = tk.Frame(root, bg="#f0f0f0")                                  
        left_value_frame.pack(side=tk.LEFT, padx=80, pady=(10))

        right_value_frame = tk.Frame(root, bg="#f0f0f0")
        right_value_frame.pack(side=tk.RIGHT, padx=80, pady=(10))

        left_value_labels = []
        right_value_labels = []

        combined_text, _, left_value_areas, right_value_areas, left_value_example_values, right_value_example_values = ocr_single_file(selected_item)
        
        for i in range(num_converted_files):
            for area in left_value_areas:
                value_label = tk.Label(left_value_frame, text=f"{area}:", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
                value_label.pack(pady=(15, 0))
                left_value_labels.append(value_label)

                example_value = left_value_example_values[left_value_areas.index(area)]
                example_label = tk.Label(left_value_frame, text=example_value, font=("Helvetica", 9), bg="#f0f0f0",  wraplength=200)
                example_label.pack()

            for area in right_value_areas:
                value_label = tk.Label(right_value_frame, text=f"{area}:", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
                value_label.pack(pady=(15, 0))
                right_value_labels.append(value_label)

                example_value = right_value_example_values[right_value_areas.index(area)]
                example_label = tk.Label(right_value_frame, text=example_value, font=("Helvetica", 9), bg="#f0f0f0",  wraplength=200)
                example_label.pack()


    else:
        left_value_example_values_list, right_value_example_values_list, left_value_areas_list, right_value_areas_list = ocr_multiple_files(selected_item)

        canvas = tk.Canvas(root, bg="#f0f0f0")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas_frame = tk.Frame(canvas, bg="#f0f0f0")
        canvas.create_window((0, 0), window=canvas_frame, anchor=tk.NW)

        left_value_frame = tk.Frame(canvas_frame, bg="#f0f0f0")                                  
        left_value_frame.pack(side=tk.LEFT, padx=110, pady=(10))

        right_value_frame = tk.Frame(canvas_frame, bg="#f0f0f0")
        right_value_frame.pack(side=tk.RIGHT, padx=80, pady=(10))

        unique_areas = set()

        for i in range(num_converted_files):
            left_example_values = left_value_example_values_list[i]
            right_example_values = right_value_example_values_list[i]

            for area in left_value_areas_list[i]:
                value_label = tk.Label(left_value_frame, text=f"{area}:", font=("Helvetica", 14, "bold"), bg="#f0f0f0",  wraplength=200)
                value_label.pack(pady=(15, 0))

                example_value = left_example_values.pop(0)
                example_label = tk.Label(left_value_frame, text=example_value, font=("Helvetica", 9), bg="#f0f0f0",  wraplength=200)
                example_label.pack()

                unique_areas.add(area)


            separator = ttk.Separator(left_value_frame, orient="horizontal")
            separator.pack(fill="x", pady=(5, 0))

            for area in right_value_areas_list[i]:
                value_label = tk.Label(right_value_frame, text=f"{area}:", font=("Helvetica", 14, "bold"), bg="#f0f0f0",  wraplength=200)
                value_label.pack(pady=(15, 0))

                example_value = right_example_values.pop(0)
                example_label = tk.Label(right_value_frame, text=example_value, font=("Helvetica", 9), bg="#f0f0f0",  wraplength=200)
                example_label.pack()

                unique_areas.add(area)

            separator = ttk.Separator(right_value_frame, orient="horizontal")
            separator.pack(fill="x", pady=(5, 0))

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        print("Unique Areas:", unique_areas)


def images_and_buttons():
    global pdf_directory, root, title_label, image_label, question_label, select_file_button, button_frame, convert_button, back_button, extract_frame, extract_data_button, back_button_copy, file_loc_frame, convert_more_button_copy, extract_converted_image_button, reset_button, csv_label, csv_button, CSV_frame, start_frame

    root = tk.Tk()
    root.title("Invoice Processing Tool")
    root.geometry("800x600")  
    root.configure(bg="#f0f0f0")
    root.resizable(False, False)

    icon_path = iconIMG
    root.iconbitmap(icon_path)

    # Window title
    title_label = tk.Label(root, text="Invoice Processing Tool", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
    title_label.pack(pady=20)

    # Image and Label
    image_path = resetIMG
    image = Image.open(image_path)
    image = image.resize((150, 150), Image.LANCZOS)  
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=photo, bg="#f0f0f0")
    image_label.pack(pady=30) 

    question_label = tk.Label(root, text="Select a file/folder with the extension .pdf or .jpg in order to proceed with the processing", font=("Helvetica", 14), bg="#f0f0f0", fg="#7d7d7d", wraplength=500)
    question_label.pack(pady=20)
    
    # Create a frame for the select file / select folder buttons
    start_frame = tk.Frame(root, bg="#f0f0f0")

    # Create Select File Button
    select_file_image = Image.open(selectFileButtonIMG)
    select_file_image = select_file_image.resize((137, 58), Image.LANCZOS)
    select_file_photo = ImageTk.PhotoImage(select_file_image)
    select_file_button = tk.Button(start_frame, image=select_file_photo, command=lambda: select_file_image_file())
    select_file_button.config(borderwidth=0, highlightthickness=0)

    # Select Folder button
    select_folder_image = Image.open(selectFolderButtonIMG)
    select_folder_image = select_folder_image.resize((162, 58), Image.LANCZOS)
    select_folder_photo = ImageTk.PhotoImage(select_folder_image)
    select_folder_button = tk.Button(start_frame, image=select_folder_photo, command=lambda: select_file_image_file(is_folder=True))
    select_folder_button.config(borderwidth=0, highlightthickness=0)

    # Frame for convert / back buttons
    button_frame = tk.Frame(root, bg="#f0f0f0")

    # Convert Button
    convert_image = Image.open(convertButtonIMG)  
    convert_image = convert_image.resize((174, 58), Image.LANCZOS)
    convert_photo = ImageTk.PhotoImage(convert_image)
    convert_button = tk.Button(button_frame, image=convert_photo, command=convert_pdf_to_jpg)
    convert_button.config(borderwidth=0, highlightthickness=0)

    # Back Button
    back_image = Image.open(cancelButtonIMG)  
    back_image = back_image.resize((103, 58), Image.LANCZOS)
    back_photo = ImageTk.PhotoImage(back_image)
    back_button = tk.Button(button_frame, image=back_photo, command=reset_interface)
    back_button.config(borderwidth=0, highlightthickness=0)

    #Frame for extract / back copy buttons
    extract_frame = tk.Frame(root, bg="#f0f0f0")

    # Extract Data Button
    extract_data_image = Image.open(extractDataImageButtonIMG)  
    extract_data_image = extract_data_image.resize((106, 58), Image.LANCZOS)
    extract_data_photo = ImageTk.PhotoImage(extract_data_image)
    extract_data_button = tk.Button(extract_frame, image=extract_data_photo, command=play_animation_and_extract)  
    extract_data_button.config(borderwidth=0, highlightthickness=0)

    # Copy of the back Button used for the frame
    back_image_copy = Image.open(cancelButtonIMG)  
    back_image_copy = back_image_copy.resize((103, 58), Image.LANCZOS)
    back_photo_copy = ImageTk.PhotoImage(back_image_copy)
    back_button_copy = tk.Button(extract_frame, image=back_photo_copy, command=reset_interface)
    back_button_copy.config(borderwidth=0, highlightthickness=0)

    #Frame for the convert more / Extract converted image data buttons
    file_loc_frame = tk.Frame(root, bg="#f0f0f0")

    #Copy of the convert Button used for the frame
    convert_more_image_copy = Image.open(convertMoreButtonIMG)  
    convert_more_image_copy = convert_more_image_copy.resize((154, 58), Image.LANCZOS)
    convert_more_photo_copy = ImageTk.PhotoImage(convert_more_image_copy)
    convert_more_button_copy = tk.Button(file_loc_frame, image=convert_more_photo_copy, command=reset_interface)
    convert_more_button_copy.config(borderwidth=0, highlightthickness=0)

    #File Location Button
    extract_converted_image_image = Image.open(extractConvertedImageButtonIMG)  
    extract_converted_image_image = extract_converted_image_image.resize((214, 58), Image.LANCZOS)
    extract_converted_image_photo = ImageTk.PhotoImage(extract_converted_image_image)
    extract_converted_image_button = tk.Button(file_loc_frame, image=extract_converted_image_photo, command=extract_data_after_conversion)
    extract_converted_image_button.config(borderwidth=0, highlightthickness=0)

    convert_button.pack(side=tk.LEFT, padx=10)
    back_button.pack(side=tk.LEFT, padx=10)
    
    #Frame for csv / reset buttons
    CSV_frame = tk.Frame(root, bg="#f0f0f0")

    # Create Reset Button
    reset_image = Image.open(resetButtonIMG)  
    reset_image = reset_image.resize((74, 47), Image.LANCZOS)
    reset_photo = ImageTk.PhotoImage(reset_image)
    reset_button = tk.Button(CSV_frame, image=reset_photo, command=reset_interface)
    reset_button.config(borderwidth=0, highlightthickness=0)
    reset_button.pack(side=tk.LEFT)

    # Image in the middle
    csv_image_path = csvIMG
    csv_image = Image.open(csv_image_path)
    csv_image = csv_image.resize((267, 150), Image.LANCZOS)
    csv_photo = ImageTk.PhotoImage(csv_image)
    csv_label = tk.Label(CSV_frame, image=csv_photo, bg="#f0f0f0")
    csv_label.photo = csv_photo  
    csv_label.pack(side=tk.LEFT)

    # Create CSV Button
    csv_button_image = Image.open(csvButtonIMG)  
    csv_button_image = csv_button_image.resize((157, 47), Image.LANCZOS)
    csv_button_photo = ImageTk.PhotoImage(csv_button_image)
    csv_button = tk.Button(CSV_frame, image=csv_button_photo, command=save_to_csv)
    csv_button.config(borderwidth=0, highlightthickness=0)
    csv_button.pack(side=tk.LEFT)

    convert_more_button_copy.pack(side=tk.LEFT, padx=10)
    extract_converted_image_button.pack(side=tk.LEFT, padx=10)

    convert_button.pack(side=tk.LEFT, padx=10)
    back_button.pack(side=tk.LEFT, padx=10)

    select_file_button.pack(side=tk.LEFT, padx=10)
    select_folder_button.pack(side=tk.LEFT, padx=10)
    start_frame.pack(pady=50)

    extract_data_button.pack(side=tk.LEFT, padx=10)
    back_button_copy.pack(side=tk.LEFT, padx=10)

    reset_button.pack(side=tk.LEFT, padx=50)
    csv_label.pack(side=tk.LEFT)
    csv_button.pack(side=tk.LEFT, padx=50)

    root.mainloop()
images_and_buttons()