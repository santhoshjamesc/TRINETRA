# drishyam
S7 CSA FACE RECOGNITION AND GENERATION SOFTWARE

download the trained model = https://drive.google.com/drive/folders/1RiOF1c_Z-qF9VWsne_cDagiAFpdfWI_Q?usp=sharing
paste it


BIM.PY

the file bim.py is runned to take the best face for each person in dataset and crop the face and save in a folder called persons
everytime it runs the persons folder will be emptied


DATASETGEN.PY

this file is used to generate images by varying img attributes


SIAMESE.PY

this is a hardcoded file where the path of dataset and epochs are already hardcoded
this program is called train the model using the given dataset
we belive the more you train the more accurate it become 

recogggg1.py
its the main file that handles face recognition and sending email
face detection and verify.py files are imported in recogggg1.py


if recognition not working check similarity threshold then check recognized faces folder


FOLDER PERSON = output of bim.py
FOLDER recognized faces = faces that passed first checking and waiting for second checking
