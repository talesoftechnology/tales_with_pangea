from flask import Flask, render_template, request, redirect, url_for, session, flash
from pangea.services import Redact, FileIntel
from pangea.config import PangeaConfig
from pangea.services import Audit
from details import info, config
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 *1024
app.config['ALLOWED_EXTENSIONS'] = ['.txt','.cfg']
#app.permanent_session_lifetime = timedelta(minutes=5)

config1 = PangeaConfig(domain=os.getenv("DOMAIN"))
audit = Audit("pts_6cbbz3ikyknt4ei7zkbp7nrq26hrg7x4", config = config1)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login_customer', methods = ["POST", "GET"])
def login_customer():
    if request.method == "POST":
        #session.permanent = True
        if request.form["ip"] == '192.66.66.3' and request.form["username"] == "Abraham" and request.form["password"] == "lincoln150":
            audit.log("Customer: " + str(request.form['name']) + "logged into " + str(request.form["ip"]) + "and ran command " + str(request.form["command"]))
            session["command"] = request.form["command"]
            session["name"] = request.form["name"]
            return redirect(url_for("results_c"))
        else:
            return render_template('wrong_credentials.html')
    else:
        return render_template('login_customer.html')

@app.route('/login_technician', methods = ["POST", "GET"])
def login_technician():
    if request.method == "POST":
        #session.permanent = True
        if request.form["ip"] == '192.66.66.3' and request.form["username"] == "Abraham" and request.form["password"] == "lincoln150":
            audit.log("Technician: " + str(request.form['name']) + "logged into " + str(request.form["ip"]) + "and ran command " + str(request.form["command"]))
            session["command"] = request.form["command"]
            session["name"] = request.form["name"]
            return redirect(url_for("results"))
        else:
            return render_template('wrong_credentials.html')
    else:
        return render_template('login_technician.html')

@app.route('/logout')
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"you have been logged out,")
    session.pop("user", None)
    session.pop("command", None)
    session.pop("ip", None)
    session.pop("username", None)
    session.pop("password", None)
    return render_template("logout.html")


@app.route("/results", methods = ["POST", "GET"])
def results():
    redact = Redact(token = os.getenv("TOKEN"))
    check_res = redact.redact_structured(info)
    info_redacted = check_res.raw_result["redacted_data"]
    return render_template("results.html", cname = info_redacted ["Company Name"],
    status = info_redacted ["Status"],
    ip = info_redacted ["WAN IP Address"],
    vendor = info_redacted["Vendor"],
    customer_name = info_redacted ["Customer Name"],
    number = info_redacted["Phone Number"],
    mail = info_redacted["Email ID"],
    address = info_redacted["Address"],
    city = info_redacted["City"],
    state = info_redacted ["State"], name = str(session["name"]), 
    output = config[str(session["command"])])
    
@app.route("/results_c", methods = ["POST", "GET"])
def results_c():
        redact = Redact(token = os.getenv("TOKEN")) 
        check_res = redact.redact_structured(config)
        config_redacted = check_res.raw_result["redacted_data"]
        if request.method == 'GET':
            return render_template("results_c.html", cname = info ["Company Name"],
            status = info ["Status"],
            ip = info ["WAN IP Address"],
            vendor = info ["Vendor"],
            customer_name = info ["Customer Name"],
            number = info ["Phone Number"],
            mail = info ["Email ID"],
            address = info ["Address"],
            city = info ["City"],
            state = info ["State"], name = str(session["name"]), 
            output = config_redacted[str(session["command"])])
        if request.method == 'POST':
            return redirect(url_for("review_submitted"))


@app.route('/save_review', methods=['POST'])
def review_submitted():
    redact = Redact(token=os.getenv("TOKEN"))
    check_res = redact.redact(text = request.form['review'])
    review = check_res.raw_result['redacted_text']
    reviewer = request.form['reviewer']

    # read the existing reviews from the file
    with open('reviews.txt', 'r') as f:
        reviews = f.read().splitlines()

    # append the new review to the list
    reviews.append(f'{reviewer}~tot~ {review}')

    # write the entire list back to the file
    with open('reviews.txt', 'w') as f:
        for r in reviews:
            f.write(f'{r}\n')

    return redirect(url_for('reviews_page'))


@app.route('/reviews')
def reviews_page():
    with open('reviews.txt', 'r') as f:
        reviews = f.read().splitlines()
    
    review_list = []
    for review in reviews:
        parts = review.split("~tot~")
        review_text = parts[0].strip()
        reviewer_name = parts[1].strip()
        review_list.append({'review': review_text, 'reviewer': reviewer_name})
    
    return render_template('reviews.html', reviews=review_list)

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    if request.method == "POST":
        try:
            file = request.files['file']
            print(file)
            if file:
                file.save(f'uploads/uploaded_file')
                intel = FileIntel(token=os.getenv("TOKEN"))
                response = intel.filepathReputation(filepath="./uploads/uploaded_file", provider = "reversinglabs")
                os.remove('./uploads/uploaded_file')
                audit.log("File uploaded by " + str(request.form['name']))
                if response.result.data.verdict == 'malicious':
                    return render_template('after_upload.html', message = '''Our security systems have detected a potentially malicious file during the upload process.\n 
                    Please refrain from uploading such files for the safety of our platform and users''', name = request.form['name'])
                else:
                    return render_template('after_upload.html', message = '''Configuration pushed successfully to the device
                    ''', name = request.form['name'])

        except:
            return """Check the uploaded file, \n
            File must be less than 8 MB\n
            File must be a text file or configuration file\n
            File extensions allowed : ('.txt', '.cfg')"""
        
    if request.method == "GET":
        return render_template('upload_page.html')

@app.route('/upload_check')
def upload_check():
    return render_template('upload_check.html', filecontent = "Hello")

@app.route('/admin', methods = ['POST', 'GET'])
def admin():
    return render_template('admin_page.html')

@app.route('/documentation' , methods = ['GET'])
def documentation():
    return render_template('documentation.html')

if __name__ == '__main__':
    app.run(debug=True)