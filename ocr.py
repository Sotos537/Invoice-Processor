import os
import shutil
import pytesseract
import json
from PIL import Image
import time
import random
from initialization import *

def ocr_single_file(selected_file):
    # Paths
    print(f"Processing file: {selected_file}")
    model_weights = "training_data\\invoice_test_set\\weights\\best.pt"
    image_path = selected_file
    #Path to the tesseract-ocr location
    os.environ['TESSDATA_PREFIX'] = r'\tessdata'
    img_size = 640

    start_time = time.time()
    os.chdir(yolov5_path)

    detection_command = (
        f"python detect.py --source {image_path} --weights {model_weights} --img-size {img_size} --conf 0.5"
    )

    os.system(detection_command)
    print(image_path)

    image_name = os.path.splitext(os.path.basename(image_path))[0]
    detection_result_folder = os.path.join(yolov5_path, "runs", "detect", "exp")
    image_name_without_extension = os.path.splitext(os.path.basename(image_path))[0]
    json_files = [f for f in os.listdir(detection_result_folder) if f.endswith('.json')]
    if len(json_files) == 0:
        print("No matching JSON files found in the detection result folder.")
        exit(1)
    json_path = os.path.join(detection_result_folder, json_files[0])

    with open(json_path, 'r') as json_file:
        detection_results = json.load(json_file)

    ignore_classes = ["paragraph", "logo"]

    class_confidences = {}

    image_full_path = os.path.join(yolov5_path, image_path)

    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789().,!?-/:'
    custom_config += ' -c language_model_penalty_non_freq_dict_word=1'

    combined_text = ""

    extracted_text = ""
    
    left_value_areas = []
    right_value_areas = []

    left_value_example_values = []
    right_value_example_values = []

    for detection_info in detection_results:
        class_name = detection_info["class_name"]
        confidence = detection_info["confidence"]
        bbox = detection_info["bbox"]
        x_min, y_min, x_max, y_max = bbox

        if class_name.lower() in ignore_classes:
            continue 

        if class_name in class_confidences:
            class_confidences[class_name] = max(class_confidences[class_name], confidence)
        else:
            class_confidences[class_name] = confidence

    total_classes = len(class_confidences)

    classes_per_area = total_classes // 2

    shuffled_class_names = list(class_confidences.keys())
    random.shuffle(shuffled_class_names)
    shuffled_class_names.sort()

    left_value_areas = shuffled_class_names[:classes_per_area]
    right_value_areas = shuffled_class_names[classes_per_area:]

    for class_name in sorted(class_confidences.keys()):
        for detection_info in detection_results:
            if detection_info["class_name"] == class_name and detection_info["confidence"] == class_confidences[class_name]:
                bbox = detection_info["bbox"]
                x_min, y_min, x_max, y_max = bbox

                # Crop the bounding box area
                image = Image.open(image_full_path)
                cropped_image = image.crop((x_min, y_min, x_max, y_max))

                extracted_text = pytesseract.image_to_string(cropped_image, lang='ell+eng', config=custom_config)

                if class_name in left_value_areas:
                    left_value_example_values.append(extracted_text)
                elif class_name in right_value_areas:
                    right_value_example_values.append(extracted_text)

                combined_text += f"Table Name: {class_name}\n"
            combined_text += extracted_text + "\n\n"

    output_text_path = os.path.join(tess_results_directory, f"{image_name}_combined_extracted.txt")
    with open(output_text_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(combined_text)

    print(f"Combined extracted text saved to: {output_text_path}")
    
    detection_result_folder = os.path.join(yolov5_path, "runs", "detect")
    for folder_name in os.listdir(detection_result_folder):
        if folder_name.startswith("exp"):
            folder_path = os.path.join(detection_result_folder, folder_name)
            shutil.rmtree(folder_path)
            print(f"Deleted folder: {folder_path}")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"OCR function execution time: {execution_time:.2f} seconds")
    print(f"Finished processing file: {selected_file}")
    return combined_text, execution_time, left_value_areas, right_value_areas, left_value_example_values, right_value_example_values


def ocr_multiple_files(selected_folder):

    left_value_example_values_list = []
    right_value_example_values_list = []
    
    left_value_areas_list = []  
    right_value_areas_list = []  

    for filename in os.listdir(selected_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(selected_folder, filename)

            print(f"Running OCR on file: {image_path}")

            _, _, left_value_areas, right_value_areas, left_value_example_values, right_value_example_values = ocr_single_file(image_path)

            left_value_example_values_list.append(left_value_example_values)
            right_value_example_values_list.append(right_value_example_values)

            left_value_areas_list.append(left_value_areas)
            right_value_areas_list.append(right_value_areas)

    return left_value_example_values_list, right_value_example_values_list, left_value_areas_list, right_value_areas_list
