# HSEEmoRec

<p align="center"> <img src="https://flask.palletsprojects.com/en/2.1.x/_static/flask-icon.png" alt="Flask" width="80" height="80"/> 
  <img src="https://seaborn.pydata.org/_static/logo-wide-lightbg.svg" alt="Seaborn" width="80" height="80"/> 
  <img src="https://pytorch.org/assets/images/pytorch-logo.png" alt="PyTorch" width="80" height="80"/> 
</p>

This web application is built with the Flask framework and allows users to analyze staff satisfaction using an EfficientNet-B0 backbone and an 
EmoRec classifier. The app supports registration and login for users, and allows them to save analysis by various parameters such as sex, 
job position, age, weekday, etc. All analysises will be saved locally.

All user account info (password, email, e.t.c) will be saved locally in instance/database.db. 
Users info (for analysis) will be saved in usersdata/usersdata.csv with fields
|id|email|position|sex|age|date|weekday|is_weekend|emotion|
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Installation

To install the necessary dependencies, run the following command:
1. Clone the repository: 
```
git clone https://github.com/endlessagony/HSEEmoRec.git
```
2. Install the requirements
```
pip install -r requirements.txt
```
## Usage

To run the app, run the following command:
```
python main.py
```
This will start the Flask development server, and the app will be accessible in your web browser at http://localhost:5000.

## Screenshots

### Home page
![home](https://github.com/endlessagony/HSEEmoRec/assets/74978814/0484ff2e-b558-47c5-a92f-368ee2534bbe)

### Login page
![login](https://github.com/endlessagony/HSEEmoRec/assets/74978814/23a3cc88-ec6d-4200-8c40-f35c86f89e44)

### Sign-up page
![sign-up](https://github.com/endlessagony/HSEEmoRec/assets/74978814/6dd94c6d-c8e0-4f72-8aa6-a1a497c85bf1)

### Analysis page
![analyze](https://github.com/endlessagony/HSEEmoRec/assets/74978814/2b243218-6e7f-4005-92f8-2ac8583c1d8e)

#### P.S. Feature field takes values: sex, age, weekday, position, is_weekend.
