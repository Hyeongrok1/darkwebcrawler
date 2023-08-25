from flask import Flask, request
import sqlite3, datetime
from multiprocessing import Lock

# db file access if not exist, create file (0 byte).
# then, if you reconnect, you will access the file
con = sqlite3.connect("darkweb.db", check_same_thread=False)
# cursor for handling db file
cursor = con.cursor()
lock = Lock()

try:
    cursor.execute("create table category \
        (no integer PRIMARY KEY AUTOINCREMENT, category text, url text);")
    
    cursor.execute("create table entry \
        (no integer PRIMARY KEY AUTOINCREMENT, category text, link text, description text, last_seen text, added_at text);")
    
    cursor.execute("create table darkweb \
        (no integer PRIMARY KEY AUTOINCREMENT, title text, category text, description varchar(255), url_type varchar(10), tag_text text, url text, referer text, bitcoin text, keyword text, datetime datetime);")
    
    con.commit()    
    
except Exception as err:
    pass

app = Flask(__name__)

@app.route("/kisia", methods=["GET", "POST"])
def kisia():
    if request.method == "GET":
        return "<html><body><h1>Send DarkWeb Info To Me</h1>Welcome, I'm developing this site.</body></html>", 200
    
    print(request.json)
    num = request.json["num"]

    # category table
    if num == 1:
        category = request.json["category"]
        url = request.json["url"]   
        
        lock.acquire()
        try:
            cursor.execute("insert into category(category, url) values(?, ?)", (category, url))
            con.commit()
        except:
            pass
        lock.release()
        
    # entry table
    elif num == 2:
        
        category = request.json["category"]
        onion_link = request.json["Onion link"]
        description = request.json["description"]
        last_seen = request.json["Last seen"]
        added_at = request.json["Added at"]
        lock.acquire()
        try:
            cursor.execute("insert into entry(category, link, description, last_seen, added_at) values(?, ?, ?, ?, ?)", \
                           (category, onion_link, description, last_seen, added_at))
            con.commit()
        except:
            pass
        lock.release()

    # darkweb
    elif num == 3:
        
        title = request.json["title"]
        category = request.json["category"]
        description = request.json["description"]
        type = request.json["type"]
        text = request.json["text"]
        url = request.json["url"]
        referer = request.json["referer"]
        keyword = request.json["keyword"]
        bitcoin = request.json["bitcoin"]
        lock.acquire()
        try:
            cursor.execute("insert into darkweb(title, category, description, url_type, tag_text, url, referer, bitcoin, keyword, datetime)\
                            values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                           (title, category, description, type, text, url, referer, bitcoin, keyword, datetime.datetime.now().strftime("%Y-%m-%d")))
            con.commit()
        except:
            pass
        lock.release()
    
    
    return "kisia", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    