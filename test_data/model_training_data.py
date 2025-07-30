from dataclasses import dataclass, field
import time

@dataclass
class model_training_data:
    project_name: str = f"auto_project_{time.strftime('%Y%m%d-%H%M%S-%f')}"
    project_description: str = "This is a test project description."
    model_name: str = f"Test Model {time.strftime('%Y%m%d_%H%M%S')}"
    model_arch: str = "YOLO11n"
    epoch_value: str = "5"

# constants = {
#     "PROJECT_NAME" :f"auto_project_" + time.strftime("%Y%m%d-%H%M%S"),
#     "PROJECT_DESCRIPTION" : "This is a test project description.",
#     "MODEL_NAME" : "Test Model",
#     "MODEL_ARCH" : "YOLO11n",
#     "EPOCH_VALUE" : "5"
# }

# class ModelTrainingData:
#     PROJECT_NAME = f"auto_project_" + time.strftime("%Y%m%d-%H%M%S")
#     PROJECT_DESCRIPTION = "This is a test project description."
#     MODEL_NAME = "Test Model"
#     MODEL_ARCH = "YOLO11n"
#     EPOCH_VALUE = "5"
