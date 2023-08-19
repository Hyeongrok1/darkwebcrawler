from flask import Flask, request
import sqlite3

# db file access if not exist, create file (0 byte).
# then, if you reconnect, you will access the file
con = sqlite3.connect("darkweb_final.db", check_same_thread=False)
# cursor for handling db file
cursor = con.cursor()

try:
    cursor.execute("create table darkweb \
        (no integer PRIMARY KEY AUTOINCREMENT, category text, description varchar(255), url_type varchar(10), tag_text text, url text, referer text, bitcoin text);")
    cursor.execute("create table category \
        (no integer PRIMARY KEY AUTOINCREMENT, category_kind text, category_name text, url text);")
    cursor.execute("create table entry \
        (no integer PRIMARY KEY AUTOINCREMENT, category text, link text, Description text, last_seen text, added_at text, actions text);")
    con.commit()    
    
    # cursor.execute("create table bitcoin \
    #     (no integer PRIMARY KEY AUTOINCREMENT, description varchar(255), tag_text text, url text);")
    # cursor.execute("insert into like_click_table values(?, ?, ?, ?, ?, ?)", (1, "kisia", "kisia_pw", "cookie", 2239, datetime.now()))
except:
    pass

app = Flask(__name__)

@app.route("/kisia", methods=["GET", "POST"])
def kisia():
    print(request.json)
    
    num = request.json["num"]

    if num == 1:
        # data = {
        #     "num": 2,
        #     "category_kind": category_kind,
        #     "category_name": li_tag.text,
        #     "url": href
        # }
        category_kind = request.json["category_kind"]
        category_name = request.json["category_name"]
        url = request.json["url"]   
        try:
            cursor.execute("insert into category(category_kind, category_name, url) values(?, ?, ?)", (category_kind, category_name, url))
        except:
            cursor.execute("insert into category(no, category_kind, category_name, url) values(?, ?, ?, ?)", (1, category_kind, category_name, url))
             
    elif num == 2:
        
        category = request.json["category"].replace(":", "")
        onion_link = request.json["Onion link"]
        description = request.json["Description"]
        last_seen = request.json["Last seen"]
        added_at = request.json["Added at"]
        actions = request.json["Actions"]   
        try:
            cursor.execute("insert into entry(category, link, Description, last_seen, added_at, actions) values(?, ?, ?, ?, ?, ?)", (category, onion_link, description, last_seen, added_at, actions))
        except:
            cursor.execute("insert into entry(no, category, link, Description, last_seen, added_at, actions) values(?. ?, ?, ?, ?, ?, ?)", (1, category, onion_link, description, last_seen, added_at, actions))
    
    elif num == 3:
        
        description = request.json["description"]
        category = request.json["category"]
        type = request.json["type"]
        text = request.json["text"]
        url = request.json["url"]
        referer = request.json["referer"]
        bitcoin = request.json["bitcoin"]
        try:
            cursor.execute("insert into darkweb(category, description, url_type, tag_text, url, referer, bitcoin) values(?, ?, ?, ?, ?, ?, ?)", (category, description, type, text, url, referer, bitcoin))
        except:
            cursor.execute("insert into darkweb(no, category, description, url_type, tag_text, url, referer, bitcoin) values(?, ?, ?, ?, ?, ?, ?, ?)", (1, category, description, type, text, url, referer, bitcoin))
        
    con.commit()
    
    return "kisia", 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1023)