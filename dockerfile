# Python 3.11 का बेस इमेज
FROM python:3.11-slim

# वर्किंग डायरेक्टरी सेट करें
WORKDIR /app

# requirements.txt को कॉपी करें और पैकेजेज इंस्टॉल करें
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ऐप के फाइल्स को कॉपी करें
COPY . .

# एप्लिकेशन को रन करें
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
