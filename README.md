# Smart-traffic-sign-management-system-based-on-mobile-phone-images
This system is designed to recognize traffic signs in an image and estimate their geographical position by using distance estimation algorithms and the camera's geographical position. Once the location is determined, it can be displayed on Google Maps. I conducted this project as my B.Sc. thesis in the Department of Computer Engineering at Amirkabir University of Technology. 
<p align="center">
  <img src="https://github.com/Mohadeseh-Atyabi/Smart-traffic-sign-management-system-based-on-mobile-phone-images/assets/72689599/69f229b3-a132-413a-ac26-74ebbbb04f47">
</p>

## Dataset
I collected a dataset that focuses on Tehran's dynamic streets, presenting a distinct perspective on the traffic sign challenges encountered in this vibrant urban environment. To collect the images, the mobile phone camera was installed on the windshield of the moving car and a picture was taken every 3 seconds. Investigations have shown that signs that are up to 7 meters away from the camera can be easily identified. To reduce the overlapping of consecutive images, the images that are less than 7 meters apart have been filtered. Eventually, a total of **1759 images** were used that were divided into test and train with the ratio of 80 to 20. In this dataset, 18 different types of traffic signs was annotated using **Label Studio**. I have shared my dataset on [Kaggle](https://www.kaggle.com/datasets/mohadesehatyabi/iranian-traffic-sign-dataset/). Feel free to download it and use it in your machine vision and image processing projects. 

## Finetuning Faster R-CNN
## Determining the location of detected objects
## Visualization of identified signs on Google Map 
## Feedback
