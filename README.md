# Basketball-Shot-Counter

A computer vision pipeline that counts made/attempted shots from video,
using a YOLOv11 object-detection model.

## Method
- Trained and fine-tuned YOLOv11 for shot-attempt detection
- Benchmarked two model sizes; selected a 9.4M-parameter model with
  89% fewer FLOPs while retaining 94% of the larger model's precision/recall
- Added frame-filtering and cooldown logic to suppress false and duplicate detections
- Flask web app around the pipeline, with user accounts (Flask-SQLAlchemy) and video upload/validation triggering the shot-tracker
- Added recent and all-time analytics dashboards (shots attempted/made, field goal %) plus an NBA player comparison feature

## Results
- 90% mAP50 on validation data
- 76% improvement in shot-counting accuracy after adding the filtering/cooldown logic
