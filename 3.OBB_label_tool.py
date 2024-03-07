import cv2
import numpy as np

# Đọc bức ảnh
image_path = 'plane.jpg'
image = cv2.imread(image_path)

# Vẽ hình chữ nhật (ví dụ: góc trái trên (100, 100), góc phải dưới (200, 200))
cv2.rectangle(image, (100, 100), (200, 200), (255, 0, 0), 2)  # Màu xanh lá cây, độ dày viền 2

# Xoay hình chữ nhật (ví dụ: xoay 45 độ)
center = (150, 150)  # Tọa độ tâm của hình chữ nhật
angle = 45  # Góc xoay
scale = 1  # Tỉ lệ không thay đổi
rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=scale)
rotated_rect = cv2.warpAffine(image, rotate_matrix, (image.shape[1], image.shape[0]))

# Hiển thị ảnh
cv2.imshow('Rotated Rectangle', rotated_rect)
cv2.waitKey(0)
cv2.destroyAllWindows()
