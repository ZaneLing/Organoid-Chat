**1 Start**
  **1.1 If you want to run it locally:**
    **1.1.1** change the code in /chat_frontend/src/main.js into the first line
      app.config.globalProperties.$apiBaseUrl = 'http://127.0.0.1:8000';
    **1.1.2** then run the command following
      ./start.sh
 
  **1.2 If you want to run it on the server:**
      **1.2.1** change the code in /chat_frontend/src/main.js into the first line
        app.config.globalProperties.$apiBaseUrl = 'http://172.16.120.14:8081';
      **1.2.2** then run the command following
        npm run build
      **1.2.3** then copy the content in /chat_frontend/dist to the server
        /var/www/chat_frontend

**2 Release**
  **2.1 Backend**
    Django
  **2.2 Frontend**
    Vue3 + TailwindCSS
