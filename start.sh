#!/bin/bash
set -x

# Navigate to backend directory and start the backend (Django in this case)
echo "Starting Django backend..."
cd chat_backend
python manage.py runserver &

# Navigate to frontend directory and start the frontend (Vue 3 in this case)
echo "Starting Vue 3 frontend..."
cd ../chat_frontend

# Start frontend development server or serve build version
npm run dev # or `npm run build` if using production build

# Keep the script running
wait