Файл SIFT/SURF.py

Эта программа использует алгоритм SIFT (Scale-Invariant Feature Transform) для обнаружения и сопоставления ключевых точек между двумя изображениями.

Для использования программы необходимо установить следующие библиотеки:

* opencv-python
* opencv-python-headless
* rasterio

Путь к файлам изображения указан в переменных `layout_path` и `crop_path`. Функция `preparation_tif` используется для преобразования изображений в градации серого и нормализации каналов. Функция `show_image` используется для отображения изображений с использованием matplotlib.

Затем программа использует SIFT детектор для обнаружения ключевых точек и дескрипторов в обоих изображениях. Функция `cv2.BFMatcher` используется для сопоставления дескрипторов. Результаты сопоставления сортируются по расстоянию и выводятся на экран с использованием `cv2.drawMatches`.

Если количество совпадений больше 12, программа вычисляет матрицу преобразования перспективы между двумя изображениями и выводит изображение с обнаруженным расположением обрезанной области.

Файл SIFT/SURF.pyproj

Это файл проекта Visual Studio, который не используется в данной программе.

Файл SIFT/SURF.sln

Это файл решения Visual Studio, который не используется в данной программе.

Пример использования программы:

* Установить необходимые библиотеки: `pip install opencv-python opencv-python-headless rasterio`
* Указать путь к файлам изображения в переменных `layout_path` и `crop_path`
* Запустить программу: `python SIFT/SURF.py`

Ограничения:

* Изображение должно иметь хотя бы 3 канала (RGB)
* Если количество ключевых точек превышает 5000, программа может не справиться с вычислениями в полном разрешении. В этом случае необходимо уменьшить количество точек или уменьшить разрешение изображения.
* Если программа не находит ключевые точки и дескрипторы на одном из изображений, она выдает исключение `ValueError`.
* Если количество совпадений меньше 12, программа не вычисляет матрицу преобразования перспективы и не выводит изображение с обнаруженным расположением обрезанной области.

_______________________________________________________________________________________________


This documentation is for a program that uses the SIFT (Scale-Invariant Feature Transform) algorithm to detect and match features between two images. The program is written in Python and uses the OpenCV library.

The program consists of three files:

* `SIFT/SURF.py`: the main Python script that contains the logic for loading and processing the images, detecting and matching features, and displaying the results.
* `SIFT/SURF.pyproj`: a project file for Visual Studio that specifies the build configuration and settings for the program.
* `SIFT/SURF.sln`: a solution file for Visual Studio that groups the project file and any other related files together.

To use the program, follow these steps:

1. Install the required dependencies:
	* OpenCV library: `pip install opencv-python`
	* rasterio library: `pip install rasterio`
2. Place the two images that you want to compare in the same directory as the `SIFT/SURF.py` script.
	* The first image is the "layout" image, which is the larger image that contains the scene.
	* The second image is the "crop" image, which is the smaller image that is a subset of the layout image.
3. Modify the `layout_path` and `crop_path` variables in the `SIFT/SURF.py` script to point to the correct file paths for your images.
4. Run the `SIFT/SURF.py` script.

The program will perform the following steps:

1. Load the layout and crop images using the `rasterio` library.
2. Normalize the red, green, and blue channels of the images.
3. Convert the images to grayscale.
4. Detect and compute the SIFT features for both images.
5. Match the features between the two images using the brute force matcher with cross-checking.
6. Sort the matches by distance and draw the top 20 matches on the images.
7. If there are more than 12 matches, compute the homography matrix and draw a bounding box around the detected crop location on the layout image.
8. Display the original RGB images, the grayscale images, the matches, and the detected crop location on the layout image using `matplotlib`.

Note:

* The program saves the layout image in JPEG format with reduced quality to reduce the file size.
* The SIFT detector is initialized with a reduced number of features (5000) to improve performance. If you encounter an error, try increasing the number of features or reducing the size of the images.
* The program checks if there are any descriptors for both images. If not, it raises a `ValueError` with a message indicating that the program was unable to find key points and descriptors on one of the images.
* The program checks if there are at least 12 matches before computing the homography matrix and drawing the bounding box. If there are fewer than 12 matches, the program will only display the matches without the bounding box.

Example usage:

Assuming the layout image is located at `C:/Users/79192/resized.tif` and the crop image is located at `C:/Users/79192/Downloads/18_Sitronics/18_Sitronics/1_20/crop_0_0_0000.tif`, the `layout_path` and `crop_path` variables should be set as follows:
```
layout_path = 'C:/Users/79192/resized.tif'
crop_path = 'C:/Users/79192/Downloads/18_Sitronics/18_Sitronics/1_20/crop_0_0_0000.tif'
```
After running the `SIFT/SURF.py` script, the program will display the following images:

* The original RGB image for the crop.
* The original RGB image for the layout.
* The grayscale image for the crop.
* The grayscale image for the layout.
* The matches between the crop and layout images.
* The detected crop location on the layout image (if there are at least 12 matches).
