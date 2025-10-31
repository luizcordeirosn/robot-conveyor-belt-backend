class Mapper:
    @staticmethod
    def centroid_and_label_to_dict(
        x=0, y=0, label=None, class_label=None, prediction=None, filename=None
    ):
        return {
            "x": x,
            "y": y,
            "label": label,
            "class": class_label,
            "prediction": prediction,
            "filename": filename,
        }
