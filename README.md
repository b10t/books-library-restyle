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
python main.py
```

дополнительные параметры запуска:
```console
--start_page:   Начальный номер страницы  
--end_page:     Конечный номер страницы  
--dest_folder:  Путь к каталогу с результатами парсинга: картинкам, книгам, JSON  
--skip_imgs:    Не скачивать картинки  
--skip_txt:     Не скачивать книги  
--json_path:    Указать свой путь к *.json файлу с результатами  
```

например:
```bash
python main.py --start_page 700 --dest_folder temp
```
