import numpy as np
import cv2
import torch
import glob as glob
from model import create_model
from screeninfo import get_monitors
import json


# set the computation device
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
# load the model and the trained weights
model = create_model(num_classes=19).to(device)
model.load_state_dict(torch.load('../outputs/model80.pth', map_location=device))
model.eval()

# directory where all the images are present
DIR_TEST = '../test_data'
test_images = glob.glob(f"{DIR_TEST}/*")
print(f"Test instances: {len(test_images)}")
# classes: 0 index is reserved for background
CLASSES = [
    'background', 'Area with Camera', 'At the junction', 'Give Way', 'Keep Left', 'Keep Right', 'Maximum Speed', 'No Entry',
    'No Stopping', 'No Waiting', 'No through road', 'On approaches to junctions', 'One-way Traffic', 'Pedestrian Route',
    'Sharp deviation of Route (group)', 'Sharp deviation of route (single)', 'Stop', 'Taxi Station', 'Transport with Crane'
]
# define the detection threshold...
# ... any detection having score below this will be discarded
detection_threshold = 0.8

for i in range(len(test_images)):
    # get the image file name for saving output later on
    image_name = test_images[i].split('/')[-1].split('.')[0]
    image = cv2.imread(test_images[i])
    orig_image = image.copy()
    # BGR to RGB
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB).astype(np.float32)
    # make the pixel range between 0 and 1
    image /= 255.0
    # bring color channels to front
    image = np.transpose(image, (2, 0, 1)).astype(float)
    # convert to tensor
    image = torch.tensor(image, dtype=torch.float)
    # add batch dimension
    image = torch.unsqueeze(image, 0)
    with torch.no_grad():
        outputs = model(image)

    # load all detection to CPU for further operations
    outputs = [{k: v.to('cpu') for k, v in t.items()} for t in outputs]

    # save the outputs to text file to use for distance estimation
    file_name = test_images[i].split('\\')[-1].split('.')[0]
    with open(f'../test_bndbox/{file_name}.json', 'w') as f:
        my_dict = {}
        for key, value in outputs[0].items():
            my_dict[key] = value.data.numpy()

        # np.array is not serializable. so we have to convert it to the list to be able to save it in the file.
        my_dict_serializable = {}
        for k, v in my_dict.items():
            if isinstance(v, np.ndarray):
                my_dict_serializable[k] = v.tolist()
            else:
                my_dict_serializable[k] = v

        json.dump(my_dict_serializable, f)
    print("bndbox data saved.")

    # carry further only if there are detected boxes
    if len(outputs[0]['boxes']) != 0:
        boxes = outputs[0]['boxes'].data.numpy()
        scores = outputs[0]['scores'].data.numpy()
        # filter out boxes according to `detection_threshold`
        boxes = boxes[scores >= detection_threshold].astype(np.int32)
        draw_boxes = boxes.copy()
        # get all the predicited class names
        pred_classes = [CLASSES[i] for i in outputs[0]['labels'].cpu().numpy()]

        # draw the bounding boxes and write the class name on top of it
        for j, box in enumerate(draw_boxes):
            cv2.rectangle(orig_image,
                          (int(box[0]), int(box[1])),
                          (int(box[2]), int(box[3])),
                          (0, 0, 255), 2)
            cv2.putText(orig_image, pred_classes[j],
                        (int(box[0]), int(box[1] - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                        2, lineType=cv2.LINE_AA)

        # Get the primary monitor
        monitor = get_monitors()[0]
        screen_res = monitor.width - 10, monitor.height - 10
        # Resize the image to the screen size
        resized_img = cv2.resize(orig_image, screen_res)
        # Show the image with full size
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('image', resized_img)
        cv2.waitKey(0)
        # Destroy all windows
        cv2.destroyAllWindows()
        cv2.imwrite(f"../test_prediction/{image_name}.jpg", orig_image)
    print(f"Image {i + 1} done...")
    print('-' * 50)
print('TEST PREDICTIONS COMPLETE')
cv2.destroyAllWindows()
