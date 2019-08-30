# Cloudbased Image Transformation

## Overview
This program calls a Cloud Function in the IBM Cloud, wehre it transforms the image given via url into an either  
Black and White Image,  
a Cartoon Image,  
or upscale it by a factor of 2, 3 or 4.  
  
**As of now, Github Pages doesn't add a CORS Header to my jQuery ajax POST request. In order to run this application it needs to be run locally, redirecting traffic over the included node.js server**  

The Cloud Function source code lies in the folder [sourceCode](https://github.com/t-brandl/t-brandl.github.io/tree/master/sourceCode)
Main executable file is [cloudbasedImageTransformation.py](https://github.com/t-brandl/t-brandl.github.io/blob/master/sourceCode/cloudbasedImageTransformation.py)


# Requirements
Python 3.7.2+ *(If the python code is to be run locally, the libraries Pillow and numpy are needed)*  
node.js, including the modules `express`, `request` and `cors`
IBM Cloud Account

## How to use it 
1. Download the repository
2. Rename the `sourceCode/cloudbasedImageTransformation.py` to `__main__.py`
3. Upload it as cloud function into your IBM Account either via UI or using the following command via commandline:  
   ``` 
   ibmcloud fn action create ACTION_NAME APP_FILE --kind RUNTIME 

   ACTION_NAME: Name you want to give the cloud function 
   APP_FILE: your __main__.py 
   RUNTIME: Python:3.7 
   ```
4. Go to your `IBM Cloud Functions` Menu, click `Actions`, select the Action you created, click `Endpoints` and `Enable as Web Action`, now save  
5. ***Optional:***  
   Go to `API`, click `Create Managed API`, set an `API name`, add a `base path` for the API and create an `Operation` 
   ``` 
   PATH: the REST-API path you want it to have, for example: /transform
   Verb: POST
   Package containing action: If your action is in a custom package, select it. Otherwise leave it at (Default)
   Action: Select the Cloudfunctionname you created
   Response content type: application/json
   ```
   Click create, then save
6. Now go to the `API Explorer` tab, click `POST <your Operation PATH>`, then copy the Link next to `POST`.  
   Alternatively, if you skipped the API creation, copy the URL of the Web Action we activated in `Step 4`
7. Edit the `sourceCode/nodejs local/addCORSheader.js` you downloaded from this repository and replace the link of the constant `apiUrl` in line `7` with your link
8. Run the node.js file via CLI
   ``` 
   node addCORSheader.js
   ``` 
9.  Open the `Index.html` in your browser
10. Select the Filter of your choice
11. add a direct url to a `jpeg` or `png` file in the `Image URL` and, if you used `upscale`, select a scale modifier
12. Click Confirm. Note: It'll take a few seconds to load the image


## Source of the included Images

Example forrest image by Johannes Plenio, which can be found [here](https://www.pexels.com/de-de/foto/feldweg-gebaude-haus-hohe-ba-ume-2816284/)  
Example image of the 3 Dogs by Helena Lopes, which can be found [here](https://www.pexels.com/de-de/foto/augen-draussen-fokus-gras-1938123/)




