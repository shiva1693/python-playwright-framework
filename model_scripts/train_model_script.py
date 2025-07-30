from ultralytics import YOLO, checks, hub
checks()

hub.login('57ee9a418b5b5b8e02c0f3564228815880eaf9ffda')

model = YOLO('https://hub.ultralytics.com/models/DQKaAyI0jUaFu5q0Z6zO')
results = model.train()