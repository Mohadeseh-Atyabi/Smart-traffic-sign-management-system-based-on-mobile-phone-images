import torch

BATCH_SIZE = 4  # increase / decrease according to GPU memeory
BATCH_SIZE_VALID = 1
RESIZE_TO = 512  # resize the image for training and transforms
NUM_EPOCHS = 50  # number of epochs to train for

DEVICE = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# training images and XML files directory
TRAIN_DIR = '../Dataset/train'
# validation images and XML files directory
VALID_DIR = '../Dataset/test'
# classes: 0 index is reserved for background

CLASSES = [
    'background', 'Area with Camera', 'At the junction', 'Give Way', 'Keep Left', 'Keep Right', 'Maximum Speed', 'No Entry',
    'No Stopping', 'No Waiting', 'No through road', 'On approaches to junctions', 'One-way Traffic', 'Pedestrian Route',
    'Sharp deviation of Route (group)', 'Sharp deviation of route (single)', 'Stop', 'Taxi Station', 'Transport with Crane'
]
NUM_CLASSES = 19

# whether to visualize images after crearing the data loaders
VISUALIZE_TRANSFORMED_IMAGES = False

# location to save model and plots
OUT_DIR = '../outputs'
SAVE_PLOTS_EPOCH = 2 # save loss plots after these many epochs
SAVE_MODEL_EPOCH = 2 # save model after these many epochs