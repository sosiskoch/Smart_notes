import json
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QInputDialog, QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget, QTextEdit
import os

if not os.path.exists("notes.json"):
    notes = {
        "Привет мир!": {
            "text": "Это приветственная статья.",
            "tags": ["Привет", "мир"],
        }
    }
    with open("notes.json", "w", encoding="utf-8") as f:
        json.dump(notes, f, sort_keys=True, ensure_ascii=False)

app = QApplication([])
main_window = QWidget()

# Тут создаем все необходимые виджеты
text = QTextEdit()  # Текст статьи
articles = QListWidget()  # Список статей
tags = QListWidget() # Список тегов
add_article = QPushButton("Добавить заметку")
del_article = QPushButton("Удалить заметку")
save_article = QPushButton("Сохранить заметку")
add_tag = QPushButton("Добавить к заметке")
del_tag = QPushButton("Открепить от заметки")
filter_articles = QPushButton("Искать заметки по тэгу")
tag = QLineEdit() # Поле ввода тэга для поиска или добавления
tag.setPlaceholderText("Введите тэг...")
articles_title = QLabel("Список заметок")  # Заголовок списка заметок
tags_title = QLabel("Список тэгов")  # Заголовок списка тэгов

# Тут располагаем виджеты
cols = QHBoxLayout()
cols.addWidget(text)
rows = QVBoxLayout()
cols.addLayout(rows)
rows.addWidget(articles_title)
rows.addWidget(articles)
row1 = QHBoxLayout()
row1.addWidget(add_article)
row1.addWidget(del_article)
rows.addLayout(row1)
rows.addWidget(save_article)
rows.addWidget(tags_title)
rows.addWidget(tags)
rows.addWidget(tag)
row2 = QHBoxLayout()
row2.addWidget(add_tag)
row2.addWidget(del_tag)
rows.addLayout(row2)
rows.addWidget(filter_articles)

# Тут работаем с данными
with open("notes.json", "r", encoding="utf-8") as f:
    notes = json.load(f)
articles.addItems(notes)

def onClick():
    title = articles.selectedItems()[0].text()
    article = notes[title]
    tags.clear()
    tags.addItems(article["tags"])
    text.setText(article["text"])
articles.itemClicked.connect(onClick)

def add_article_click():
    text, ok = QInputDialog().getText(main_window, "Добавить заметку", "Описание:")
    if ok:
        notes[text] = {"text": "", "tags": []}
        articles.addItem(text)
add_article.clicked.connect(add_article_click)

def save_article_click():
    title = articles.selectedItems()[0].text()
    article = notes[title]
    article["text"] = text.toPlainText()
    with open("notes.json", "w", encoding="utf-8") as f:
        json.dump(notes, f, sort_keys=True, ensure_ascii=False)
save_article.clicked.connect(save_article_click)

def del_article_click():
    title = articles.selectedItems()[0].text()
    res = QMessageBox.question(
        main_window, 
        "Удалить заметку", 
        "Вы хотите удалить "+title+"?",
        QMessageBox.Yes | QMessageBox.No 
    )
    if res == QMessageBox.Yes:
        del notes[title]
        with open("notes.json", "w", encoding="utf-8") as f:
            json.dump(notes, f, sort_keys=True, ensure_ascii=False)
        text.setText("")
        tags.clear()
        articles.clear()
        articles.addItems(notes)
del_article.clicked.connect(del_article_click)

def add_tag_click():
    title = articles.selectedItems()[0].text()
    article = notes[title]
    new_tag = tag.text()
    if new_tag and new_tag not in article["tags"]:
        article["tags"].append(new_tag)
        tags.addItem(new_tag)
add_tag.clicked.connect(add_tag_click)

def del_tag_click():
    title = articles.selectedItems()[0].text()
    article = notes[title]
    tag_title = tags.selectedItems()[0].text()
    article["tags"].remove(tag_title)
    tags.clear()
    tags.addItems(article["tags"])
del_tag.clicked.connect(del_tag_click)

def filter_articles_click():
    if filter_articles.text() == "Искать заметки по тэгу":
        new_articles = []
        tag_text = tag.text()
        for title in notes:
            article = notes[title]
            if tag_text in article["tags"]:
                new_articles.append(title)
        articles.clear()
        articles.addItems(new_articles)
        filter_articles.setText("Отменить поиск")
    else:
        articles.clear()
        articles.addItems(notes)
        filter_articles.setText("Искать заметки по тэгу")
    
filter_articles.clicked.connect(filter_articles_click)

main_window.setLayout(cols)
main_window.show()
app.exec_()