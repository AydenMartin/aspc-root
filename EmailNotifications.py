# Define these once; use them twice!
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ReportGenerator as rg
def sendMessage():
    strFrom = 'aspcrootserver@gmail.com'
    strTo = 'aspcrootserver@gmail.com'
    rg.genSigStrGraph_Example()
    # Create the root message and fill in the from, to, and subject headers
    msgRoot =  MIMEMultipart('related')
    msgRoot['Subject'] = 'test message'
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)
    msgText = MIMEText("""\
    <!DOCTYPE html> 
    <html>
        <head>
        <title>Diagnostic Report</title>
        <style>
            body { 
                background-color: YellowGreen; 
                border-style:solid;
                border-width:3 ;
                border-color:black;

            }
            p { 
                color: black;
                order-style:solid;
                border-width:3 ;
                border-color:black;
            }
        </style>
        </head>
    <body style="border:1px solid black; height:1000px">
        <h1 style="text-align:center; text-decoration:underline;">Diagnostic Info</h1>
        <img src="cid:image1" width="600px", height="400px" style="margin-left:3.5vw; margin-right:auto">
        <h2 style="color:red; font-size:15px;text-align:center;"> Warning: Several leaf nodes performing poorly </h2>
        
    </body>
    </html>
    """, 'html')
    # We reference the image in the IMG SRC attribute by the ID we give it below
    #msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open('Charts/speed.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    # Send the email (this example assumes SMTP authentication is required)
    import smtplib
    smtp=smtplib.SMTP_SSL('smtp.gmail.com', 465)

    smtp.login('aspcrootserver@gmail.com', '1654GRBP')
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()

sendMessage()