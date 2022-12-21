# Functional-Python-Programming-3rd-Edition

This is the code repository for [Functional Python Programming - Third Edition](https://www.packtpub.com/application-development/functional-python-programming-third-edition?utm_source=github&utm_medium=repository&utm_campaign=9781788627061), published by [Packt](https://www.packtpub.com/?utm_source=github). It contains all the supporting project files necessary to work through the book from start to finish.

## About the Book
If you’re a Python developer who wants to discover how to take the power of functional programming (FP) and bring it into your own programs, then this book is essential for you, even if you know next to nothing about the paradigm.

Starting with a general overview of functional concepts, you’ll explore common functional features such as first-class and higher-order functions, pure functions, and more. You’ll see how these are accomplished in Python 3.6 to give you the core foundations you’ll build upon. After that, you’ll discover common functional optimizations for Python to help your apps reach even higher speeds.

You’ll learn FP concepts such as lazy evaluation using Python’s generator functions and expressions. Moving forward, you’ll learn to design and implement decorators to create composite functions. You'll also explore data preparation techniques and data exploration in depth, and see how the Python standard library fits the functional programming model. Finally, to top off your journey into the world of functional Python, you’ll at look at the PyMonad project and some larger examples to put everything into perspective.

## Instructions and Navigation
All of the code is organized into folders. Each folder starts with a number followed by the application name. For example, Chapter02.



The code will look like the following:
```
s = 0 
for n in range(1, 10): 
    if n % 3 == 0 or n % 5 == 0: 
        s += n 
print(s) 
```

This book presumes some familiarity with Python 3 and general concepts of application development. We won’t look deeply at subtle or complex features of Python; we’ll avoid much consideration of the internals of the language.

We’ll presume some familiarity with functional programming. Since Python is not a functional programming language, we can’t dig deeply into functional concepts. We’ll pick and choose the aspects of functional programming that fit well with Python and leverage just those that seem useful.

Some of the examples use exploratory data analysis (EDA) as a problem domain to show the value of functional programming. Some familiarity with basic probability and statistics will help with this. There are only a few examples that move into more serious data science.

You’ll need to have Python 3.10 installed and running. 
For more information on Python, visit http://www.python.org/. 

There are two paths to installing the required packages:

- Conda. This requires an additional install of mini Conda. Visit https://docs.conda.io/en/latest/miniconda.html to download and install Conda and use it to build a virtual environment.

- PIP and venv. These are built-in.

### Conda Installation

When using the **conda** tool, start with an installation of Miniconda.
See https://docs.conda.io/en/latest/miniconda.html

After the **conda** tool is installed,
the required packages can be installed using the following:

```bash
conda create -n functional3 --channel=conda-forge  python=3.10 --file requirements-conda.txt
conda activate functional3
python -m pip install pymonad==2.4.0
```

This will create and activate a virtual environment for the examples in the book.

Skip over the PIP installation section.

### PIP Installation

When using the **PIP**  and **venv** tools, the required packages can be installed using the following:

```bash
python3 -m venv functional3
```

This must be activated. The command varies between OS's.

For Windows, use this command:

```bash
functional3\Scripts\activate.bat
```

For Linux and macOS, use this command:

```bash
source functional3/bin/activate
```

Then, use the following to install all the packages.

```bash
python -m pip install -rrequirements.txt
```

### Test Suite

There's a comprehensive test suite for the code that's run using the **tox** tool.
To confirm that all the tests pass run the following:

```bash
$ tox
```

To run the tests for a particular chapter you can use a command like the following:

```bash
$ tox -e ch01
```


## Related Products
* [Functional Python Programming](https://www.packtpub.com/application-development/functional-python-programming?utm_source=github&utm_medium=repository&utm_campaign=9781784396992)

* [Learn Python Programming - Fundamentals of Python - Second Edition](https://www.packtpub.com/application-development/learn-python-programming-fundamentals-python?utm_source=github&utm_medium=repository&utm_campaign=9781788996662)

* [Neural Network Programming with Python](https://www.packtpub.com/big-data-and-business-intelligence/neural-network-programming-python?utm_source=github&utm_medium=repository&utm_campaign=9781784398217)

### Suggestions and Feedback
[Click here](https://docs.google.com/forms/d/e/1FAIpQLSe5qwunkGf6PUvzPirPDtuy1Du5Rlzew23UBp2S-P3wB-GcwQ/viewform) if you have any feedback or suggestions.

