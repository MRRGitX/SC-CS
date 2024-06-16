import rasterio
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

# Путь к файлам изображения

layout_path = 'C:/Users/79192/resized.tif'
crop_path = 'C:/Users/79192/Downloads/18_Sitronics/18_Sitronics/1_20/crop_0_0_0000.tif'

# Функция для нормализации каналов
def normalize(array):
    array_min, array_max = array.min(), array.max()
    return (array - array_min) / (array_max - array_min)

def resize_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized

def preparation_tif(frame_path, resize_percent=100):
    # Чтение изображения с помощью rasterio
    with rasterio.open(frame_path) as img:
        data = img.read()
    
    # Транспонируем данные для корректного порядка осей (в rasterio формат [band, row, col])
    data = np.transpose(data, (1, 2, 0))
    
    # Проверка количества каналов и нормализация
    channels = data.shape[2]
    if channels >= 3:
        r, g, b = data[..., 0], data[..., 1], data[..., 2]
    else:
        raise ValueError("Изображение должно иметь хотя бы 3 канала (RGB)")

    # Нормализуем каналы
    red_norm = normalize(r)
    green_norm = normalize(g)
    blue_norm = normalize(b)

    # Переводим нормализованные каналы в 8-битный формат для OpenCV
    red_norm_8bit = (red_norm * 255).astype(np.uint8)
    green_norm_8bit = (green_norm * 255).astype(np.uint8)
    blue_norm_8bit = (blue_norm * 255).astype(np.uint8)

    # Объединение каналов для вывода примера
    merge = cv2.merge([red_norm_8bit, green_norm_8bit, blue_norm_8bit])

    # Перевод изображения в градации серого
    gray_image = cv2.cvtColor(merge, cv2.COLOR_RGB2GRAY)

    return merge, gray_image

# Функция для отображения изображения с использованием matplotlib
def show_image(img, title="Image", cmap_type=None):
    plt.figure(figsize=(10, 10))
    if cmap_type:
        plt.imshow(img, cmap=cmap_type)
    else:
        plt.imshow(img)
    plt.title(title)
    plt.axis('off')
    plt.show()

# Подготовка изображений
merge_layout, original_img_bw = preparation_tif(layout_path)
merge_crop, query_img_bw = preparation_tif(crop_path)

# Сохранение layout в формате JPEG с уменьшенным качеством
layout_jpeg_path = 'C:/Users/79192/Downloads/18_Sitronics/18_Sitronics/layouts/layout_2021_10_10_compressed.jpg'
cv2.imwrite(layout_jpeg_path, merge_layout, [int(cv2.IMWRITE_JPEG_QUALITY), 50])  # 50 - качество JPEG

# Инициализация SIFT детектора с уменьшенным количеством точек
sift = cv2.SIFT_create(5000)  # Уменьшаем количество точек до 300 
# вот здесь (сверху) в ошибку сваливается, если в полном разрешении считать, даже 5k точек недостаточно

# Поиск ключевых точек и дескрипторов
queryKP, queryDes = sift.detectAndCompute(query_img_bw, None)
trainKP, trainDes = sift.detectAndCompute(original_img_bw, None)

# Проверка на наличие дескрипторов
if queryDes is None or trainDes is None:
    raise ValueError("Не удалось найти ключевые точки и дескрипторы на одном из изображений")

# Сопоставление дескрипторов
matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
matches = matcher.match(queryDes, trainDes)
matches = sorted(matches, key=lambda x: x.distance)

# Сопоставление изображений
final_img = cv2.drawMatches(merge_crop, queryKP, merge_layout, trainKP, matches[:20], None)

# Изменение размера изображения для отображения
final_img = cv2.resize(final_img, (1000, 650))

if len(matches) > 12:  # Убедимся, что у нас достаточно совпадений
    src_pts = np.float32([queryKP[m.queryIdx].pt for m in matches]).reshape(-1, 2)
    dst_pts = np.float32([trainKP[m.trainIdx].pt for m in matches]).reshape(-1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    h, w = query_img_bw.shape
    pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)  # координаты углов шаблона
    dst = cv2.perspectiveTransform(pts, M)
    layout_with_box = cv2.polylines(merge_layout, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
else:
    layout_with_box = merge_layout

# Отображение изображений
show_image(merge_crop, "Original RGB Image (Crop)")
show_image(merge_layout, "Original RGB Image (Layout)")
show_image(query_img_bw, "Grayscale Image (Crop)", cmap_type='gray')
show_image(original_img_bw, "Grayscale Image (Layout)", cmap_type='gray')
show_image(final_img, "Matches")
show_image(layout_with_box, "Detected Crop Location")




