import requests
from dateutil.relativedelta import relativedelta
import datetime
import smtplib

# Foursquare Token
# https://foursquare.com/developers/explore
API_TOKEN = ""

# Amazon SES
SMTP_AUTH_USER = ""
SMTP_AUTH_PWD = ""

EMAIL = ""

def get_checkins_from_past(years):
    endDate = datetime.datetime.now() - relativedelta(years=years)
    startDate = endDate - datetime.timedelta(days=8)
    
    afterTimestamp = int(startDate.timestamp())
    beforeTimestamp = int(endDate.timestamp())
    
    url = 'https://api.foursquare.com/v2/users/self/checkins?oauth_token={}&v=20180806&afterTimestamp={}&beforeTimestamp={}'.format(API_TOKEN, afterTimestamp, beforeTimestamp)
    
    req = requests.request('GET', url)
    
    return req.json()['response']['checkins']['items']

def get_html_checkins_content():
    html_msg = ""

    for year in range(1, 6):
        checkins = get_checkins_from_past(year)

        for item in checkins:
            date_str = datetime.datetime.fromtimestamp(item['createdAt']).strftime('%Y-%m-%d %H:%M')

            if 'address' in item['venue']['location']:
                address = item['venue']['location']['address']
            else:
                address = item['venue']['location']['formattedAddress'][0]

            html_msg = html_msg + date_str + " - " + item['venue']['name'] + " (" + address + ")"
            html_msg = html_msg + "<br>"

        html_msg = html_msg + "<hr>"

    return html_msg

def send_email(html_msg):

    # Send Email
    fromaddr = EMAIL
    toaddrs  = EMAIL

    msg = ""
    msg = msg + "From: Carlos Kobayashi <" + EMAIL +">\n"
    msg = msg + "To: Carlos Kobayashi <" + EMAIL +">\n"
    msg = msg + "MIME-Version: 1.0\n"
    msg = msg + "Content-type: text/html\n"
    msg = msg + "Subject: Foursquare Last Years Check Ins\n"
    msg = msg + "\n"
    msg = msg + html_msg

    server = smtplib.SMTP('email-smtp.us-east-1.amazonaws.com:587')
    server.ehlo()
    server.starttls()
    server.login(SMTP_AUTH_USER, SMTP_AUTH_PWD)
    server.sendmail(fromaddr, toaddrs, msg.encode("utf8"))
    server.quit()

if __name__ == '__main__':
    html_msg = get_html_checkins_content()
    send_email(html_msg)
