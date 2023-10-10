# Smart-traffic-sign-management-system-based-on-mobile-phone-images
This system is designed to recognize traffic signs in an image and estimate their geographical position by using distance estimation algorithms and the camera's geographical position. Once the location is determined, it can be displayed on Google Maps. I conducted this project as my B.Sc. thesis in the Department of Computer Engineering at Amirkabir University of Technology. 
<p align="center">
  <img src="https://github.com/Mohadeseh-Atyabi/Smart-traffic-sign-management-system-based-on-mobile-phone-images/assets/72689599/69f229b3-a132-413a-ac26-74ebbbb04f47">
</p>

## Dataset
We collected a dataset that focuses on Tehran's dynamic streets, presenting a distinct perspective on the traffic sign challenges encountered in this vibrant urban environment. To collect the images, we installed the mobile phone camera on the windshield of the moving car and took pictures every 3 seconds. Our investigations have shown that signs that are up to 7 meters away from the camera can be easily identified. To reduce the overlapping of consecutive images, we filtered the images that are less than 7 meters apart. Eventually, a total of **1759 images** were used that were divided into test and train with the ratio of 80 to 20. In this dataset, 18 different types of traffic signs was annotated using **Label Studio**. We have shared our dataset on [Kaggle](https://www.kaggle.com/datasets/mohadesehatyabi/iranian-traffic-sign-dataset/). Feel free to download it and use it in your machine vision and image processing projects. 

## Finetuning object detection model
Our system is not real-time, so we need a model with higher accuracy than higher speed. Consequently, we decided on Faster R-CNN as our object detection model. As our dataset is not large enough to train the model from scratch, we used a pre-trained model and finetuned it. We finetuned the model for 80 epochs, which took about 6 hours, with a learning rate equal to 0.0001, and considered SGD (Stochastic Gradient Descend) as the optimizer function. We used several augmentations, including rotation, blur, and flip, to ensure the robustness of our model against different conditions such as rotation. The graph of the cost of training data for each training period is shown in the image below.
<p align="center">
  <img src="https://github.com/Mohadeseh-Atyabi/Smart-traffic-sign-management-system-based-on-mobile-phone-images/assets/72689599/e4d0a57b-7f55-4b29-ac5f-b4f125117c25" width=400px>
</p>
The evaluation criteria are mAP (Mean Average Precision), equal to 0.3189 after 80 training epochs. The mAP graph of training data for each epoch is shown in the image below. As you can see, the overall trend of the graph is ascending, illustrating a reasonable result of training.
<p align="center">
  <img src="https://github.com/Mohadeseh-Atyabi/Smart-traffic-sign-management-system-based-on-mobile-phone-images/assets/72689599/558dbd12-15d3-4529-8754-55cc87f3b1d0" width=400px>
</p>

## Locating detected objects

## Visualization of identified signs on Google Map 

## Feedback
