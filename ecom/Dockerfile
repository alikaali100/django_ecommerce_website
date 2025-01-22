# انتخاب تصویر پایه
FROM python:3.10-slim

# تنظیمات پوشه کاری
WORKDIR /app

# نصب وابستگی‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کد پروژه
COPY . .

# تنظیمات برای اجرا
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
