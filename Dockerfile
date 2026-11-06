FROM python:3.14-slim
WORKDIR /app
COPY inventory_manager.py .
CMD ["python3","inventory_manager.py"]