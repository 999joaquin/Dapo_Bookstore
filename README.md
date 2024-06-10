# Dapo Bookstore Microservices

Project buat Online Bookstore untuk Tugas Besar IAE

## Needs

1. **Python** [python.org](https://www.python.org/).
2. **MySQL** [phpmyadmin](localhost/phpmyadmin)
3. **RabbitMQ** [rabbitmq.com](https://www.rabbitmq.com/).

## Structures

OnlineBookstore/

    server1/
        run.py
        templates/
            index.html
        static/
            css/
                styles.css
            js/
                scripts.js
        database.py

    server2/
        run.py
        database.py

    server3/
        run.py

    database.py
    db_onlinebookstore.sql

### Step cara run

# 1. Buka xampp kek biasa buat start mysql.

# 2. Import file db_onlinebookstore.sql ke phpmyadmin

# 3. Buka vscode, buka 3 terminal trus start virtual enviroment d smua terminalny 
    !! "venv/Scripts/activate" !!

# 4. skrg install dependenciesny
    !! "pip install -r requirements.txt" !!

# 5. cd ke server1, server2, server3 (d masing' terminal)
    !! "cd server1" !!

# 5. kalo udah tinggal run server1, server2, server3
    !! "py run.py" !!

# 6. kalo mau ngecek API bisa lewat browser ato postman kalo di postman
    !! GET, 127.0.0.1:5001/books !!
    !! GET, 127.0.0.1:5002/authors !!

# 7. kalo mau ke UI tinggal buka browser trus ke
    !! 127.0.0.1:5001 !!

# 8. buat event-based pub/sub nya lu pada harus download RabbitMQ dulu dari 
    !! https://www.rabbitmq.com/docs/install-windows !!

# 9. kalo udah keinstall tinggal buka d windows lu pada trus search
    !! RabbitMQ - Start service !!

# 10. cek rabbitMQ nya ke (loginnya guest:guest)
    !! http://localhost:15672/ !!

# 11. cek ada connection ga kalo ada trus queue nya ada tulisan book_created berarti dah aman

# beres.
