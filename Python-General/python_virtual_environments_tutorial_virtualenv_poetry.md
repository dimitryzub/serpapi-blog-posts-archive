- <a href="#intro">Intro</a>
- <a href="#what_venv">What is virtual environment</a>
- <a href="#why_venv">Why to use virtual environment</a>
- <a href="#how_venv">How to use virtual environment</a>
    - <a href="#venv">Virtualenv</a>
    - <a href="#poetry">Poetry</a>
- <a href="#links">Links</a>
- <a href="#acknowledgments">Acknowledgments</a>
- <a href="#сonclusion">Conclusion</a>
- <a href="#outro">Outro</a>

___

<h2 id="intro">Intro</h2>

#### What this blog post is about

This blog post is mostly aimed at people who didn't work with it. Here you will find that this is *not a complete* Python virtual environment reference, it is rather a mini-guided tutorial about:

- **what Python virtual environment is**
- **why bother using it**
- **how to use it**

... with example process of two popular modules: [`virtualenv`](https://docs.python.org/3/library/venv.html) and [`poetry`](https://python-poetry.org/), and software such as IntelliJ IDE via [Python plugin](https://plugins.jetbrains.com/plugin/631-python), PyCharm Community Edition, VSCode, Windows system, and Git Bash terminal.

If you're using JetBrains products you also need to [index installed site-packages from the virtual environment](https://www.jetbrains.com/help/idea/indexing.html).

> Indexing is a core JetBrains features: code completion, inspections, finding usages, navigation, syntax highlighting, refactoring, and more.

___

<h2 id="what_venv">What is virtual environment?</h2>

#### A thing that isolates other things

Python virtual environment is basically a separate folder that [creates an independent set of installed packages](https://docs.python.org/3/library/venv.html), Python binaries in its own directory, that isolates any other installation of Python on your computer.

#### A thing that prevents conflicts

Python virtual environment is used to [prevent interfering with the behavior of other applications](https://docs.python.org/3/glossary.html#term-virtual-environment). Therefore it will prevent packages or Python version conflicts when working with different projects that are running on the same system.

![what is venv_03](https://user-images.githubusercontent.com/78694043/145010258-2ad35301-b0a0-4fd7-b8be-c44a0df28483.png)


<h2 id="why_venv">Why to use virtual environment?</h2>

**To avoid Python version conflicts**

Python virtual environment allows multiple versions of Python to coexist with each other. It will let you work with the old version of Python after installing a newer version all on the same system.

If you try to do it without separated virtual environment things will break pretty quickly:

![illustration by xkcd](https://user-images.githubusercontent.com/78694043/145189874-1686744d-8498-4eb1-a144-2e86e59df7f8.png)
*Python environment - xkcd.com*


**To avoid package version conflicts**

Say you're on two projects, two of them are using [`serpapi` library](https://pypi.org/project/google-search-results/) which is installed globally (system-wide) with a *1.15* version.

*Project_1* depends on the *1.05* version and *Project_2* depends on the *1.08* version. What will happen if each project tries to `import` a `serpapi` library...


### Example without the virtual environment

Since Python doesn’t distinguish between different versions of the same library in the `/site-packages` directory, this leads to the problem when you have two projects that require different versions of the same library and globally installed library have a completely different version.

![why to use venv_1_04](https://user-images.githubusercontent.com/78694043/145010290-2eeabc7a-d22b-4b5b-ad98-5bebc5ae8b46.png)


### Example with the virtual environment

When using a Python virtual environment you can use different versions of the same library or different versions of the Python separated by different virtual environments - folders.

![why to use venv_2_04](https://user-images.githubusercontent.com/78694043/145010310-aadd8463-100e-495a-ad26-61fc7c03b502.png)

📌Note: You can install globally different versions of site-packages and use them but as stated before it would become a mess pretty quickly and could break system tools or other projects.

<h2 id="how_venv">How to use virtual environment?</h2>

Let's look at examples of how to use Python virtual environment from the initial install, creating and activating environment, adding dependencies using `virtualenv` and `poetry` modules, and deactivating virtual environment when done.

![how to use venv_1_07](https://user-images.githubusercontent.com/78694043/145010188-0e11d33a-521f-4684-894b-fc0669820b34.png)


<h2 id="venv">An example process of using Virtualenv</h2>

**Install** `virtualenv`:

```
$ pip install virtualenv
```


**Create** environment folder inside the current package/project directory:

```
$ python -m venv env
```

> - [`-m` stands for `<module-name>`](https://docs.python.org/3/using/cmdline.html#cmdoption-m) (`venv`)
>
> - env is a folder created by `venv` module.

**Activate** environment:

```
# On Windows
source env/Scripts/activate

(env)
```

```
# On Linux
$ source env/bin/activate

(env) $ 
```
> `(env)` indicates that you're in the virtual environment.

**Add site-packages** (third-party libraries) to the activated environment.

Add the latest version:

```
(env) $ pip install google-search-results
```

Add specific version using equals `==` sign:

```
(env) $ pip install 'google-search-results==1.3.0'
```

📌Note: if you're on Windows and using Command Line Prompt, use double quotes `"` when specifying versions:

```
pip install 'google-search-results==1.3.0'
ERROR: Invalid requirement: "'google-search-results==1.3.0'"
```

Add specific version without overwriting lower version(s):

```
(env) $ pip install -I 'google-search-results==1.3.0'
```

> [`-I` argument will ignore already installed packages](https://stackoverflow.com/a/36399566/15164646).


A quick look at how you can install site-package (`virtualenv`) and create a virtual environment for a specific Python version:

```
# For Windows:
# install package for specific Python version (https://bit.ly/3pXtHng)
$ py -3.6 -m pip install virtualenv

# create venv for specific Python version (https://bit.ly/3oQ008v)
$ py -3.6 -m venv my_test_env
```

```
# For Linux:
# install package for specific Python version
$ python3.6 -m pip install virtualenv

# create venv for specific Python version
$ python3.6 -m venv my_test_env
```


**Use and index added site-packages** inside IDE

Refer to <a href="#activate_env"><i>activate and index installed packages</i> section</a> with the illustrated process using `poetry` examples for <a href="#pycharm">PyCharm</a>, <a href="#intellij">IntelliJ</a>, and <a href="#vscode">VSCode</a>.

Everything is almost the same <a href="#poetry_find_path">except you don't need to find a `poetry` cache folder via command line</a> to find a path to `python.exe` file because the `env` folder is already in your project directory that was created earlier *above*.

**Deactivate** virtual environment when done:

```
(env) $ deactivate
$ 
```

___

<h2 id="poetry">An example process of using Poetry</h2>

**Install** `poetry`:

```
$ pip install poetry
```

A quick look at how you can install site-package (`poetry`) for a specific Python version:

```
# For Windows:
$ py -3.6 -m pip install poetry

# For Linux:
$ python3.6 -m pip install poetry
```

**Create** (initialize) `poetry` inside *current* package/project directory:

```
$ poetry init
```

> The `init` command will ‘initialize’ an existing directory and [create a `pyproject.toml` which will manage your project and its dependencies](https://python-poetry.org/docs/pyproject/):
>
> ```
> # pyproject.toml file
> 
>[tool.poetry]
>name = "virtual environments"
>version = "0.1.0"
>description = ""
>authors = ["Dimitry Zub <dimitryzub@gmail.com>"]
>
>[tool.poetry.dependencies]
>python = "^3.9"
>google-search-results = "^2.4.0"
># other site-packages will appear here..
>
>[tool.poetry.dev-dependencies]
># development dependencies will appear here..
>
>[build-system]
>requires = ["poetry-core>=1.0.0"]
>build-backend = "poetry.core.masonry.api"
>```
>
> [What the heck is `pyproject.toml`](https://snarky.ca/what-the-heck-is-pyproject-toml/)?
>
> In short, [`pyproject.toml` is the new unified Python project settings file](https://www.python.org/dev/peps/pep-0518/#specification) that contains build system requirements and information, which are used by [`pip`](https://www.w3schools.com/python/python_pip.asp) to build the package/project, and it is *almost* a replacement for [`setup.py`](https://stackoverflow.com/questions/1471994/what-is-setup-py).

Before `pyproject.toml` creation, [`$ poetry init` will interactively ask you to fill the fields about your package/project](https://python-poetry.org/docs/cli/#init):

>- `--name`: Name of the package/package.
>- `--description`: Description of the package.
>- `--author`: Author of the package.
>- `--python` Compatible Python versions.
>- `--dependency`: Package to require with a version constraint. Should be in format `package:1.0.0`(version).
>- `--dev-dependency`: Development requirements, see `--require`.

**Add** dependencies to your package/project:

```
$ poetry add google-search-results
```

```
...
Creating virtualenv PROJECT-9SrbZw5z-py3.9 in C:\Users\USER\AppData\Local\pypoetry\Cache\virtualenvs

Using version ^2.4.0 for google-search-results

Updating dependencies
Resolving dependencies...

Writing lock file

Package operations: 1 install, 0 updates, 0 removals

  • Installing google-search-results (2.26.0)
```


>- The [`add` command adds dependencies to `pyproject.toml`](https://python-poetry.org/docs/cli/#add) and [`poetry.lock`](https://python-poetry.org/docs/libraries#lock-file), and installs them.
>- `Creating virtualenv` will create a virtual environment with the showed path. Environment creation will be done once.
>- `Writing lock file` will write dependencies to [`poetry.lock` file](https://python-poetry.org/docs/libraries#lock-file).
>
>[`poetry.lock` prevents from automatically getting the latest versions of your dependencies](https://python-poetry.org/docs/basic-usage/#updating-dependencies-to-their-latest-versions).
>
> You can explicitly [write `lock` command to lock dependencies](https://python-poetry.org/docs/cli/#lock) listed in the `pyproject.toml`

Add specific version:

```
# multiple ways
# double quotes ("foo") for Windows CMD 

$ poetry add google-search-results@^2.1.0

$ poetry add 'google-search-results>=1.8.5'

$ poetry add 'google-search-results==1.8.5'

$ poetry add google-search-results@latest
```

> If you specify a constraint (`@` or `>=`), the dependency will be updated by using the specified constraint.
>
> Otherwise, if you try to add a package that is already present, you will get an error.

(*optional*) Install from existing project/package dependencies.

If you're using an already created project that has either `poetry.lock` or `pyproject.toml` files, you can install those dependencies to the virtual environment:

```
$ poetry install
```

> [The `install` command read](https://python-poetry.org/docs/cli/#install) `pyproject.toml` or `poetry.lock` file and installs all listed dependencies.
>
> [If there's a `poetry.lock` file](https://python-poetry.org/docs/basic-usage/#installing-with-poetrylock):
> - **Poetry uses the exact versions** listed in `poetry.lock`.
>
> [If there is no `poetry.lock` file](https://python-poetry.org/docs/basic-usage/#installing-without-poetrylock):
> - **Poetry will resolves all dependencies** from the `pyproject.toml` file and downloads the latest version of their files.


(*optional*) To not install development dependencies, use `--no-dev` argument:

```
$ poetry install --no-dev
```

___

<h4 id="activate_env"><b>Use added site packages</b> inside IDE</h4>

**If using `poetry`**, find a location of the initialized environment first [via `config --list` command](https://python-poetry.org/docs/cli#config). Look for `virtualenvs.path` in the output:

```
$ poetry config --list

cache-dir = "C:\\Users\\USER\\AppData\\Local\\pypoetry\\Cache"
experimental.new-installer = true
installer.parallel = true
virtualenvs.create = true
virtualenvs.in-project = null
👉virtualenvs.path = "{cache-dir}\\virtualenvs"  👉👉👉# C:\Users\USER\AppData\Local\pypoetry\Cache\virtualenvs
```

A few more steps to do:

- Go to the `virtualenvs.path` folder and open created environment folder (in my case its: `PROJECT-9SrbZw5z-py3.9`).

- Go to `Scripts` (Windows) or `bin` (Linux) folder, copy the full path and add `python.exe` at the end of the path:
```
C:\Users\USER\AppData\Local\pypoetry\Cache\virtualenvs\PROJECT-9SrbZw5z-py3.9\Scripts\python.exe
```

> `virtualenvs.path` is needed to find a path to `python.exe` inside created virtual environment which will let JetBrains or VSCode to [index installed site-packages](https://www.jetbrains.com/help/idea/indexing.html).


**If using `virtualenv`**, go to `env\Scripts\python.exe` folder in your project and copy the full path to the `python.exe` file and enter it as a System Interpreter inside IDE.

___

<h4>Activate and index installed packages</h4>

Currently, if you run the script inside IDE, it will look at the globally installed package (`serpapi`, for example) and will throw an error because globally there's no such library installed (it won't throw an error if it's installed):

```
Traceback (most recent call last):
  File "C:\Users\USER\PyCharmProjects\PROJECT\environment.py", line 1, in <module>
    from serpapi import GoogleSearch
ModuleNotFoundError: No module named 'serpapi'
```

<h4 id="vscode">VSCode version</h4>

To fix this in VSCode we need to [select a virtual environment Python Interpreter and set it as a System Interpreter](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment).

Open command palette `CTRL+SHIFT+P` and type: *Python: System Interpreter* ([Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) should be installed).

![Vscode_1](https://user-images.githubusercontent.com/78694043/145968033-cdb91765-f6b2-4ec4-be9e-0fe892e1b7e6.png)

Both for `virtualenv` and `poetry`, VSCode should automatically detect a proper `python.exe` file from the virtual environment.

If you don't see a proper path to `python.exe` from your virtual environment then you need to locate and enter it.

![Vscode_2](https://user-images.githubusercontent.com/78694043/145968041-14b6d7c1-7b40-4b62-9b25-9feb408f66c9.png)

Now you can run your Python scripts from the virtual environment either by the command line or using  [VSCode Code Runner extension](https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner).


<h4 id="pycharm">PyCharm version</h4>

To fix this in PyCharm we need to add the path to `python.exe` from the `virtualenv` folder and set it as a [PyCharm System Interpreter](https://www.jetbrains.com/help/pycharm/configuring-local-python-interpreters.html) which will index all site-packages from the virtual environment:

![pycharm_env_1](https://user-images.githubusercontent.com/78694043/144842354-86bc5461-3c23-44c8-b158-50d442556df9.png)

![pycharm_env_2](https://user-images.githubusercontent.com/78694043/144844623-98b9588d-bbc7-4cb2-9c18-ef25d091f619.png)

![pycharm_env_3](https://user-images.githubusercontent.com/78694043/144848170-4483e721-d3ad-44e5-8383-2d37b7f1dc4a.png)

![pycharm_env_4](https://user-images.githubusercontent.com/78694043/145018801-b10a3548-6377-45d2-9370-b39306b86bb9.png)

<h4 id="intellij">IntelliJ IDEA version</h4>

To fix this in IntelliJ IDEA we need to add the path to `python.exe` from the `virtualenv` folder as well and set it as a [PyCharm System Interpreter](https://www.jetbrains.com/help/pycharm/configuring-local-python-interpreters.html) with a few additional tweaks which will index all site-packages from the virtual environment:


![intellij_env_1](https://user-images.githubusercontent.com/78694043/144851324-bad5ae7c-f294-433c-aac3-e341ec2d24de.png)

![intellij_env_2](https://user-images.githubusercontent.com/78694043/144851331-a3ecb5a1-4eb1-4978-962b-10284d930343.png)

![intellij_env_3](https://user-images.githubusercontent.com/78694043/144851349-7bb66743-422f-4ddd-ba60-413b31769a8e.png)

![intellij_env_4](https://user-images.githubusercontent.com/78694043/144851356-9d7dbf34-f19b-44c8-ac82-78a6e244adbc.png)

![intellij_env_5](https://user-images.githubusercontent.com/78694043/145018901-b538bf67-eef0-4c26-aa94-29a75e9c6f72.png)


**Deactivate** virtual environment when done

To deactivate virtual environment *in order to use system Python* both in PyCharm, IntelliJ IDEA and VSCode you need to set Python System Interpreter back to the default one without `virtualenv` prefix for example: "*Python 3.9 virtualenv..*" ==> "*Python 3.9*", a reverse process of what's being shown above.

____

<h2 id="сonclusion">Conclusion</h2>

**Different project - different environment**

In short, it is better to use a virtual environment if you need to work with several projects at the same time which:
- use different library versions.
- use different Python versions.

**Installing globally will become a mess**

Installing globally different versions of the same library for different projects will quickly turn into a mess, there will be no order, or if there will be a need to install different versions of Python it will turn into a mess of all messes:

![image](https://user-images.githubusercontent.com/78694043/145216823-7f2c8c4f-d469-4315-a852-6f817e5fe10d.png)

___

<h2 id="links">Links</h2>

- [Virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
- [Poetry](https://python-poetry.org/docs/)
- [SerpApi libraries](https://serpapi.com/libraries)
- [Black&White illustration by xkcd.com](https://xkcd.com/1987/)

___

<h2 id="acknowledgments">Acknowledgments</h2>

A big thanks to these guys for helping out with the feedback about illustrations:

- [Ilya Z.](https://www.linkedin.com/in/ilyazub/)
- [Yevhen M.](https://www.linkedin.com/in/yevhen-mykhailov-043a341a1/)
- [Oleh V.](https://www.linkedin.com/in/exsesx/)
- [Yehor T.](https://www.linkedin.com/in/yehor-tishchenko-6a8a32159/)

___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions or suggestions to this blog post, feel free to reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://forum.serpapi.com/feature-requests">Feature Request</a>💫 or a <a href="https://forum.serpapi.com/bugs">Bug</a>🐞</p>