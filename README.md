![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)
# Speech-Recognition-Deployment
### About the project
This repository is the continuation of my other project [Arabic Speech recognition](https://github.com/lutfi640/Arabic-Speech-Recognition) that the saved model are being served on Heroku platform. The model will be served cloud so from any platform can use it like Android application or Website just by using the API.

### System Design
The design of my app is to deploy the model using Heroku and the android App can call the API to predict new audio. This is the design system of my developed app :

![System Design](https://github.com/lutfi640/Speech-Recognition-Deployment/blob/master/Other/System%20Design.png)

### How to deploy on Heroku
1. Create Heroku account and login, after that create a new App on the top bar after that fill the necessary information about your new App
2. Make sure everything's is pushed to repo :
  1. Saved model
  2. Python file (Flask)
  3. Procfile (without extension)
  4. Requirements (txt file contains every library that needed)
3. Then click Deploy Branch

Please take a look on this [Heroku documentation](https://devcenter.heroku.com/articles/github-integration) on Github Integration Deployment to perform your own deployment. 
