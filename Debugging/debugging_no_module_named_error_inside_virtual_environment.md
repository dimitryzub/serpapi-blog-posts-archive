- <a href="#problem">The Problem</a>
    - <a href="#error">The Error</a>
    - <a href="#debugging">Process of Debugging</a>
        - <a href="#additional_thoughts">Additional Thoughts</a>
- <a href="#thoughts">Thoughts on the problem</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

<h3 id="problem">The Problem</h3>

Today I stumbled upon to a not a very straightforward issue while using IntelliJ IDEA via Python Plugin, and PyCharm. In other words IntelliJ IDEA and PyCharm not recognizing installed packages inside virtual environment.

When running the script via `Run` button, it blows up with an error but when running the script from the command line it runs with no errors, as it supposed to.


<h3 id="error">The Error (via Run button)</h3>

```lang-none
$ python wierd_error.py

Traceback (most recent call last):
  File "C:\Users\path_to_file", line 943, in <module>
    import bcrypt
ModuleNotFoundError: No module named 'bcrypt'
```

1. Python script is executing.
2. When trying to import a package blows up with an error.

The error is clearly says:

> *Hey man, there's no `bcrypt` module, just go and install it.*

BUT (*DUDE, THE MODULE IS RIGHT THERE! COME ON!*) it was already installed to the virtual environment, and I'm not really sure if I did something wrong, or the program didn't do what I expected. But at that moment I wanted to break the table in half.

Before running the script I've created a `env` folder for a project to isolate it from globally installed packages.

```
python -m venv env
```

Then I activate it:

```
$ source env/Scripts/activate

(env)
```

After that, I installed a few packages via `pip install`. They were installed to `env` folder as they should, and I confirmed it via `pip list` command to print out all install packages in the `virtualenv`.

```lang-none
$ pip list

Package    Version
---------- -------
bcrypt     3.2.0    <-- It's there!
pip        21.1.1
setuptools 56.0.0
```

So why on Earth does the script blows up with an error while using `Run` button but runs smoothly from the command line both inside IntelliJ IDEA and PyCharm?

<h3 id="debugging">Process of debugging</h3>


#### Idea 1. Tinker everything inside Project Structure settings

*The following examples will be from IntelliJ IDEA but almost the same thing happening in the PyCharm.*

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mp7ngln6j8nwq6nxuhr8.png)

I was trying to change project interpreter SDK/Setting, create module (*inside project structure settings*) for absolute no reason just to test if it helps. There's not much I could say about this idea, but this process goes in circle for a few hours in and Googling related things at the same time.


#### Idea 2. Test in other IDE

After trying the same thing for a few hours I tried to test if the same behavior will be in other IDE's such as PyCharm and VSCode. And the answer is "Yes", same behavior, in terminal runs, via `Run` button explodes with an error.

At that point I understand that something happening inside IDE since running from a command line everything runs as it should, so I focused on figuring out what causes error inside IDE.

#### Idea 3. Google "pycharm not recognizing installed packages"

At this point I was trying to formulate a problem in order to google it. The first Google results was exactly what I was looking for [PyCharm doesn't recognise installed module](https://stackoverflow.com/questions/31235376/pycharm-doesnt-recognise-installed-module).

This is the [answer](https://stackoverflow.com/a/46285214/15164646) that helped to solve the problem which said:

> Pycharm is unable to recognize installed local modules, since python interpreter selected is wrong. It should be the one, where your pip packages are installed i.e. virtual environment.

The person who answer the question had the similar problem I had:

> I had installed packages via pip in Windows. In Pycharm, they were neither detected nor any other Python interpreter was being shown (only python 3.6 is installed on my system).

#### Step 4. Change Project SDK to python.exe from virtual environment

In order to make it work I first found where `python.exe` inside virtual environment folder is located, and copied the full path.

Then, go to `Project Structure` settings (*CTRL+ALT+SHIFT+S*) -> `SDK's` -> `Add new SDK` -> `Add Python SDK` -> `System interpreter` -> changed existing path to the one I just copied. Done!

Path changed from this:

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7m3nea9p6yue3zz9qg5x.png)

To this:

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qx569notlyz7yl41psiq.png)

One thing left. We also need to change Python interpreter path inside `Run Configuration` to the one that was just created inside `System Interpreter` under `Project Structure`:

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k17kts05lowjk9o66xkd.png)

Changing Python interpreter path from the default one:

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2li6i01pbiynoh1pf68y.png)


<h3 id="additional_thoughts">Additional Thoughts</h3>


I'm not creating another virtual environment (`venv`) that PyCharm provides because I already create it from the command line beforehand, that's why I change path inside *System Interpreter*.

It can be also achieved by creating new `Virtual Environment` instead of creating it from command line (*basically the same process as described above*):

- Set `Base Interpreter` to whatever Python version is running.

- *Make sure* that `Project SDK` (*`Project Structure` window*) is set to the one from `Virtual Environment` (`Python 3.9 (some words)`).

- Open `Run Configuration` -> `Python Interpreter` -> `Use specific interpreter` path is set to `python.exe` path from the `venv` folder (e.g. newly created `virtual environment`).

Note: When using such method, Bash commands not found for unknown for me reason.

```
$ which python

bash: which: command not found
()  <- tells that you're currently in virtualenv
```

But when creating `env` manually (`python -m venv env`), Bash commands are working.

___

<h3 id="thoughts">Thoughts on the problem</h3>

I thought that IntelliJ IDEA, PyCharm handles such things under the hood so end user doesn't have to think about it, just create an `env`, activate it via `$ source env/Scripts/activate` and it works.

I should skip tinkering step right away after few minutes of trying to formulate the problem correctly and googling it instead of torture myself for over an hour.

In the end, I'm happy that I've stumbled upon such problem because with new problems it will be much easier to understand what steps to do based on the previous experience.

___

<h3 id="links">Links</h3>

- [StackOverflow question](https://stackoverflow.com/questions/31235376/pycharm-doesnt-recognise-installed-module/46285214#46285214)
- [StackOverflow answer](https://stackoverflow.com/a/46285214/15164646)
- [Googling the problem](https://www.google.com/search?q=pycharm+not+recognizing+installed+packages)

___

<h3 id="outro">Outro</h3>

If you have anything to share, any questions, suggestions, feel free to drop a comment in the comment section or reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub).

Yours,
Dimitry