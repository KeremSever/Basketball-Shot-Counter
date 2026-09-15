# Basketball-Shot-Counter

A computer vision pipeline that counts made/attempted shots from video,
using a YOLOv11 object-detection model.

- Trained and fine-tuned YOLOv11 for shot-attempt detection
- Benchmarked two model sizes; selected a 9.4M-parameter model with 89% fewer FLOPs while retaining 94% of the larger model's precision/recall
- 90% mAP50 on validation data
- Added frame-filtering and cooldown logic to suppress false and duplicate detections
- Flask web app around the pipeline, with user accounts (Flask-SQLAlchemy) and video upload
- Added recent and all-time analytics dashboards (shots attempted/made, field goal %) plus an NBA player comparison feature


