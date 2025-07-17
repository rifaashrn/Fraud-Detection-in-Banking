from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # SMTP server address
app.config['MAIL_PORT'] = 587  # SMTP port
app.config['MAIL_USE_TLS'] = True  # Enable TLS
app.config['MAIL_USERNAME'] = 'bankyenproject@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'mtff nqut hxct hpun'  # Your email password

mail = Mail(app)

def load_model():
    # Load your dataset
    credit_card_data = pd.read_csv("creditcard.csv")
    
    # Separate the dataset into legitimate and fraudulent transactions
    legit = credit_card_data[credit_card_data.Class == 0]
    fraud = credit_card_data[credit_card_data.Class == 1]

    # Combine both classes, balancing the data
    legit_sample = legit.sample(n=492)
    new_dataset = pd.concat([legit_sample, fraud], axis=0)
    
    # Select only the top 10 features based on importance or domain knowledge
    selected_features = ['Time','V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8','V9','V10','Amount']
    
    # Extract features and target variable
    X = new_dataset[selected_features]
    Y = new_dataset['Class']
    
    # Split the data into training and testing sets
    X_train, _, Y_train, _ = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)
    
    # Train the logistic regression model
    model = LogisticRegression()
    model.fit(X_train, Y_train)

    return model


# Load the model once when the application starts
model = load_model()

@app.route('/')
def index():
    return render_template('index.html', result=None)

@app.route('/predict')
def startnew():
    return render_template('index2.html',result=None)
@app.route('/predict1', methods=['GET'])
def predict():
    if request.method == 'GET':
        try:
            # Get user input from the form for the top 12 features
            features = [float(request.args.get(f'feature{i}', 0.0)) for i in range(1, 13)]  # Adjust range to match top 12 features

            # Make a prediction
            result = model.predict([features])

            return render_template('index2.html', result=result[0])

        except Exception as e:
            return render_template('index2.html', error=str(e))
    else:
        # Handle GET method
        return render_template('index2.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    recipient = request.form['recipient']
    subject = 'Bank Fraud transaction'
    body = 'We regret to inform you that our system has detected a potentially fraudulent transaction associated with your account. Ensuring the security of your financial information is our top priority, and we are taking immediate action to investigate this matter further.'

    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.body = body

    try:
        mail.send(msg)
        res="Mail sent successfully!"
        return render_template('index6.html', ans=res)
    except Exception as e:
        return str(e)


@app.route('/rules')
def progress():
    return render_template('index3.html');

@app.route('/graph')
def graph():
    return render_template('index4.html');

@app.route('/about')
def about():
    return render_template('index5.html');


if __name__ == '__main__':
    app.run(debug=True)
