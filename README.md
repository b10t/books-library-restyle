# Скачивание книг с [tululu.org](https://tululu.org/)

Программа позволяет скачивать книги, обложки книг с сайта [https://tululu.org/](https://tululu.org/).
  
### Как установить

Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```bash
pip install -r requirements.txt
```

### Как запускать
```bash
python main.py start_id end_id
```

где:
```console
start_id:   Начальный id книги
end_id:     Конечный id книги
```

например:
```bash
python main.py 1 10
```
