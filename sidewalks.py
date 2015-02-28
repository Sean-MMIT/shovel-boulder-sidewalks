from flask import Flask
from flask import render_template
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    snowData = returnLastSnowDateAndTime()
    return render_template('index.html', snowData=snowData)

def returnLastSnowDateAndTime():
    snowReportResponse = requests.get('http://www.nws.noaa.gov/data/obhistory/KBDU.html')
    #forecastResponse = requests.get('https://api.forecast.io/forecast/a1dcd3de7338008cc494d5677bcee08e/40.04,105.23')
    snowReportSoup = BeautifulSoup(snowReportResponse.text)
    lastSnowReport = snowReportSoup.find(text=re.compile(r'Snow'))
    snowRow = lastSnowReport.parent.parent
    snowDateStr = snowRow.find("td").string
    #TODO: Capture date properly and adjust forecast based on calendar
    snowTimeStr = snowRow.find(text=re.compile(r'..:..')).string
    snowTimeTup = datetime.strptime( snowTimeStr, "%H:%M")
    snowTime = snowTimeTup.strftime("%r")
    return { 'lastSnowReport':lastSnowReport, 'snowDate':ord(snowDateStr), 'snowTime':snowTime }

def ord(n):
    n = int(n)
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

if __name__ == "__main__":
    app.run()