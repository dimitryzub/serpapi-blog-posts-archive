👉**Кратко о сути**: обучающий блог пост о парсинге: позиция сайта, заголовок, ссылка, отображаемая ссылка, описание и иконка из поисковой выдачи qwant.com используя Python.

🔨**Что понадобится**: понимание циклов, структур данных, обработка исключений, и, базовое понимание `CSS` селекторов. А так же `bs4`, `requests`, `lxml` библиотеки.

⏱️**Сколько времени займет**: ~15-30 минут.

___

- <a href="#intro">Что такое Qwant Search</a>
- <a href="#what_will_be_scraped">Что парсим</a>
- <a href="#prerequisites">Что необходимо для старта</a>
- <a href="#process">Процесс</a>
  - <a href="#organic_results">Органические результаты</a>
  - <a href="#advertisement_results">Рекламные результаты</a>
- <a href="#code">Код целиком</a>
- <a href="#links">Ссылки</a>
- <a href="#outro">Заключение</a>

___

<h2 id="intro">Что такое Qwant Search</h2>

[Qwant](https://www.qwant.com/) это базирующаяся в Париже европейская поисковая система с независимой системой индексирования которая не отслеживает действия пользователей для использования этих данных в рекламных целях. Qwant доступна на 26 языках и имеющая более [30 миллионов индивидуальных пользователей в месяц по всему миру](https://www.similarweb.com/website/qwant.com/).

___

<h2 id="what_will_be_scraped">Что парсим</h2>

![qwant_organic_results_02](https://user-images.githubusercontent.com/78694043/146533506-32bdec38-78d1-4f2f-bb70-c1c3f40ca5a0.png)

<h2 id="prerequisites">Что необходимо для старта</h2>

**Базовое понимание `CSS` селекторов**

`CSS` селекторы объявляют к какой части разметки применяется тот или иной стиль, что позволяет извлекать данные из совпадающих тегов и атрибутов.

Если вы не парсили с помощью `CSS` селекторов, есть блог пост посвященный этому на английском языке - [how to use `CSS` selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) который рассказывает о том что это такое, их плюсы и минусы и для чего они вообще с точки зрения веб скрейпинга.

**Отдельное вирутуальное окружение**

Вкратце, это штука, которая создает независимый набор установленных библиотек включая возможность установки разных версий Python которые могут сосуществовать друг с другом одновременно на одной системе, что в свою очередь предотвращает конфликты библиотек и разных версий Python.

Если вы не имели дело с виртуальным окружением ранее, взгляните на посвященный этому блог пост на английском языке - [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/).


**Установка библиотек**:

```lang-none
pip install requests
pip install lxml 
pip install beautifulsoup4
```

**Предотвращение блокировок**

Есть вероятность, что запрос может быть заблокирован по тем или иным причинам. Можете взглянуть на одиннадцать вариантов предотвращения блокировок с большинства сайтами в моём отдельном блог посте на английском языке - [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/).

___

<h2 id="process">Процесс</h2>

Если объяснение не нужно:
- забирайте код в секции <a href="#code">весь код целиком</a>,
- [попробуйте сразу в online IDE](https://replit.com/@DimitryZub1/Scrape-Qwant-Organic-and-Ad-Results#main.py).

**Начальный код** для органической и рекламной выдачи:


```python
from bs4 import BeautifulSoup
import requests, lxml, json, logging

headers = {
  "User-Agent": "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}

params = {
  "q": "minecraft",
  "t": "web"
}

html = requests.get("https://www.qwant.com/", params=params, headers=headers, timeout=20)
soup = BeautifulSoup(html.text, "lxml")
# ...
```

### Объяснение кода

**Импортируем библиотеки**:

```python
from bs4 import BeautifulSoup
import requests, lxml, json
```

**Добавляем [`user-agent`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) и [query параметры](https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls)** к запросу:

```python
headers = {
  "User-Agent": "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}

params = {
  "q": "minecraft",  # поисковый запрос
  "t": "web"         # qwant параметр для отображения веб результатов 
}
```

**Отправляем запрос**, [добавляем `timeout` аргумент](https://docs.python-requests.org/en/master/user/quickstart/#timeouts), создаем `BeautifulSoup()` объект:

```python
html = requests.get("https://www.qwant.com/", params=params, headers=headers, timeout=20)
soup = BeautifulSoup(html.text, "lxml")
```

- `timeout` параметр скажет `requests` остановиться ожидать ответ на запрос после X числа секунд.
- `BeautifulSoup()` это то что парсит HTML. `lxml` это HTML парсер.

<h2 id="organic_results">Парсинг органических результатов</h2>

```python
def scrape_organic_results():

  organic_results_data = []

  for index, result in enumerate(soup.select("[data-testid=webResult]"), start=1):
    title = result.select_one(".WebResult-module__title___MOBFg").text
    link = result.select_one(".Stack-module__VerticalStack___2NDle.Stack-module__Spacexxs___3wU9G a")["href"]
    snippet = result.select_one(".Box-module__marginTopxxs___RMB_d").text

    try:
      displayed_link = result.select_one(".WebResult-module__permalink___MJGeh").text
      favicon = result.select_one(".WebResult-module__iconBox___3DAv5 img")["src"]
    except:
      displayed_link = None
      favicon = None

    organic_results_data.append({
      "position": index,
      "title": title,
      "link": link,
      "displayed_link": displayed_link,
      "snippet": snippet,
      "favicon": favicon
    })

  print(json.dumps(organic_results_data, indent=2))


scrape_organic_results()
```

**Создаем временный список `list()`** где будут храниться извлеченные данные:

```python
organic_results_data = []
```

**Итерируем в цикле и парсим** данные:

```python
for index, result in enumerate(soup.select("[data-testid=webResult]"), start=1):
  title = result.select_one(".WebResult-module__title___MOBFg").text
  link = result.select_one(".Stack-module__VerticalStack___2NDle.Stack-module__Spacexxs___3wU9G a")["href"]
  snippet = result.select_one(".Box-module__marginTopxxs___RMB_d").text

  try:
    displayed_link = result.select_one(".WebResult-module__permalink___MJGeh").text
    favicon = result.select_one(".WebResult-module__iconBox___3DAv5 img")["src"]
  except:
    displayed_link = None
    favicon = None
```

Чтобы извлечь позицию сайта, мы можем использовать [`enumerate()` функцию которая добавляет счетчик к итерируемому объекту и возвращает его](https://www.programiz.com/python-programming/methods/built-in/enumerate) и установить `start` аргумент равным 1, для того чтобы начать отсчёт с единицы (1), а не с нуля (0).

Чтобы обработать `None` значения, мы можем использовать блок `try/except`, то есть если из самой выдачи Qwant ничего не будет, мы установим ту или иную переменную на `None` соответственно, в ином случае вылетит ошибка которая, скажет что нет того или иного элемента, или атрибута в HTML дереве.


**Добавляем извлеченные данные** во временный список `list()` как словарь `dict()`:

```python
organic_results_data.append({
  "position": index,
  "title": title,
  "link": link,
  "displayed_link": displayed_link,
  "snippet": snippet,
  "favicon": favicon
})
```

**Вывод**:

```python
print(json.dumps(organic_results_data, indent=2))


# часть вывода:
'''
[
  {
    "position": 1,
    "title": "Minecraft Official Site | Minecraft",
    "link": "https://www.minecraft.net/",
    "displayed_link": "minecraft.net",
    "snippet": "Get all-new items in the Minecraft Master Chief Mash-Up DLC on 12/10, and the Superintendent shirt in Character Creator, free for a limited time! Learn more. Climb high and dig deep. Explore bigger mountains, caves, and biomes along with an increased world height and updated terrain generation in the Caves & Cliffs Update: Part II! Learn more . Play Minecraft games with Game Pass. Get your ...",
    "favicon": "https://s.qwant.com/fav/m/i/www_minecraft_net.ico"
  },
  
  ... другие результаты
  
  {
    "position": 10,
    "title": "Minecraft - download free full version game for PC ...",
    "link": "http://freegamepick.net/en/minecraft/",
    "displayed_link": "freegamepick.net",
    "snippet": "Minecraft Download Game Overview. Minecraft is a game about breaking and placing blocks. It's developed by Mojang. At first, people built structures to protect against nocturnal monsters, but as the game grew players worked together to create wonderful, imaginative things. It can als o be about adventuring with friends or watching the sun rise over a blocky ocean.",
    "favicon": "https://s.qwant.com/fav/f/r/freegamepick_net.ico"
  }
]
'''
```

___

<h2 id="advertisement_results">Парсинг рекламных результатов</h2>

```python
def scrape_ad_results():

  ad_results_data = []

  for index, ad_result in enumerate(soup.select("[data-testid=adResult]"), start=1):
    ad_title = ad_result.select_one(".WebResult-module__title___MOBFg").text
    ad_link = ad_result.select_one(".Stack-module__VerticalStack___2NDle a")["href"]
    ad_displayed_link = ad_result.select_one(".WebResult-module__domain___1LJmo").text
    ad_snippet = ad_result.select_one(".Box-module__marginTopxxs___RMB_d").text
    ad_favicon = ad_result.select_one(".WebResult-module__iconBox___3DAv5 img")["src"]

    ad_results_data.append({
      "ad_position": index,
      "ad_title": ad_title,
      "ad_link": ad_link,
      "ad_displayed_link": ad_displayed_link,
      "ad_snippet": ad_snippet,
      "ad_favicon": ad_favicon
    })

  print(json.dumps(ad_results_data, indent=2))


scrape_ad_results()
```

**Создаём временный список `list()`** для хранения извлеченных данных:
```python
ad_results_data = []
```

**Итерируем и извлекаем**:

```python
for index, ad_result in enumerate(soup.select("[data-testid=adResult]"), start=1):
  ad_title = ad_result.select_one(".WebResult-module__title___MOBFg").text
  ad_link = ad_result.select_one(".Stack-module__VerticalStack___2NDle a")["href"]
  ad_displayed_link = ad_result.select_one(".WebResult-module__domain___1LJmo").text
  ad_snippet = ad_result.select_one(".Box-module__marginTopxxs___RMB_d").text
  ad_favicon = ad_result.select_one(".WebResult-module__iconBox___3DAv5 img")["src"]
```

Такой же подход используется для извлечения позиции сайта. Единственное отличие в другом `CSS` "контейнер" селекторе `[data-testid=adResult]`, когда в органической выдаче это другой селектор `[data-testid=webResult]`. Все остальное осталось прежним.

**Добавляем извлеченные данные во временный список `list()`** как словарь:

```python
ad_results_data.append({
  "ad_position": index,
  "ad_title": ad_title,
  "ad_link": ad_link,
  "ad_displayed_link": ad_displayed_link,
  "ad_snippet": ad_snippet
})
```

**Вывод**:

```python
print(json.dumps(ad_results_data, indent=2))

# в данном случае один рекламный результат:
'''
[
  {
    "ad_position": 1,
    "ad_title": "Watch Movies & TV on Amazon - Download in HD on Amazon Video",
    "ad_link": "https://www.bing.com/aclick?ld=e8pyYjhclU87kOyQ4ap78CRzVUCUxgK0MGMfKx1YlQe_w7Nbzamra9cSRmPFAtSOVF4MliAqbJNdotR3G-aqHSaMOI0tqV9K0EAFRTemYDKhbqLyjFW93Lsh0mnyySb8oIj6GXADnoePUk-etFDgSvPdZI0xObBo4hesqbOHypYhSGeJ-ZbG1eY0kijv95k0XJ9WKPPA&u=aHR0cHMlM2ElMmYlMmZ3d3cuYW1hem9uLmNvLnVrJTJmcyUyZiUzZmllJTNkVVRGOCUyNmtleXdvcmRzJTNkbWluZWNyYWZ0JTJidGhlJTI2aW5kZXglM2RhcHMlMjZ0YWclM2RoeWRydWtzcG0tMjElMjZyZWYlM2RwZF9zbF8ydmdscmFubWxwX2UlMjZhZGdycGlkJTNkMTE0NDU5MjQzNjk0ODQzOSUyNmh2YWRpZCUzZDcxNTM3MTUwMzgzNDA4JTI2aHZuZXR3JTNkcyUyNmh2cW10JTNkZSUyNmh2Ym10JTNkYmUlMjZodmRldiUzZG0lMjZodmxvY2ludCUzZCUyNmh2bG9jcGh5JTNkMTQxMTcxJTI2aHZ0YXJnaWQlM2Rrd2QtNzE1Mzc2Njc4MjI5NzklM2Fsb2MtMjM1JTI2aHlkYWRjciUzZDU5MTJfMTg4MTc4NQ&rlid=c61aa73b62e916116cbdc687c021190a",
    "ad_displayed_link": "amazon.co.uk",
    "ad_snippet": "Download now. Watch anytime on Amazon Video.",
    "ad_favicon": "https://s.qwant.com/fav/a/m/www_amazon_co_uk.ico"
  }
]
'''
```


___

<h2 id="code">Код целиком</h2>

```python
from bs4 import BeautifulSoup
import requests, lxml, json

headers = {
  "User-Agent": "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}

params = {
  "q": "minecraft",
  "t": "web"
}

html = requests.get("https://www.qwant.com/", params=params, headers=headers, timeout=20)
soup = BeautifulSoup(html.text, "lxml")


def scrape_organic_results():

  organic_results_data = []

  for index, result in enumerate(soup.select("[data-testid=webResult]"), start=1):
    title = result.select_one(".WebResult-module__title___MOBFg").text
    link = result.select_one(".Stack-module__VerticalStack___2NDle.Stack-module__Spacexxs___3wU9G a")["href"]
    snippet = result.select_one(".Box-module__marginTopxxs___RMB_d").text

    try:
      displayed_link = result.select_one(".WebResult-module__permalink___MJGeh").text
      favicon = result.select_one(".WebResult-module__iconBox___3DAv5 img")["src"]
    except:
      displayed_link = None
      favicon = None

    organic_results_data.append({
      "position": index,
      "title": title,
      "link": link,
      "displayed_link": displayed_link,
      "snippet": snippet,
      "favicon": favicon
    })

  print(json.dumps(organic_results_data, indent=2))


def scrape_ad_results():

  ad_results_data = []

  for index, ad_result in enumerate(soup.select("[data-testid=adResult]"), start=1):
    ad_title = ad_result.select_one(".WebResult-module__title___MOBFg").text
    ad_link = ad_result.select_one(".Stack-module__VerticalStack___2NDle a")["href"]
    ad_displayed_link = ad_result.select_one(".WebResult-module__domain___1LJmo").text
    ad_snippet = ad_result.select_one(".Box-module__marginTopxxs___RMB_d").text
    ad_favicon = ad_result.select_one(".WebResult-module__iconBox___3DAv5 img")["src"]

    ad_results_data.append({
      "ad_position": index,
      "ad_title": ad_title,
      "ad_link": ad_link,
      "ad_displayed_link": ad_displayed_link,
      "ad_snippet": ad_snippet,
      "ad_favicon": ad_favicon
    })

  print(json.dumps(ad_results_data, indent=2))
```

___

<h2 id="links">Ссылки</h2>

- [Код в онлайн IDE](https://replit.com/@DimitryZub1/Scrape-Qwant-Organic-and-Ad-Results#main.py)

___

<h2 id="outro">Заключение</h2>

С вопросами и предложениями по блог посту пишите в комментариях или в Твиттер на [@dimitryzub](https://twitter.com/DimitryZub) или [@serp_api](https://twitter.com/serp_api).

___

<p style="text-align: center;">Присоединяйтесь к нам на <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Добавляйте <a href="https://forum.serpapi.com/feature-requests">запрос на фичу</a>💫 или <a href="https://forum.serpapi.com/bugs">существующий баг</a>🐞</p>