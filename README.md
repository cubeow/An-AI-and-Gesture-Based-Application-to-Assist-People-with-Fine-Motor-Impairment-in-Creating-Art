# An AI and Gesture-Based Application to Assist People with Fine Motor Impairment in Creating Art

## This allows users to perform hand gestures to draw on the computer, and also has voice recognition to change color and use stable diffusion's image-to-image feature to enhance drawings.

This was my freshman year science research project aimed at allowing people with fine motor impairment to create digital art. It uses Openpose's hand tracking software along with the computer camera to detect hand gestures and draw according to the position of the hand. It also uses Google's voice recognition software to implement voice commands. Here are the following functionalities it provides and how to use them:

* Changing color, a choice of red, orange, yellow, green, blue, purple, pink, brown, white, black, and grey. To activate it, you only need to say the color out loud and the program will switch the color
* Start and stop drawing. To begin drawing, say the word "begin". To temporarily stop drawing to make a break in your stroke, say the word "stop". To resume again, just say the word "begin"
* Finish drawing. To finish drawing, say "save the drawing", and it'll move on to the AI segment
* Prompting for stable diffusion's image-to-image feature. Just say the prompt out loud. To change the prompt, just resay the prompt. If you have the correct prompt and would like to finally confirm it and start generating the enhanced image, say "confirm"

## Watch a demo!
https://www.youtube.com/watch?v=MGTBVCl5_5Q