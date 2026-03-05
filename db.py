import sqlite3

DATABASE = "flashcards.db"


def setup_db():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY,
            subject TEXT,
            question TEXT,
            answer TEXT
        )
    ''')
    db.commit()
    db.close()


def add_flashcard(subject, question, answer):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('INSERT INTO cards (subject, question, answer) VALUES (?, ?, ?)',
                   (subject, question, answer))
    db.commit()
    db.close()


def get_flashcards(subject):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('SELECT question, answer FROM cards WHERE subject = ?', (subject,))
    results = cursor.fetchall()
    db.close()
    
    cards = []
    for row in results:
        cards.append({'q': row[0], 'a': row[1]})
    return cards

def get_all_subjects():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('SELECT DISTINCT subject FROM cards')
    results = cursor.fetchall()
    db.close()
    
    subjects = []
    for row in results:
        subjects.append(row[0])
    return subjects
