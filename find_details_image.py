import cv2
import numpy as np
from scipy.signal import find_peaks


img = cv2.imread("skewed_test2.jpg")

#Contrast Enhancement
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
enhanced = clahe.apply(gray)

#Prewitt
kernel_x = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1]
], dtype=np.float32)

grad_x = cv2.filter2D(enhanced, cv2.CV_32F, kernel_x)
edge_image = np.clip(grad_x, 0, 255).astype(np.uint8)

#Canny
blurred = cv2.GaussianBlur(enhanced, (5, 5), 1.4)
edge_image = cv2.Canny(blurred, threshold1=50, threshold2=150)


#save result for debugging
cv2.imwrite("details_test2.jpg", edge_image)




#Convert to binary
_, binary_edges = cv2.threshold(edge_image, 127, 255, cv2.THRESH_BINARY)
binary_edges_norm = (binary_edges > 0).astype(np.float32)

#Summation profiles
row_profile = np.sum(binary_edges_norm, axis=1)
col_profile = np.sum(binary_edges_norm, axis=0)


#Handle outliers
def process_profile(profile):
    p_min = np.min(profile)
    p_max = np.max(profile)
    if p_max > p_min:
        normalized = (profile - p_min) / (p_max - p_min)
    else:
        normalized = profile.astype(float)
        
    noise_threshold = 0.15
    cleaned = np.where(normalized < noise_threshold, 0, normalized)
    return cleaned


horizontal_edge_profile = process_profile(row_profile)
vertical_edge_profile = process_profile(col_profile)


#Estimate num of floors
s= 13.5     #px/m

min_floor_height_pixels = int(2.5 * s)

peaks, properties = find_peaks(
    horizontal_edge_profile, 
    distance=min_floor_height_pixels,  
    prominence=0.1                     
)

number_of_floors = len(peaks)
print(f"Estimated number of floors: {number_of_floors}")

