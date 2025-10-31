import cv2
import numpy as np


class RedRectangleDetector:
    """
    Initializes the RedRectangleDetector with a minimum area for contour
    detection.
    The color range for red detection is set in the LAB color space.
    The default values are set to detect red colors in the range of 150 to 255
    e 'a' channel.
    The default minimum contour area is set to 1000 pixels.

    Args:
    min_contour_area (int): Minimum area of contours to be considered for
    detection.
    l_range (tuple): Range of L channel values in LAB color space.
    a_range (tuple): Range of A channel values in LAB color space.
    b_range (tuple): Range of B channel values in LAB color space.

    """

    def __init__(
        self,
        min_contour_area=1000,
        l_range: tuple = (0, 255),
        a_range: tuple = (150, 255),
        b_range: tuple = (0, 255),
    ):
        self.min_contour_area = min_contour_area
        self.lower_lab_red = np.array([l_range[0], a_range[0], b_range[0]])
        self.upper_lab_red = np.array([l_range[1], a_range[1], b_range[1]])
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

        self.last_detection = None

    def _get_red_mask(self, image: np.ndarray) -> np.ndarray:
        """
        Generates a binary mask for red regions using a robust pipeline.

        This method is designed to be resilient to lighting variations.
        It converts the image to the LAB color space, applies CLAHE to
        normalize the lightness channel, and then filters for red based on
        the 'a' channel.

        Args:
            image (np.ndarray): The input image in BGR format.

        Returns:
            np.ndarray: A binary mask where white pixels correspond to
            detected red regions.
        """
        # Convert the image from BGR to the LAB color space.
        img_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        # Split the L*, a*, and b* channels.
        l_channel, a_channel, b_channel = cv2.split(img_lab)

        # Apply Contrast Limited Adaptive Histogram Equalization (CLAHE) ONLY
        #  to the L-channel.
        l_channel_eq = self.clahe.apply(l_channel)

        # Merge the equalized L-channel back with the original a* and b*
        #  channels.
        img_lab_eq = cv2.merge([l_channel_eq, a_channel, b_channel])

        # Create the mask using cv2.inRange on the normalized LAB image
        red_mask = cv2.inRange(img_lab_eq, self.lower_lab_red, self.upper_lab_red)

        # Clean up small noise from the mask using morphological opening
        #  operation.
        kernel = np.ones((3, 3), np.uint8)
        red_mask_opened = cv2.morphologyEx(
            red_mask, cv2.MORPH_OPEN, kernel, iterations=2
        )

        return red_mask_opened

    def _get_centroid(self, approx_polygon: np.ndarray) -> tuple:
        """
        Calculates the centroid of an approximated polygon.

        Args:
            approx_polygon (numpy.ndarray): Coordinates of the polygon's
            vertices (Nx1x2).

        Returns:
            tuple: (x, y) coordinates of the polygon's centroid.
        """
        x_coords = approx_polygon[:, 0, 0]
        y_coords = approx_polygon[:, 0, 1]

        x_min = np.min(x_coords)
        x_max = np.max(x_coords)
        y_min = np.min(y_coords)
        y_max = np.max(y_coords)

        x_center = (x_min + x_max) // 2
        y_center = (y_min + y_max) // 2

        return int(x_center), int(y_center)

    def draw_centroids(self, image: np.ndarray, centroids: list[tuple]) -> np.ndarray:
        """
        Draws circles on the image at the specified centroids.

        Args:
            image (numpy.ndarray): Input image in BGR format.
            centroids (list): List of (x, y) coordinates of centroids to draw.

        Returns:
            numpy.ndarray: Image with drawn centroids.
        """
        image_copy = image.copy()
        for centroid in centroids:
            cv2.circle(image_copy, centroid, 5, (0, 255, 0), -1)
        return image_copy

    def get_rectangle_centroids(self, image: np.ndarray) -> list[tuple]:
        """
        Detects red rectangular shapes in the input image.

        This function identifies red regions, filters contours by area,
        approximates them to polygons, and checks if
        they have four vertices (i.e., are rectangles).

        Args:
            image (numpy.ndarray): Input image in BGR format.

        Returns:
            - list of (x, y) coordinates of detected centroids.
        """
        centroids = []

        red_mask = self._get_red_mask(image)
        contours, _ = cv2.findContours(
            red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            contour_area = cv2.contourArea(contour)

            if contour_area > self.min_contour_area:
                perimeter = cv2.arcLength(contour, True)
                epsilon = 0.02 * perimeter
                approx_polygon = cv2.approxPolyDP(contour, epsilon, True)

                if len(approx_polygon) == 4:
                    centroid = self._get_centroid(approx_polygon)
                    centroids.append(centroid)

        num_detections = len(centroids)
        if num_detections == 4:
            self.last_detection = centroids
        elif 0 < num_detections <= 3:
            ordered_points = self.order_points(image, centroids)
            centroids = self.find_missing_points(ordered_points, image)
            self.last_detection = centroids
        elif num_detections == 0:
            centroids = self.last_detection

        return centroids

    def find_missing_points(
        self, points: dict[str, tuple[float, float] | None], image: np.ndarray
    ) -> list[tuple[float, float]]:
        """Estimates missing rectangle points based on geometric patterns from
        known points.

        This method handles different scenarios of missing points (1, 2, or 3
        missing) and estimates their positions using symmetry and relative
        positioning based on the image center.

        Args:
            points (dict): Dictionary with keys 'top_left', 'top_right',
                           'bottom_left', 'bottom_right' containing either
                           (x,y) coordinates or None for missing points.
            image (np.ndarray): Reference image used to calculate center point.

        Returns:
            list[tuple]: List containing all four points in order [top_left,
                         top_right, bottom_right, bottom_left] with estimated
                         points filled in.
        """
        # Separate known and missing points
        missing_points = []
        known_points = []
        x_points = []
        y_points = []
        for i in points:
            if not points[i]:
                missing_points.append(i)
            else:
                x_points.append(points[i][0])
                y_points.append(points[i][1])
                known_points.append(i)

        known_points_len = 4 - len(missing_points)

        if known_points_len == 3:
            x_points.sort()
            diffs_x = [
                abs(x_points[2] - x_points[1]),
                abs(x_points[0] - x_points[2]),
                abs(x_points[0] - x_points[1]),
            ]
            min_index_x = diffs_x.index(min(diffs_x))
            x = x_points[min_index_x]

            diffs_y = [
                abs(y_points[2] - y_points[1]),
                abs(y_points[0] - y_points[2]),
                abs(y_points[0] - y_points[1]),
            ]
            min_index_y = diffs_y.index(min(diffs_y))
            y = y_points[min_index_y]
            points[missing_points[0]] = (x, y)
        elif known_points_len == 2:
            center = self.get_center_image(image)
            if "top" in known_points[0] and "top" in known_points[1]:
                points["bottom_left"] = (
                    points["top_left"][0],
                    int(
                        points["top_left"][1] + (center[1] - points["top_left"][1]) * 2
                    ),
                )

                points["bottom_right"] = (
                    points["top_right"][0],
                    int(
                        points["top_right"][1]
                        + (center[1] - points["top_right"][1]) * 2
                    ),
                )

            elif "bottom" in known_points[0] and "bottom" in known_points[1]:
                points["top_left"] = (
                    points["bottom_left"][0],
                    int(
                        points["bottom_left"][1]
                        - (points["bottom_left"][1] - center[1]) * 2
                    ),
                )

                points["top_right"] = (
                    points["bottom_right"][0],
                    int(
                        points["bottom_right"][1]
                        - (points["bottom_right"][1] - center[1]) * 2
                    ),
                )

            elif "left" in known_points[0] and "left" in known_points[1]:
                points["top_right"] = (
                    int(
                        points["top_left"][0] + (center[0] - points["top_left"][0]) * 2
                    ),
                    points["top_left"][1],
                )

                points["bottom_right"] = (
                    int(
                        points["bottom_left"][0]
                        + (center[0] - points["bottom_left"][0]) * 2
                    ),
                    points["bottom_left"][1],
                )

            elif "right" in known_points[0] and "right" in known_points[1]:
                points["top_left"] = (
                    int(
                        points["top_right"][0]
                        - (points["top_right"][0] - center[0]) * 2
                    ),
                    points["top_right"][1],
                )

                points["bottom_left"] = (
                    int(
                        points["bottom_right"][0]
                        - (points["bottom_right"][0] - center[0]) * 2
                    ),
                    points["bottom_right"][1],
                )

            elif "top_right" in known_points and "bottom_left" in known_points:
                points["top_left"] = (points["bottom_left"][0], points["top_right"][1])

                points["bottom_right"] = (
                    points["top_right"][0],
                    points["bottom_left"][1],
                )

            else:
                points["top_right"] = (points["bottom_right"][0], points["top_left"][1])

                points["bottom_left"] = (
                    points["top_left"][0],
                    points["bottom_right"][1],
                )

        elif known_points_len == 1:
            center = self.get_center_image(image)

            if known_points[0] == "top_left":
                points["top_right"] = (
                    int(
                        points["top_left"][0] + (center[0] - points["top_left"][0]) * 2
                    ),
                    points["top_left"][1],
                )

                points["bottom_left"] = (
                    points["top_left"][0],
                    int(
                        points["top_left"][1] + (center[1] - points["top_left"][1]) * 2
                    ),
                )

                points["bottom_right"] = (
                    points["top_right"][0],
                    points["bottom_left"][1],
                )

            elif known_points[0] == "top_right":
                points["top_left"] = (
                    int(
                        points["top_right"][0]
                        - (points["top_right"][0] - center[0]) * 2
                    ),
                    points["top_right"][1],
                )

                points["bottom_left"] = (
                    points["top_left"][0],
                    int(
                        points["top_left"][1] + (center[1] - points["top_left"][1]) * 2
                    ),
                )

                points["bottom_right"] = (
                    points["top_right"][0],
                    points["bottom_left"][1],
                )

            elif known_points[0] == "bottom_left":
                points["top_left"] = (
                    points["bottom_left"][0],
                    int(
                        points["bottom_left"][1]
                        - (points["bottom_left"][1] - center[1]) * 2
                    ),
                )

                points["top_right"] = (
                    int(
                        points["top_left"][0] + (center[0] - points["top_left"][0]) * 2
                    ),
                    points["top_left"][1],
                )

                points["bottom_right"] = (
                    points["top_right"][0],
                    points["bottom_left"][1],
                )

            else:
                points["bottom_left"] = (
                    int(
                        points["bottom_right"][0]
                        - (points["bottom_right"][0] - center[0]) * 2
                    ),
                    points["bottom_right"][1],
                )

                points["top_right"] = (
                    points["bottom_right"][0],
                    int(
                        points["bottom_right"][1]
                        - (points["bottom_right"][1] - center[1]) * 2
                    ),
                )

                points["top_left"] = (points["bottom_left"][0], points["top_right"][1])

        complete_points = [point for point in points.values()]
        return complete_points

    def order_points(
        self, image: np.ndarray, points: list[tuple]
    ) -> dict[str, tuple[float, float] | None]:
        """Sorts points into quadrants relative to the image center and
        categorizes them.

            Divides the image into 4 quadrants using the center point and
            assigns each input point to one of the positions: top_left,
            top_right, bottom_left, bottom_right.

            Args:
                image (np.ndarray): Reference image used to determine center
                point.
                points (list[tuple[float, float]]): List of (x, y) coordinate
                points to be sorted.

            Returns:
                dict[str, tuple[float, float] | None]: Dictionary with keys
                for each corner position and corresponding point coordinates
                or None if no point was found in that quadrant.
        """
        if not points:
            raise ValueError("Points list cannot be empty")

        center = self.get_center_image(image)
        top_left, top_right, bottom_right, bottom_left = None, None, None, None
        for point in points:
            if point[0] < center[0] and point[1] < center[1]:
                top_left = point
            elif point[0] > center[0] and point[1] > center[1]:
                bottom_right = point
            elif point[0] > center[0] and point[1] < center[1]:
                top_right = point
            else:
                bottom_left = point
        return {
            "top_left": top_left,
            "top_right": top_right,
            "bottom_right": bottom_right,
            "bottom_left": bottom_left,
        }

    def get_center_image(self, image: np.ndarray) -> tuple[float, float]:
        """
        Calculates the center point coordinates of an image.
        Args:
            image (np.ndarray): Input image in numpy array format.

        Returns:
            tuple[float, float]: (x_center, y_center) coordinates of the image
            center point.

        """
        image_size_y, image_size_x = image.shape[:2]
        x_center, y_center = image_size_x / 2, image_size_y / 2
        return x_center, y_center

    def painting_black_outside_rectangle(
        self, image: np.ndarray, points: list[tuple]
    ) -> np.ndarray:
        """
        Paint black outside rectangle of an image.
        Args:
            image (np.ndarray): Input image in numpy array format.
            points (list[tuple[float, float]]): List of (x, y) coordinate
            points to be sorted.

        Returns:
            painted_image (np.ndarray): Image painted in black outside
            rectangle.
        """
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        ordered_points = self.order_points(image, points)
        points = [
            ordered_points["top_left"],
            ordered_points["top_right"],
            ordered_points["bottom_right"],
            ordered_points["bottom_left"],
        ]
        points_np = np.array(points, dtype=np.int32).reshape((-1, 1, 2))

        cv2.drawContours(mask, [points_np], -1, 255, thickness=cv2.FILLED)

        painted_image = cv2.bitwise_and(image, image, mask=mask)

        return painted_image
