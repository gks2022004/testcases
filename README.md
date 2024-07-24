# Assignment

1. Used React.js for frontend.
2. For the backend, I have used the Flask and socket.io 
3. Made REST API and integrated it with PostgreSQL to fetch the data from table "testcases"
   using methods like GET, POST, PUT, and DELETE.
4. Implement real-time data synchronization between the web page and the database using Flask Cors and socket.io  
5. Display the retrieved data on the web page, following the provided UI design image.


![image](https://github.com/user-attachments/assets/840a2468-9d82-4e52-b208-3ee935f135b1)

# How to run 

- Git clone the repository
  `git clone https://github.com/gks2022004/testcases.git`
  
- Change the directory to frontend and do
   `npm install`
then `npm run dev`

- Then change the directory to the backend and use these commands
  `pip install Flask Flask-SQLAlchemy Flask-SocketIO psycopg2-binary`
  `pip install flask-cors`
after this use `python app.py`

- Now your web application will run and you can use it.

## NOTE: 
### Don't forget to add the `SQLALCHEMY_DATABASE_URI` in backend env file and `VITE_BACKEND_URL=http://localhost:5000` in frontend env file
