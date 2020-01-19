# Krabby-Patty-Secret-Formula-Finder
Our project submission for HackED 2020.
We first started by finding the proper Arduino file and libraries to be able to connect and communicate with our camera module. 
We found this program file: https://github.com/fariskazmi/Krabby-Patty-Secret-Formula-Finder/blob/master/FC7PPF5ILCN87DX.ino
Then we followed the wiring schematic shown here to hook up the camera:https://circuitdigest.com/fullimage?i=circuitdiagram_mic/Circuit-Diagram-for-Interfacing-OV7670-Camera-Module-with-Arduino.png (note that on the schmatic, the SDA pin is called SIOD, and the SCL pin is called SIOC). 

We modified our Arduino setup and code to include a button that would allow us to only take a picture when the button to shoot an image is pressed. After running the Arduino program, we needed to find a way to read the data sent to the computer's USB port and convert it to a useful image file that we could save to our computer and access. This was done by a Java program made specifically for this purpose which we found online; we ran it in command prompt and used it to save the pictures taken by the camera and name them as "0.bmp , 1.bmp, 2.bmp, 3.bmp" and so on. Then we wrote a batch file for Windows to automatically select the highest number in the picture files' title to determine which was the newest picture taken, rename it to "food.bmp" so that it would continually update a single file called "food.bmp" and move it to a different folder which was synced to Google Drive backup. 

Google Drive backup helped us by automatically retrieving the updated food picture in the linked folder and uploading it to a shared drive which any of us could access on any device. By rewriting the same "food.bmp" file over and over again, we had a constant URL to the picture, we helped with webscraping. This automated process allowed us to progress to the next stage: sending the pictue to our website and image recgonition using machine learning.

The image recognition is run on one of our machines, and it analyzes the image we send over Google Drive with TensorFlow. Once we have the name of the food, we send that data to a web scraper we built. The scraper searches foodnetwork.com for recipes and ingredients involving the recognized food.

Once we have all this we send the recipe, ingredients, and the image to our website which displays it all. However, we did not manage to finish sending the recipe and ingredients to the website, so it only contains the image for now.
