<img src="https://cdn.dribbble.com/users/470545/screenshots/2153975/face-morphing.gif" width="300"/>

## Face Morphing (Server Side Script) - See Client Side [Here](https://github.com/tarunnsingh/morph-client).
## Project Demo 
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/_ThVHciEj4g/0.jpg)](http://www.youtube.com/watch?v=_ThVHciEj4g)

### What is Morphing?
The face morphing algorithm morphs between faces using a common set of feature points, placed by hand on each face. To morph between two faces, you need to warp both faces to a common shape so they can be blended together.

### Uses DLIB and OpenCV

### Steps for Local Deployment:
1. Download the 68 facial landmarks predictor by dlib from [here](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) and extract it to the root directory. It should have the following name : _shape_predictor_68_face_landmarks.dat_.
2. Clone the repo.
3. Open terminal/CMD in repo directory.
4. Create a new virtual environment by ```py -m venv env```.
5. Activate the environment by ```env\Scripts\activate```.
6. Intall the packages by ```pip install -r requirements.txt```
7. Start the server by ```python server.py```.

### To be added...
