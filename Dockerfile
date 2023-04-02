FROM parados/ta-lib-python-3.6

WORKDIR /app

#COPY requirements.txt .

RUN pip install numpy krakenex pykrakenapi TA-Lib

COPY src cryptopilot

CMD ["python", "-m", "cryptopilot.main"]
