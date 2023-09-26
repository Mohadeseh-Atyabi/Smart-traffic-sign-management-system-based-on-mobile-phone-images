import albumentations as A
import cv2
import torch
import numpy as np
from albumentations.pytorch import ToTensorV2
from config import DEVICE, CLASSES as classes
from mean_average_precision import MetricBuilder


# this class keeps track of the training and validation loss values...
# ... and helps to get the average for each epoch as well
class Averager:
    def __init__(self):
        self.current_total = 0.0
        self.iterations = 0.0

    def send(self, value):
        self.current_total += value
        self.iterations += 1

    @property
    def value(self):
        if self.iterations == 0:
            return 0
        else:
            return 1.0 * self.current_total / self.iterations

    def reset(self):
        self.current_total = 0.0
        self.iterations = 0.0

    def collate_fn(self, batch):
        """
        To handle the data loading as different images may have different number
        of objects and to handle varying size tensors as well.
        """
        return tuple(zip(*batch))

    # define the training transforms
    def get_train_transform(self):
        return A.Compose([
            A.Flip(0.5),
            A.RandomRotate90(0.5),
            A.MotionBlur(p=0.2),
            A.MedianBlur(blur_limit=3, p=0.1),
            A.Blur(blur_limit=3, p=0.1),
            ToTensorV2(p=1.0),
        ], bbox_params={
            'format': 'pascal_voc',
            'label_fields': ['labels']
        })

    # define the validation transforms
    def get_valid_transform(self):
        return A.Compose([
            ToTensorV2(p=1.0),
        ], bbox_params={
            'format': 'pascal_voc',
            'label_fields': ['labels']
        })

    def get_mean_average_precision(self, model, data_loader, iou_threshold, device):
        model.eval()
        metric_fn = MetricBuilder.build_evaluation_metric("map_2d", async_mode=True, num_classes=18)
        with torch.no_grad():
            for images, targets in data_loader:
                images = list(image.to(device) for image in images)
                targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

                outputs = model(images)

                boxes = outputs[0]['boxes']
                labels = outputs[0]['labels']
                scores = outputs[0]['scores']

                preds = []
                for i in range(len(boxes)):
                    box = boxes[i]
                    label = labels[i]
                    score = scores[i]

                    xmin, ymin, xmax, ymax = box.tolist()
                    class_id = label.item()
                    confidence = score.item()

                    preds.append([xmin, ymin, xmax, ymax, class_id, confidence])

                boxes = targets[0]['boxes']
                labels = targets[0]['labels']
                num_boxes = boxes.shape[0]
                gt = []
                for i in range(num_boxes):
                    xmin, ymin, xmax, ymax = boxes[i].tolist()
                    class_id = labels[i].item()
                    gt.append([xmin, ymin, xmax, ymax, class_id, 0, 0])

                metric_fn.add(np.array(preds), np.array(gt))
        model.train()

        return metric_fn.value(iou_thresholds=0.5, recall_thresholds=np.arange(0., 1.1, 0.1))['mAP']

    def show_transformed_image(train_loader):
        """
        This function shows the transformed images from the `train_loader`.
        Helps to check whether the tranformed images along with the corresponding
        labels are correct or not.
        Only runs if `VISUALIZE_TRANSFORMED_IMAGES = True` in config.py.
        """
        if len(train_loader) > 0:
            for i in range(1):
                images, targets = next(iter(train_loader))
                images = list(image.to(DEVICE) for image in images)
                targets = [{k: v.to(DEVICE) for k, v in t.items()} for t in targets]
                boxes = targets[i]['boxes'].cpu().numpy().astype(np.int32)
                sample = images[i].permute(1, 2, 0).cpu().numpy()
                for box in boxes:
                    cv2.rectangle(sample,
                                  (box[0], box[1]),
                                  (box[2], box[3]),
                                  (0, 0, 255), 2)
                cv2.imshow('Transformed image', sample)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
