from dataclasses import dataclass


@dataclass
class ModelExportData:
    name: str
    expect_ext: str

test_export_data = [
ModelExportData(name="PyTorch", expect_ext=".pt"),
ModelExportData(name="TorchScript", expect_ext=".torchscript.pt"),
ModelExportData(name="ONNX", expect_ext=".onnx"),
ModelExportData(name="OpenVINO", expect_ext="_openvino_model.zip"),
ModelExportData(name="TFLite", expect_ext=".tflite"),
]