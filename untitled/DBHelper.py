import sqlite3
import model.article

def create_table():
    conn = sqlite3.connect('articles.db')
    try:
        create_tb_cmd = '''
            CREATE TABLE IF NOT EXISTS article
            (url TEXT,
            name TEXT,
            hasVideo INT,
            hasUpload INT );
            '''
        conn.execute(create_tb_cmd)
        conn.commit()
    except:
        print
        "Create table failed"
        return False
    finally:
        conn.close()

def insertArticle(article):
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()
    cursor.execute("insert into  article (url,name,hasVideo,hasUpload) values (?,?,?,?)",(article.url,article.name,1,0))
    cursor.close()
    conn.commit()
    conn.close()

def findArticle(url):
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()
    cursor.execute("select * from article where url=?",(url,))
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    if len(values) > 0:
        return 1
    else:
        return 0


