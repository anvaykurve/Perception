import cv2


input_path = r"/home/anvay/Downloads/image.png"
output_name = "result.png"

# Constants for Depth Calculation
REAL_HEIGHT_CM = 25       
FOCAL_LENGTH = 1000      

# [class_id, [x, y, w, h], confidence]
boxes_data = [
    [2.0, [0.43476563692092896, 0.7194444537162781, 0.03984374925494194, 0.1111111119389534], 0.8438236117362976],
    [2.0, [0.47539061307907104, 0.737500011920929, 0.04296875, 0.11666666716337204], 0.8504939675331116],
    [0.0, [0.33671873807907104, 0.7111111283302307, 0.03593749925494194, 0.09444444626569748], 0.9057255387306213],
    [3.0, [0.2679687440395355, 0.7361111044883728, 0.04374999925494194, 0.125], 0.919158935546875],
    [0.0, [0.21054688096046448, 0.7479166388511658, 0.04921875149011612, 0.12638889253139496], 0.9196999073028564],
    [3.0, [0.38945311307907104, 0.7201389074325562, 0.03984374925494194, 0.10972221940755844], 0.9205850958824158],
    [3.0, [0.5414062738418579, 0.762499988079071, 0.05312500149011612, 0.14444445073604584], 0.9242506623268127],
    [0.0, [0.610156238079071, 0.7909722328186035, 0.06406249850988388, 0.1736111044883728], 0.9282561540603638]
]

color_map = {
    0.0: (255, 0, 0),    # Blue
    2.0: (0, 0, 255),    # Red
    3.0: (0, 255, 255)   # Yellow
}

# --- PROCESSING ---
image = cv2.imread(input_path)

if image is None:
    print(f"Error: Could not load image from {input_path}")
else:
    img_h, img_w = image.shape[:2]

    for data in boxes_data:
        class_id = data[0]
        norm_box = data[1] # [cx, cy, w, h]
        
        # 1. Colors & Coordinates
        color = color_map.get(class_id, (0, 255, 0))
        
        cx = norm_box[0] * img_w
        cy = norm_box[1] * img_h
        w  = norm_box[2] * img_w
        h  = norm_box[3] * img_h # Height in pixels

        x_min = int(cx - (w / 2))
        y_min = int(cy - (h / 2))
        x_max = int(cx + (w / 2))
        y_max = int(cy + (h / 2))

        # 2. Draw Rectangle
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)

        # 3. Calculate Depth
        # Formula: Distance = (Focal_Length * Real_Height) / Image_Height_Pixels
        if h > 0: # Avoid division by zero
            distance_cm = (FOCAL_LENGTH * REAL_HEIGHT_CM) / h
            
            # Create text label (e.g., "150.2 cm")
            label = f"{distance_cm:.1f} cm"

            # 4. Draw Text
            # Position: Slightly above the box (y_min - 10)
            text_pos = (x_min, y_min - 10)
            
            # Arguments: image, text, position, font, scale, color, thickness
            cv2.putText(image, label, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # --- OUTPUT ---
    cv2.imwrite(output_name, image)
    print(f"Success! Image saved as {output_name}")
    
    cv2.imshow("Depth Estimation", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
