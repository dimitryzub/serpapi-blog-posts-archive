👉**Кратко о сути**: обучающий демо-блог пост о парсинге исторических органических результатов с 2017 по 2021 года используя пагинацию, а так же, цитируемых результатов с Google Scholar, и их сохранение в CSV и SQLite базу данных используя Python и библиотеку для веб-скрейпинга от SerpApi.

🔨**Что понадобится**: понимание циклов, структур данных, обработка исключений, и, базовое понимание `CSS` селекторов. А так же `serpapi`, `urllib`, `pandas`, `sqlite3` библиотек.

⏱️**Сколько времени займет**: ~20-60 минут на чтение и реализацию.

___

- <a href="#what_will_be_scraped">Что парсим</a>
    - <a href="#prerequisites">Что понадобится</a>
- <a href="#process">Процесс</a>
    - <a href="#organic_results">Органические результаты</a>
    - <a href="#cite_results">Цитируемые результаты</a>
    - <a href="#save_csv">Сохраняем в CSV</a>
    - <a href="#save_sqlite">Сохраняем в SQLite</a>
- <a href="#full_code">Код целиком - парсинг</a>
- <a href="#saving_code">Код целиком - сохранение</a>
- <a href="#links">Ссылки</a>
- <a href="#outro">Что дальше</a>


<h2 id="what_will_be_scraped">Что парсим</h2>

Из органических результатов:

![what_will_be_scraped_1_01](https://user-images.githubusercontent.com/78694043/147768216-70816917-01f4-490a-854a-3ac1ad5f83ed.png)

📌Примечание: На Google Scholar есть максимальный лимит в 100 страниц, поэтому когда вы видите `About xxx.xxx results` это не означает что все результаты отображаются и их можно спарсить. Так же как это происходит с Гугл поиском.


Из цитируемых результатов:

![what_will_be_scraped_3](https://user-images.githubusercontent.com/78694043/147768207-27016821-7ae9-4243-8e3b-29ebb1a097c2.png)


<h2 id="prerequisites">Что понадобится</h2>

**Отдельное вирутуальное окружение**

Если вы не имели дело с виртуальным окружением ранее, взгляните на посвященный этому блог пост на английском языке - [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/).

Вкратце, это штука, которая создает независимый набор установленных библиотек включая возможность установки разных версий Python которые могут сосуществовать друг с другом одновременно на одной системе, что в свою очередь предотвращает конфликты библиотек и разных версий Python.

📌Примечание: использование виртуальной среды не является строгим требованием.

Установка библиотек:

```lang-none
pip install google-search-results
pip install pandas
```

____

<h2 id="process">Процесс</h2>

![google_scholar_process_1_03_1](https://user-images.githubusercontent.com/78694043/146953943-dd19ebfa-7080-41bc-b674-4a1af7619d8a.png)

Если объяснение не нужно:
- забирайте код в секции <a href="#full_code">весь код целиком</a>,
- [забирайте код целиком из GitHub репозитория](https://github.com/dimitryzub/py-google-scholar-organic-cite-to-csv-sqlite),
- [пробуйте сразу в online IDE](https://replit.com/@serpapi/Scrape-historic-Google-Scholar-Organic-and-Citation-results#main.py).

___

![google_scholar_organic_results_2_1](https://user-images.githubusercontent.com/78694043/146953922-60c1b7a9-8783-43d0-902f-d291a1a99273.png)

<h2 id="organic_results">Органические результаты</h2>

```python
import os
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl


def organic_results():
    print("extracting organic results..")

    params = {
        "api_key": os.getenv("API_KEY"), # ключ для аутентификации в SerpApi 
        "engine": "google_scholar",
        "q": "minecraft redstone system structure characteristics strength",  # поисковый запрос
        "hl": "en",        # язык
        "as_ylo": "2017",  # с 2017
        "as_yhi": "2021",  # до 2021
        "start": "0"       # первая страница
    }

    search = GoogleSearch(params)

    organic_results_data = []

    loop_is_true = True

    while loop_is_true:
        results = search.get_dict()

        print(f"Currently extracting page №{results['serpapi_pagination']['current']}..")

        for result in results["organic_results"]:
            position = result["position"]
            title = result["title"]
            publication_info_summary = result["publication_info"]["summary"]
            result_id = result["result_id"]
            link = result.get("link")
            result_type = result.get("type")
            snippet = result.get("snippet")
  
            try:
              file_title = result["resources"][0]["title"]
            except: file_title = None
  
            try:
              file_link = result["resources"][0]["link"]
            except: file_link = None
  
            try:
              file_format = result["resources"][0]["file_format"]
            except: file_format = None
  
            try:
              cited_by_count = int(result["inline_links"]["cited_by"]["total"])
            except: cited_by_count = None
  
            cited_by_id = result.get("inline_links", {}).get("cited_by", {}).get("cites_id", {})
            cited_by_link = result.get("inline_links", {}).get("cited_by", {}).get("link", {})
  
            try:
              total_versions = int(result["inline_links"]["versions"]["total"])
            except: total_versions = None
  
            all_versions_link = result.get("inline_links", {}).get("versions", {}).get("link", {})
            all_versions_id = result.get("inline_links", {}).get("versions", {}).get("cluster_id", {})
  
            organic_results_data.append({
              "page_number": results["serpapi_pagination"]["current"],
              "position": position + 1,
              "result_type": result_type,
              "title": title,
              "link": link,
              "result_id": result_id,
              "publication_info_summary": publication_info_summary,
              "snippet": snippet,
              "cited_by_count": cited_by_count,
              "cited_by_link": cited_by_link,
              "cited_by_id": cited_by_id,
              "total_versions": total_versions,
              "all_versions_link": all_versions_link,
              "all_versions_id": all_versions_id,
              "file_format": file_format,
              "file_title": file_title,
              "file_link": file_link,
            })

            if "next" in results["serpapi_pagination"]:
                search.params_dict.update(dict(parse_qsl(urlsplit(results["serpapi_pagination"]["next"]).query)))
            else:
                loop_is_true = False

    return organic_results_data
```

### Объяснение парсинга органических результатов используя пагинацию

Импортируем `os`, `serpapi`, `urllib` библиотеки:

```python
import os
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
```

Создаем и передаем поисковые параметры в `GoogleSearch()` где происходит все извлечение данных на бэкенде SerpApi:

```python
params = {
  "api_key": os.getenv("API_KEY"), # ключ для аутентификации в SerpApi
  "engine": "google_scholar",
  "q": "minecraft redstone system structure characteristics strength",  # поисковый запрос
  "hl": "en",        # язык
  "as_ylo": "2017",  # с 2017
  "as_yhi": "2021",  # до 2021
  "start": "0"       # первая страница
}

search = GoogleSearch(params) # извлечение данных происходит тут
```

Создаём временный список `list()` для того чтобы сохранить данные которые будут дальше использоваться для сохранения в CSV или переданы`cite_results()` функции:

```python
organic_results_data = []
```

Создаём `while` цикл для парсинга данных со всех доступных страниц:

```python
loop_is_true = True

while loop_is_true:
    results = search.get_dict()
    
    # парсинг данных происходит тутачки..
    
    if "next" in results["serpapi_pagination"]:
        search.params_dict.update(dict(parse_qsl(urlsplit(results["serpapi_pagination"]["next"]).query)))
    else:
        loop_is_true = False
```

- Если нет ссылки на следующую `"next"` страницу - `while` прекратится установив `loop_is_true` на `False`.
- Если есть ссылка на следующую `"next"` страницу, `search.params_dict.update` разберет ссылку на части и передаст её к `GoogleSearch(params)` для результатов с новой страницы.

Парсим данные в `for` цикле:

```python
for result in results["organic_results"]:
    position = result["position"]
    title = result["title"]
    publication_info_summary = result["publication_info"]["summary"]
    result_id = result["result_id"]
    link = result.get("link")
    result_type = result.get("type")
    snippet = result.get("snippet")
  
    try:
      file_title = result["resources"][0]["title"]
    except: file_title = None
  
    try:
      file_link = result["resources"][0]["link"]
    except: file_link = None
  
    try:
      file_format = result["resources"][0]["file_format"]
    except: file_format = None
  
    try:
      cited_by_count = int(result["inline_links"]["cited_by"]["total"])
    except: cited_by_count = None
  
    cited_by_id = result.get("inline_links", {}).get("cited_by", {}).get("cites_id", {})
    cited_by_link = result.get("inline_links", {}).get("cited_by", {}).get("link", {})
  
    try:
      total_versions = int(result["inline_links"]["versions"]["total"])
    except: total_versions = None
  
    all_versions_link = result.get("inline_links", {}).get("versions", {}).get("link", {})
    all_versions_id = result.get("inline_links", {}).get("versions", {}).get("cluster_id", {})
```

- `try/except` блоки были использованы для обработки `None` значений когда они отсутствуют из Google бэкенда.

Если объединить все в один `try` блок, извлеченные данные могут быть неаккуратны, иными словами если ссылка или описание на самом деле есть в выдаче, вместо этого оно вернёт `None`, поэтому здесь много `try/except` блоков.

Добавляем извлеченные данные во временный `list()` список:

```python
organic_results_data = []

# тут парсинг и while цикл... 

organic_results_data.append({
    "page_number": results["serpapi_pagination"]["current"],
    "position": position + 1,
    "result_type": result_type,
    "title": title,
    "link": link,
    "result_id": result_id,
    "publication_info_summary": publication_info_summary,
    "snippet": snippet,
    "cited_by_count": cited_by_count,
    "cited_by_link": cited_by_link,
    "cited_by_id": cited_by_id,
    "total_versions": total_versions,
    "all_versions_link": all_versions_link,
    "all_versions_id": all_versions_id,
    "file_format": file_format,
    "file_title": file_title,
    "file_link": file_link,
})
```

Возвращаем временный `list()` список с данными которые будут использоваться позже при парсинге Цитируемых результатов:

```python
return organic_results_data
```

___

![google_scholar_cite_05_1](https://user-images.githubusercontent.com/78694043/146953960-dc9ad8a5-4715-4627-864e-790a33b82157.jpg)

<h2 id="cite_results">Цитируемые результаты</h2>

В этой секции мы используем возвращенные данные из органической выдачи и передадим `result_id` в поисковый запрос для того чтобы спарсить цитируемые результаты. В целом нам нужен список `list()` `result_ids` который будет передан в поисковый запрос `"q"`.

Если у вас уже есть `result_ids`, вы можете пропустить парсинг Органических результатов:

```python
# если у вас есть список result_ids

result_ids = ["FDc6HiktlqEJ"..."FDc6Hikt21J"]
for citation in result_ids:
    params = {
        "api_key": "API_KEY",             # ключ для аутентификации в SerpApi
        "engine": "google_scholar_cite",  # движок для парсинга цитируемых результатов
        "q": citation                     # FDc6HiktlqEJ ... FDc6Hikt21J
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    # дальнейший код парсинга..
```

Ниже примера кода парсинга Цитируемых результатов вы так же найдете пошаговое объяснение того что в нём происходит.

```python
import os
from serpapi import GoogleSearch
from google_scholar_organic_results import organic_results

def cite_results():

    print("extracting cite results..")

    citation_results = []

    for citation in organic_results():
        params = {
            "api_key": os.getenv("API_KEY"), # ключ для аутентификации в SerpApi
            "engine": "google_scholar_cite", # # движок для парсинга цитируемых результатов
            "q": citation["result_id"]       # # FDc6HiktlqEJ ... FDc6Hikt21J
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        print(f"Currently extracting {citation['result_id']} citation ID.")

        for result in results["citations"]:
            cite_title = result["title"]
            cite_snippet = result["snippet"]

            citation_results.append({
                "organic_result_title": citation["title"],
                "organic_result_link": citation["link"],
                "citation_title": cite_title,
                "citation_snippet": cite_snippet
            })

    return citation_results
```

### Объяснение парсинга цитируемых результатов

Создаём временный список `list()` для хранения извлеченных данных:

```python
citation_results = []
```

Создаём `for` цикл для итерации по `organic_results()` результатам и передаем `result_id` в `"q"` поисковый запрос:

```python
for citation in organic_results():
    params = {
      "api_key": os.getenv("API_KEY"), # ключ для аутентификации в SerpApi
      "engine": "google_scholar_cite", # # движок для парсинга цитируемых результатов
      "q": citation["result_id"]       # # FDc6HiktlqEJ ... FDc6Hikt21J
    }

    search = GoogleSearch(params)      # парсинг на бэкенде SerpApi
    results = search.get_dict()        # JSON конвертируется в словарь
```

Создаём второй `for` цикл и достукиваемся до данный таким же способом как и до словаря:

```python
for result in results["citations"]:
    cite_title = result["title"]
    cite_snippet = result["snippet"]
```

Добавляем извелченные данные во временный список `list()` как словарь:

```python
citation_results.append({
    "organic_result_title": citation["title"], # чтобы понимать откуда берутся Цитируемые результаты
    "organic_result_link": citation["link"],   # чтобы понимать откуда берутся Цитируемые результаты
    "citation_title": cite_title,
    "citation_snippet": cite_snippet
})
```

Возвращаем временный список `list()`:

```python
return citation_results
```
___


![google_scholar_save_csv_03_1](https://user-images.githubusercontent.com/78694043/146734776-e4b3c29e-a1d8-447c-a980-36b0ac698392.png)

<h2 id="save_csv">Сохраняем в CSV</h2>

Нам только нужно передать возвращенные данные из Органических и Цитируемых результатов в `DataFrame` `data` аргумент и сохранить `to_csv()`.

```python
import pandas as pd
from google_scholar_organic_results import organic_results
from google_scholar_cite_results import cite_results

print("waiting for organic results to save..")
pd.DataFrame(data=organic_results())
  .to_csv("google_scholar_organic_results.csv", encoding="utf-8", index=False)

print("waiting for cite results to save..")
pd.DataFrame(data=cite_results())
  .to_csv("google_scholar_citation_results.csv", encoding="utf-8", index=False)
```

### Объяснение процесса сохранения в CSV

Импортируем `organic_results()` и `cite_results()` откуда возвращаются данные, и библиотеку `pandas`:

```python
import pandas as pd
from google_scholar_organic_results import organic_results
from google_scholar_cite_results import cite_results
```

Сохраняем органические результаты `to_csv()`:

```python
pd.DataFrame(data=organic_results()) \
    .to_csv("google_scholar_organic_results.csv", encoding="utf-8", index=False)
```

Сохраняем цитируемые результаты `to_csv()`:

```python
pd.DataFrame(data=cite_results()) \
    .to_csv("google_scholar_citation_results.csv", encoding="utf-8", index=False)
```

- `data` аргумент внутри `DataFrame` это извлеченные данные.
- `encoding='utf-8'` аргумент просто для того чтобы все было корректно сохранено. Я использовал этот аргумент явно, несмотря на то что это его дефолтное значение.
- [`index=False`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.index.html) аргумент чтобы убрать дефолтные номера строк `pandas`.

___

![google_scholar_save_sql_05](https://user-images.githubusercontent.com/78694043/147768828-9e383c06-05c2-4a80-bace-a6c85d5dacf5.jpg)

<h2 id="save_sqlite">Сохраняем в SQLite</h2>

После этой секции вы узнаете о том как:
- сохранять данные в SQLite используя `pandas`,
- функционирует SQLite,
- подключаться и разрывать соединение с SQLite,
- создавать и удалять таблицы/колонки,
- добавлять данные в `for` цикле.


Пример того [как функционирует SQLite](https://stackoverflow.com/a/19187244/15164646):

```
1. открывается соединение
    2. транзакция начинается
        3. выполняется инструкция
    4. транзакция завершается
5. закрывается соединение
```

### Сохранение данные в SQLite используя `pandas`

```python
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
import sqlite3
import pandas as pd
from google_scholar_organic_results import organic_results
from google_scholar_cite_results import cite_results

conn = sqlite3.connect("google_scholar_results.db")

# создаём таблицу и колонки для органических результатов
conn.execute("""CREATE TABLE google_scholar_organic_results (
                page_number integer,
                position integer,
                result_type text,
                title text, 
                link text,
                snippet text,
                result_id text,
                publication_info_summary text,
                cited_by_count integer,
                cited_by_link text,
                cited_by_id text,
                total_versions integer,
                all_versions_link text,
                all_versions_id text,
                file_format text,
                file_title text,
                file_link text)""")
conn.commit()

# создаём таблицу и колонки для цитируемых результатов
conn.execute("""CREATE TABLE google_scholar_cite_results (
                organic_results_title text, 
                organic_results_link text,
                citation_title text,
                citation_link text)""")
conn.commit()

# сохраняет цитируемые результаты в SQLite
pd.DataFrame(organic_results()).to_sql(name="google_scholar_organic_results", 
                                       con=conn, 
                                       if_exists="append", 
                                       index=False)

# сохраняет цитируемые результаты в SQLite
pd.DataFrame(cite_results()).to_sql(name="google_scholar_cite_results", 
                                    con=conn, 
                                    if_exists="append", 
                                    index=False)

conn.commit()
conn.close()
```

- `name` это название SQL таблицы.
- `con` это соединение с базой данных.
- `if_exists` скажет `pandas` как себя вести если таблица уже существует. По умолчанию оно не сработает `"fail"` и вызовет `raise` ошибку `ValueError`. В данном случае `pandas` будет добавлять данные.
- `index=False` чтобы убрать индекс столбцов от `DataFrame`.

____

### Другой способ сохранения данных вручную используя запросы SQLite

```python
import sqlite3

conn = sqlite3.connect("google_scholar_results.db")

conn.execute("""CREATE TABLE google_scholar_organic_results (
                page_number integer,
                position integer,
                result_type text,
                title text, 
                link text,
                snippet text,
                result_id text,
                publication_info_summary text,
                cited_by_count integer,
                cited_by_link text,
                cited_by_id text,
                total_versions integer,
                all_versions_link text,
                all_versions_id text,
                file_format text,
                file_title text,
                file_link text)""")
conn.commit()
            
 conn.execute("""CREATE TABLE google_scholar_cite_results (
                organic_results_title text, 
                organic_results_link text,
                citation_title text,
                citation_link text)""")
conn.commit()

# сохраняем Органические результаты
for item in organic_results():
    conn.execute("""INSERT INTO google_scholar_organic_results
                    VALUES (:page_number,
                            :position,
                            :result_type,
                            :title,
                            :link,
                            :snippet,
                            :result_id,
                            :publication_info_summary,
                            :cited_by_count,
                            :cited_by_link,
                            :cited_by_id,
                            :total_versions,
                            :all_versions_link,
                            :all_versions_id,
                            :file_format,
                            :file_title,
                            :file_link)""",
                     {"page_number": item["page_number"],
                      "position": item["position"],
                      "result_type": item["type"],
                      "title": item["title"],
                      "link": item["link"],
                      "snippet": item["snippet"],
                      "result_id": item["result_id"],
                      "publication_info_summary": item["publication_info_summary"],
                      "cited_by_count": item["cited_by_count"],
                      "cited_by_link": item["cited_by_link"],
                      "cited_by_id": item["cited_by_id"],
                      "total_versions": item["total_versions"],
                      "all_versions_link": item["all_versions_link"],
                      "all_versions_id": item["all_versions_id"],
                      "file_format": item["file_format"],
                      "file_title": item["file_title"],
                      "file_link": item["file_link"]})
conn.commit()

# сохраняем Цитируемые результаты
for cite_result in cite_results():
    conn.execute("""INSERT INTO google_scholar_cite_results 
                    VALUES (:organic_result_title,
                    :organic_result_link,
                    :citation_title,
                    :citation_snippet)""",
                 {"organic_result_title": cite_result["organic_result_title"],
                  "organic_result_link": cite_result["organic_result_link"],
                  "citation_title": cite_result["citation_title"],
                  "citation_snippet": cite_result["citation_snippet"]})

conn.commit()
conn.close() # явно лучше, чем неявно
```

#### Объяснение сохранения извлеченных данных вручную прописывая запросы SQLite 

Импортируем `sqlite3` библиотеку:

```python
# встроенная библиотека
import sqlite3 
```

Соединяемся с существующей базе данных или даём новое имя и библиотека создаст базу данных:

```python
conn = sqlite3.connect("google_scholar_results.db")
```

Создаём таблицу Органические результаты и применяем изменения:

```python
conn.execute("""CREATE TABLE google_scholar_organic_results (
                page_number integer,
                position integer,
                result_type text,
                title text, 
                link text,
                snippet text,
                result_id text,
                publication_info_summary text,
                cited_by_count integer,
                cited_by_link text,
                cited_by_id text,
                total_versions integer,
                all_versions_link text,
                all_versions_id text,
                file_format text,
                file_title text,
                file_link text)""")
conn.commit()
```

Создаём таблицу Цитируемые результаты и применяем изменения:

```python
conn.execute("""CREATE TABLE google_scholar_cite_results (
            organic_results_title text, 
            organic_results_link text,
            citation_title text,
            citation_link text)""")
conn.commit()
```

Добавляем извлеченные Органические результаты в таблицу используя `for` цикл:

```python
for item in organic_results():
    conn.execute("""INSERT INTO google_scholar_organic_results
                    VALUES (:page_number,
                            :position,
                            :result_type,
                            :title,
                            :link,
                            :snippet,
                            :result_id,
                            :publication_info_summary,
                            :cited_by_count,
                            :cited_by_link,
                            :cited_by_id,
                            :total_versions,
                            :all_versions_link,
                            :all_versions_id,
                            :file_format,
                            :file_title,
                            :file_link)""",
                     {"page_number": item["page_number"],
                      "position": item["position"],
                      "result_type": item["type"],
                      "title": item["title"],
                      "link": item["link"],
                      "snippet": item["snippet"],
                      "result_id": item["result_id"],
                      "publication_info_summary": item["publication_info_summary"],
                      "cited_by_count": item["cited_by_count"],
                      "cited_by_link": item["cited_by_link"],
                      "cited_by_id": item["cited_by_id"],
                      "total_versions": item["total_versions"],
                      "all_versions_link": item["all_versions_link"],
                      "all_versions_id": item["all_versions_id"],
                      "file_format": item["file_format"],
                      "file_title": item["file_title"],
                      "file_link": item["file_link"]})
conn.commit()
```


Добавляем извлеченные Цитируемые результаты в таблицу используя `for` цикл:

```python
for cite_result in cite_results():
    conn.execute("""INSERT INTO google_scholar_cite_results 
                    VALUES (:organic_result_title,
                    :organic_result_link,
                    :citation_title,
                    :citation_snippet)""",
                 {"organic_result_title": cite_result["organic_result_title"],
                  "organic_result_link": cite_result["organic_result_link"],
                  "citation_title": cite_result["citation_title"],
                  "citation_snippet": cite_result["citation_snippet"]})
conn.commit()
```


Закрываем cоединение с базой данных:

```python
conn.close()
```

Дополнительные полезные команды:

```python
# удалить все данные из таблицы
conn.execute("DELETE FROM google_scholar_organic_results")

# удалить таблицу
conn.execute("DROP TABLE google_scholar_organic_results")

# удалить колонку
conn.execute("ALTER TABLE google_scholar_organic_results DROP COLUMN authors")

# добавить колнку
conn.execute("ALTER TABLE google_scholar_organic_results ADD COLUMN snippet text")
```

___

<h2 id="full_code">Код целиком - парсинг</h2>

```python
import os
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl


def organic_results():
    print("extracting organic results..")

    params = {
        "api_key": os.getenv("API_KEY"),
        "engine": "google_scholar",
        "q": "minecraft redstone system structure characteristics strength",  # поисковый запрос
        "hl": "en",        # язык
        "as_ylo": "2017",  # от 2017
        "as_yhi": "2021",  # до 2021
        "start": "0"
    }

    search = GoogleSearch(params)

    organic_results_data = []

    loop_is_true = True

    while loop_is_true:
        results = search.get_dict()

        print(f"Currently extracting page №{results['serpapi_pagination']['current']}..")

        for result in results["organic_results"]:
            position = result["position"]
            title = result["title"]
            publication_info_summary = result["publication_info"]["summary"]
            result_id = result["result_id"]
            link = result.get("link")
            result_type = result.get("type")
            snippet = result.get("snippet")
    
            try:
              file_title = result["resources"][0]["title"]
            except: file_title = None
    
            try:
              file_link = result["resources"][0]["link"]
            except: file_link = None
    
            try:
              file_format = result["resources"][0]["file_format"]
            except: file_format = None
    
            try:
              cited_by_count = int(result["inline_links"]["cited_by"]["total"])
            except: cited_by_count = None
    
            cited_by_id = result.get("inline_links", {}).get("cited_by", {}).get("cites_id", {})
            cited_by_link = result.get("inline_links", {}).get("cited_by", {}).get("link", {})
    
            try:
              total_versions = int(result["inline_links"]["versions"]["total"])
            except: total_versions = None
    
            all_versions_link = result.get("inline_links", {}).get("versions", {}).get("link", {})
            all_versions_id = result.get("inline_links", {}).get("versions", {}).get("cluster_id", {})
    
            organic_results_data.append({
              "page_number": results["serpapi_pagination"]["current"],
              "position": position + 1,
              "result_type": result_type,
              "title": title,
              "link": link,
              "result_id": result_id,
              "publication_info_summary": publication_info_summary,
              "snippet": snippet,
              "cited_by_count": cited_by_count,
              "cited_by_link": cited_by_link,
              "cited_by_id": cited_by_id,
              "total_versions": total_versions,
              "all_versions_link": all_versions_link,
              "all_versions_id": all_versions_id,
              "file_format": file_format,
              "file_title": file_title,
              "file_link": file_link,
            })

            if "next" in results["serpapi_pagination"]:
                search.params_dict.update(dict(parse_qsl(urlsplit(results["serpapi_pagination"]["next"]).query)))
            else:
                loop_is_true = False

    return organic_results_data
    
    
def cite_results():

    print("extracting cite results..")

    citation_results = []

    for citation in organic_results():
        params = {
            "api_key": os.getenv("API_KEY"),
            "engine": "google_scholar_cite",
            "q": citation["result_id"]
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        print(f"Currently extracting {citation['result_id']} citation ID.")

        for result in results["citations"]:
            cite_title = result["title"]
            cite_snippet = result["snippet"]

            citation_results.append({
                "organic_result_title": citation["title"],
                "organic_result_link": citation["link"],
                "citation_title": cite_title,
                "citation_snippet": cite_snippet
            })

    return citation_results



# пример вывода при парсинге органических результатов и сохранение в SQL:
'''
extracting organic results..
Currently extracting page №1..
Currently extracting page №2..
Currently extracting page №3..
Currently extracting page №4..
Currently extracting page №5..
Currently extracting page №6..
Done extracting organic results.
Saved to SQL Lite database.
'''
```

<h2 id="saving_code">Код целиком - сохранение</h2>

```python
import pandas as pd
import sqlite3
from google_scholar_organic_results import organic_results
from google_scholar_cite_results import cite_results

# Один из способов сохранить данные в БД используя Pandas
print("waiting for organic results to save..")
organic_df = pd.DataFrame(data=organic_results())
organic_df.to_csv("google_scholar_organic_results.csv", encoding="utf-8", index=False)

print("waiting for cite results to save..")
cite_df = pd.DataFrame(data=cite_results())
cite_df.to_csv("google_scholar_citation_results.csv", encoding="utf-8", index=False)

# ------------------------------

# Другой способ сохранить данные в БФ в ручную прописывая SQLite запросы
conn = sqlite3.connect("google_scholar_results.db")

conn.execute("""CREATE TABLE google_scholar_organic_results (
                page_number integer,
                position integer,
                result_type text,
                title text,
                link text,
                snippet text,
                result_id text,
                publication_info_summary text,
                cited_by_count integer,
                cited_by_link text,
                cited_by_id text,
                total_versions integer,
                all_versions_link text,
                all_versions_id text,
                file_format text,
                file_title text,
                file_link text)""")
conn.commit()


conn.execute("""CREATE TABLE google_scholar_cite_results (
            organic_results_title text,
            organic_results_link text,
            citation_title text,
            citation_link text)""")
conn.commit()

for item in organic_results():
    conn.execute("""INSERT INTO google_scholar_organic_results
                    VALUES (:page_number,
                            :position,
                            :result_type,
                            :title,
                            :link,
                            :snippet,
                            :result_id,
                            :publication_info_summary,
                            :cited_by_count,
                            :cited_by_link,
                            :cited_by_id,
                            :total_versions,
                            :all_versions_link,
                            :all_versions_id,
                            :file_format,
                            :file_title,
                            :file_link)""",
                 {"page_number": item["page_number"],
                  "position": item["position"],
                  "result_type": item["type"],
                  "title": item["title"],
                  "link": item["link"],
                  "snippet": item["snippet"],
                  "result_id": item["result_id"],
                  "publication_info_summary": item["publication_info_summary"],
                  "cited_by_count": item["cited_by_count"],
                  "cited_by_link": item["cited_by_link"],
                  "cited_by_id": item["cited_by_id"],
                  "total_versions": item["total_versions"],
                  "all_versions_link": item["all_versions_link"],
                  "all_versions_id": item["all_versions_id"],
                  "file_format": item["file_format"],
                  "file_title": item["file_title"],
                  "file_link": item["file_link"]})
conn.commit()


for cite_result in cite_results():
    conn.execute("""INSERT INTO google_scholar_cite_results
                    VALUES (:organic_result_title,
                    :organic_result_link,
                    :citation_title,
                    :citation_snippet)""",
                 {"organic_result_title": cite_result["organic_result_title"],
                  "organic_result_link": cite_result["organic_result_link"],
                  "citation_title": cite_result["citation_title"],
                  "citation_snippet": cite_result["citation_snippet"]})

conn.commit()
conn.close()
print("Saved to SQL Lite database.")


# пример вывода:
'''
extracting organic results..
Currently extracting page №1..
...
Currently extracting page №4..
extracting cite results..
extracting organic results..
Currently extracting page №1..
...
Currently extracting page №4..
Currently extracting 60l4wsP6Ps0J citation ID.
Currently extracting 9hkhIFu_BhAJ citation ID.
...
Saved to SQL Lite database.
'''
```

___

<h2 id="links">Ссылки</h2>

- [GitHub репозиторий](https://github.com/dimitryzub/py-google-scholar-organic-cite-to-csv-sqlite)
- [Код с парсингом, сохранением в CSV в онлайн IDE](https://replit.com/@serpapi/Scrape-historic-Google-Scholar-Organic-and-Citation-results#main.py)
- [Google Scholar API](https://serpapi.com/google-scholar-api)
- [SerpApi библиотеки](https://serpapi.com/libraries)

___

<h2 id="outro">Что дальше</h2>

С этими данными должно быть возможно сделать какое-нибудь исследование, или визуализацию по определенной дисциплине. Классным дополнением к этому скрипту будет добавить возможность запускать его каждую неделю или месяц для парсинга дополнительных данных.

Следующий блог пост будет о парсинге Профилей с пагинацией, а так же Авторских результатов.

Если вы хотите парсить данные без необходимости писать парсер с нуля, разбираться как обойти блокировки от поисковых систем, как увеличить объем запросов, или, как парсить данные с JavaScript - [попробуйте SerpApi](https://serpapi.com/) или [свяжитесь с SerpApi](https://serpapi.com/#contact).


___

<p style="text-align: center;">Присоединяйтесь к нам на <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Добавить <a href="https://forum.serpapi.com/feature-requests">запрос на фичу</a>💫 или <a href="https://forum.serpapi.com/bugs">существующий баг</a>🐞</p>