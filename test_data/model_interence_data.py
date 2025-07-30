from dataclasses import dataclass


@dataclass
class ModelInferenceData:
    github_image_url: str = "https://github.com/ultralytics/hub/blob/main/example_datasets/coco8/images/train/000000000030.jpg"
    confidence_threshold: float = 0.80
    expected_objects: list[str] = ("vase", "potted plant")
    expected_objects_after_adjustment: list[str] = ("vase",)