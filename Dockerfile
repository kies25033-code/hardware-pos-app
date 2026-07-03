# Python base image ကို သုံးမယ်
FROM python:3.14.6-slim

# Working directory
WORKDIR /app

# လိုအပ်တဲ့ library တွေ install လုပ်မယ်
COPY requirements.txt .
RUN pip install -r requirements.txt

# App ဖိုင်တွေကို copy ကူးမယ်
COPY . .

# App ကို စတင်ဖို့ port 8080 ကို သတ်မှတ်မယ်
EXPOSE 8080

# Streamlit ကို run မယ်
CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]