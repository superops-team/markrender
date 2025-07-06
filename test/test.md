# Think Python

## How to Think Like a Computer Scientist

Version 2.0.17

# Think Python

## How to Think Like a Computer Scientist

Version 2.0.17

Allen Downey

Green Tea Press

Needham, Massachusetts

Copyright © 2012 Allen Downey.

Green Tea Press 9 Washburn Ave Needham MA 02492

Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0 Unported License, which is available at [http:](http://creativecommons.org/licenses/by-nc/3.0/) [//creativecommons.org/licenses/by-nc/3.0/](http://creativecommons.org/licenses/by-nc/3.0/).

The original form of this book is LATEX source code. Compiling this LATEX source has the effect of generating a device-independent representation of a textbook, which can be converted to other formats and printed.

The LATEX source for this book is available from <http://www.thinkpython.com>

# <span id="page-4-0"></span>**Preface**

## **The strange history of this book**

In January 1999 I was preparing to teach an introductory programming class in Java. I had taught it three times and I was getting frustrated. The failure rate in the class was too high and, even for students who succeeded, the overall level of achievement was too low.

One of the problems I saw was the books. They were too big, with too much unnecessary detail about Java, and not enough high-level guidance about how to program. And they all suffered from the trap door effect: they would start out easy, proceed gradually, and then somewhere around Chapter 5 the bottom would fall out. The students would get too much new material, too fast, and I would spend the rest of the semester picking up the pieces.

Two weeks before the first day of classes, I decided to write my own book. My goals were:

- Keep it short. It is better for students to read 10 pages than not read 50 pages.
- Be careful with vocabulary. I tried to minimize the jargon and define each term at first use.
- Build gradually. To avoid trap doors, I took the most difficult topics and split them into a series of small steps.
- Focus on programming, not the programming language. I included the minimum useful subset of Java and left out the rest.

I needed a title, so on a whim I chose *How to Think Like a Computer Scientist*.

My first version was rough, but it worked. Students did the reading, and they understood enough that I could spend class time on the hard topics, the interesting topics and (most important) letting the students practice.

I released the book under the GNU Free Documentation License, which allows users to copy, modify, and distribute the book.

What happened next is the cool part. Jeff Elkner, a high school teacher in Virginia, adopted my book and translated it into Python. He sent me a copy of his translation, and I had the unusual experience of learning Python by reading my own book. As Green Tea Press, I published the first Python version in 2001.

In 2003 I started teaching at Olin College and I got to teach Python for the first time. The contrast with Java was striking. Students struggled less, learned more, worked on more interesting projects, and generally had a lot more fun.

Over the last nine years I continued to develop the book, correcting errors, improving some of the examples and adding material, especially exercises.

The result is this book, now with the less grandiose title *Think Python*. Some of the changes are:

- I added a section about debugging at the end of each chapter. These sections present general techniques for finding and avoiding bugs, and warnings about Python pitfalls.
- I added more exercises, ranging from short tests of understanding to a few substantial projects. And I wrote solutions for most of them.
- I added a series of case studies—longer examples with exercises, solutions, and discussion. Some are based on Swampy, a suite of Python programs I wrote for use in my classes. Swampy, code examples, and some solutions are available from <http://thinkpython.com>.
- I expanded the discussion of program development plans and basic design patterns.
- I added appendices about debugging, analysis of algorithms, and UML diagrams with Lumpy.

I hope you enjoy working with this book, and that it helps you learn to program and think, at least a little bit, like a computer scientist.

Allen B. Downey Needham MA

Allen Downey is a Professor of Computer Science at the Franklin W. Olin College of Engineering.

## **Acknowledgments**

Many thanks to Jeff Elkner, who translated my Java book into Python, which got this project started and introduced me to what has turned out to be my favorite language.

Thanks also to Chris Meyers, who contributed several sections to *How to Think Like a Computer Scientist*.

Thanks to the Free Software Foundation for developing the GNU Free Documentation License, which helped make my collaboration with Jeff and Chris possible, and Creative Commons for the license I am using now.

Thanks to the editors at Lulu who worked on *How to Think Like a Computer Scientist*.

Thanks to all the students who worked with earlier versions of this book and all the contributors (listed below) who sent in corrections and suggestions.

## **Contributor List**

More than 100 sharp-eyed and thoughtful readers have sent in suggestions and corrections over the past few years. Their contributions, and enthusiasm for this project, have been a huge help.

If you have a suggestion or correction, please send email to feedback@thinkpython.com. If I make a change based on your feedback, I will add you to the contributor list (unless you ask to be omitted).

If you include at least part of the sentence the error appears in, that makes it easy for me to search. Page and section numbers are fine, too, but not quite as easy to work with. Thanks!

- Lloyd Hugh Allen sent in a correction to Section 8.4.
- Yvon Boulianne sent in a correction of a semantic error in Chapter 5.
- Fred Bremmer submitted a correction in Section 2.1.
- Jonah Cohen wrote the Perl scripts to convert the LaTeX source for this book into beautiful HTML.
- Michael Conlon sent in a grammar correction in Chapter 2 and an improvement in style in Chapter 1, and he initiated discussion on the technical aspects of interpreters.
- Benoit Girard sent in a correction to a humorous mistake in Section 5.6.
- Courtney Gleason and Katherine Smith wrote horsebet.py, which was used as a case study in an earlier version of the book. Their program can now be found on the website.
- Lee Harr submitted more corrections than we have room to list here, and indeed he should be listed as one of the principal editors of the text.
- James Kaylin is a student using the text. He has submitted numerous corrections.
- David Kershaw fixed the broken catTwice function in Section 3.10.
- Eddie Lam has sent in numerous corrections to Chapters 1, 2, and 3. He also fixed the Makefile so that it creates an index the first time it is run and helped us set up a versioning scheme.
- Man-Yong Lee sent in a correction to the example code in Section 2.4.
- David Mayo pointed out that the word "unconsciously" in Chapter 1 needed to be changed to "subconsciously".
- Chris McAloon sent in several corrections to Sections 3.9 and 3.10.
- Matthew J. Moelter has been a long-time contributor who sent in numerous corrections and suggestions to the book.
- Simon Dicon Montford reported a missing function definition and several typos in Chapter 3. He also found errors in the increment function in Chapter 13.
- John Ouzts corrected the definition of "return value" in Chapter 3.
- Kevin Parks sent in valuable comments and suggestions as to how to improve the distribution of the book.
- David Pool sent in a typo in the glossary of Chapter 1, as well as kind words of encouragement.
- Michael Schmitt sent in a correction to the chapter on files and exceptions.

- Robin Shaw pointed out an error in Section 13.1, where the printTime function was used in an example without being defined.
- Paul Sleigh found an error in Chapter 7 and a bug in Jonah Cohen's Perl script that generates HTML from LaTeX.
- Craig T. Snydal is testing the text in a course at Drew University. He has contributed several valuable suggestions and corrections.
- Ian Thomas and his students are using the text in a programming course. They are the first ones to test the chapters in the latter half of the book, and they have made numerous corrections and suggestions.
- Keith Verheyden sent in a correction in Chapter 3.
- Peter Winstanley let us know about a longstanding error in our Latin in Chapter 3.
- Chris Wrobel made corrections to the code in the chapter on file I/O and exceptions.
- Moshe Zadka has made invaluable contributions to this project. In addition to writing the first draft of the chapter on Dictionaries, he provided continual guidance in the early stages of the book.
- Christoph Zwerschke sent several corrections and pedagogic suggestions, and explained the difference between *gleich* and *selbe*.
- James Mayer sent us a whole slew of spelling and typographical errors, including two in the contributor list.
- Hayden McAfee caught a potentially confusing inconsistency between two examples.
- Angel Arnal is part of an international team of translators working on the Spanish version of the text. He has also found several errors in the English version.
- Tauhidul Hoque and Lex Berezhny created the illustrations in Chapter 1 and improved many of the other illustrations.
- Dr. Michele Alzetta caught an error in Chapter 8 and sent some interesting pedagogic comments and suggestions about Fibonacci and Old Maid.
- Andy Mitchell caught a typo in Chapter 1 and a broken example in Chapter 2.
- Kalin Harvey suggested a clarification in Chapter 7 and caught some typos.
- Christopher P. Smith caught several typos and helped us update the book for Python 2.2.
- David Hutchins caught a typo in the Foreword.
- Gregor Lingl is teaching Python at a high school in Vienna, Austria. He is working on a German translation of the book, and he caught a couple of bad errors in Chapter 5.
- Julie Peters caught a typo in the Preface.
- Florin Oprina sent in an improvement in makeTime, a correction in printTime, and a nice typo.
- D. J. Webre suggested a clarification in Chapter 3.
- Ken found a fistful of errors in Chapters 8, 9 and 11.
- Ivo Wever caught a typo in Chapter 5 and suggested a clarification in Chapter 3.
- Curtis Yanko suggested a clarification in Chapter 2.

- Ben Logan sent in a number of typos and problems with translating the book into HTML.
- Jason Armstrong saw the missing word in Chapter 2.
- Louis Cordier noticed a spot in Chapter 16 where the code didn't match the text.
- Brian Cain suggested several clarifications in Chapters 2 and 3.
- Rob Black sent in a passel of corrections, including some changes for Python 2.2.
- Jean-Philippe Rey at Ecole Centrale Paris sent a number of patches, including some updates for Python 2.2 and other thoughtful improvements.
- Jason Mader at George Washington University made a number of useful suggestions and corrections.
- Jan Gundtofte-Bruun reminded us that "a error" is an error.
- Abel David and Alexis Dinno reminded us that the plural of "matrix" is "matrices", not "matrixes". This error was in the book for years, but two readers with the same initials reported it on the same day. Weird.
- Charles Thayer encouraged us to get rid of the semi-colons we had put at the ends of some statements and to clean up our use of "argument" and "parameter".
- Roger Sperberg pointed out a twisted piece of logic in Chapter 3.
- Sam Bull pointed out a confusing paragraph in Chapter 2.
- Andrew Cheung pointed out two instances of "use before def."
- C. Corey Capel spotted the missing word in the Third Theorem of Debugging and a typo in Chapter 4.
- Alessandra helped clear up some Turtle confusion.
- Wim Champagne found a brain-o in a dictionary example.
- Douglas Wright pointed out a problem with floor division in arc.
- Jared Spindor found some jetsam at the end of a sentence.
- Lin Peiheng sent a number of very helpful suggestions.
- Ray Hagtvedt sent in two errors and a not-quite-error.
- Torsten Hübsch pointed out an inconsistency in Swampy.
- Inga Petuhhov corrected an example in Chapter 14.
- Arne Babenhauserheide sent several helpful corrections.
- Mark E. Casida is is good at spotting repeated words.
- Scott Tyler filled in a that was missing. And then sent in a heap of corrections.
- Gordon Shephard sent in several corrections, all in separate emails.
- Andrew Turner spotted an error in Chapter 8.
- Adam Hobart fixed a problem with floor division in arc.

- Daryl Hammond and Sarah Zimmerman pointed out that I served up math.pi too early. And Zim spotted a typo.
- George Sass found a bug in a Debugging section.
- Brian Bingham suggested Exercise [11.10.](#page-132-0)
- Leah Engelbert-Fenton pointed out that I used tuple as a variable name, contrary to my own advice. And then found a bunch of typos and a "use before def."
- Joe Funke spotted a typo.
- Chao-chao Chen found an inconsistency in the Fibonacci example.
- Jeff Paine knows the difference between space and spam.
- Lubos Pintes sent in a typo.
- Gregg Lind and Abigail Heithoff suggested Exercise [14.4.](#page-160-0)
- Max Hailperin has sent in a number of corrections and suggestions. Max is one of the authors of the extraordinary *Concrete Abstractions*, which you might want to read when you are done with this book.
- Chotipat Pornavalai found an error in an error message.
- Stanislaw Antol sent a list of very helpful suggestions.
- Eric Pashman sent a number of corrections for Chapters 4–11.
- Miguel Azevedo found some typos.
- Jianhua Liu sent in a long list of corrections.
- Nick King found a missing word.
- Martin Zuther sent a long list of suggestions.
- Adam Zimmerman found an inconsistency in my instance of an "instance" and several other errors.
- Ratnakar Tiwari suggested a footnote explaining degenerate triangles.
- Anurag Goel suggested another solution for is\_abecedarian and sent some additional corrections. And he knows how to spell Jane Austen.
- Kelli Kratzer spotted one of the typos.
- Mark Griffiths pointed out a confusing example in Chapter 3.
- Roydan Ongie found an error in my Newton's method.
- Patryk Wolowiec helped me with a problem in the HTML version.
- Mark Chonofsky told me about a new keyword in Python 3.
- Russell Coleman helped me with my geometry.
- Wei Huang spotted several typographical errors.
- Karen Barber spotted the the oldest typo in the book.

- Nam Nguyen found a typo and pointed out that I used the Decorator pattern but didn't mention it by name.
- Stéphane Morin sent in several corrections and suggestions.
- Paul Stoop corrected a typo in uses\_only.
- Eric Bronner pointed out a confusion in the discussion of the order of operations.
- Alexandros Gezerlis set a new standard for the number and quality of suggestions he submitted. We are deeply grateful!
- Gray Thomas knows his right from his left.
- Giovanni Escobar Sosa sent a long list of corrections and suggestions.
- Alix Etienne fixed one of the URLs.
- Kuang He found a typo.
- Daniel Neilson corrected an error about the order of operations.
- Will McGinnis pointed out that polyline was defined differently in two places.
- Swarup Sahoo spotted a missing semi-colon.
- Frank Hecker pointed out an exercise that was under-specified, and some broken links.
- Animesh B helped me clean up a confusing example.
- Martin Caspersen found two round-off errors.
- Gregor Ulm sent several corrections and suggestions.
- Dimitrios Tsirigkas suggested I clarify an exercise.
- Carlos Tafur sent a page of corrections and suggestions.
- Martin Nordsletten found a bug in an exercise solution.
- Lars O.D. Christensen found a broken reference.
- Victor Simeone found a typo.
- Sven Hoexter pointed out that a variable named input shadows a built-in function.
- Viet Le found a typo.
- Stephen Gregory pointed out the problem with cmp in Python 3.
- Matthew Shultz let me know about a broken link.
- Lokesh Kumar Makani let me know about some broken links and some changes in error messages.
- Ishwar Bhat corrected my statement of Fermat's last theorem.
- Brian McGhie suggested a clarification.
- Andrea Zanella translated the book into Italian, and sent a number of corrections along the way.

# **Contents**

|   | Preface                                     |                                      |    |  |  |
|---|---------------------------------------------|--------------------------------------|----|--|--|
| 1 |                                             | The way of the program               | 1  |  |  |
|   | 1.1                                         | The Python programming language<br>. | 1  |  |  |
|   | 1.2                                         | What is a program?                   | 3  |  |  |
|   | 1.3                                         | What is debugging?                   | 3  |  |  |
|   | 1.4                                         | Formal and natural languages         | 5  |  |  |
|   | 1.5                                         | The first program<br>.               | 6  |  |  |
|   | 1.6                                         | Debugging                            | 7  |  |  |
|   | 1.7                                         | Glossary<br>.                        | 7  |  |  |
|   | 1.8                                         | Exercises<br>.                       | 9  |  |  |
| 2 | Variables, expressions and statements<br>11 |                                      |    |  |  |
|   | 2.1                                         | Values and types<br>.                | 11 |  |  |
|   | 2.2                                         | Variables<br>.                       | 12 |  |  |
|   | 2.3                                         | Variable names and keywords          | 12 |  |  |
|   | 2.4                                         | Operators and operands<br>.          | 13 |  |  |
|   | 2.5                                         | Expressions and statements<br>.      | 14 |  |  |
|   | 2.6                                         | Interactive mode and script mode     | 14 |  |  |
|   | 2.7                                         | Order of operations                  | 15 |  |  |
|   | 2.8                                         | String operations<br>.               | 15 |  |  |
|   | 2.9                                         | Comments<br>.                        | 16 |  |  |
|   | 2.10                                        | Debugging                            | 16 |  |  |
|   | 2.11                                        | Glossary<br>.                        | 17 |  |  |
|   | 2.12                                        | Exercises<br>.                       | 18 |  |  |

| 3 | Functions |                                         | 19 |
|---|-----------|-----------------------------------------|----|
|   | 3.1       | Function calls<br>.                     | 19 |
|   | 3.2       | Type conversion functions               | 19 |
|   | 3.3       | Math functions                          | 20 |
|   | 3.4       | Composition                             | 21 |
|   | 3.5       | Adding new functions<br>.               | 21 |
|   | 3.6       | Definitions and uses<br>.               | 22 |
|   | 3.7       | Flow of execution<br>.                  | 23 |
|   | 3.8       | Parameters and arguments                | 23 |
|   | 3.9       | Variables and parameters are local<br>. | 24 |
|   | 3.10      | Stack diagrams<br>.                     | 25 |
|   | 3.11      | Fruitful functions and void functions   | 26 |
|   | 3.12      | Why functions?<br>.                     | 26 |
|   | 3.13      | Importing with from<br>.                | 27 |
|   | 3.14      | Debugging                               | 27 |
|   | 3.15      | Glossary<br>.                           | 28 |
|   | 3.16      | Exercises<br>.                          | 29 |
|   |           |                                         |    |
| 4 |           | Case study: interface design            | 31 |
|   | 4.1       | TurtleWorld<br>.                        | 31 |
|   | 4.2       | Simple repetition<br>.                  | 32 |
|   | 4.3       | Exercises<br>.                          | 33 |
|   | 4.4       | Encapsulation<br>.                      | 34 |
|   | 4.5       | Generalization                          | 34 |
|   | 4.6       | Interface design<br>.                   | 35 |
|   | 4.7       | Refactoring                             | 36 |
|   | 4.8       | A development plan<br>.                 | 37 |
|   | 4.9       | docstring                               | 37 |
|   | 4.10      | Debugging                               | 38 |
|   | 4.11      | Glossary<br>.                           | 38 |
|   | 4.12      | Exercises<br>.                          | 39 |

| 5 |      | Conditionals and recursion             | 41 |
|---|------|----------------------------------------|----|
|   | 5.1  | Modulus operator                       | 41 |
|   | 5.2  | Boolean expressions                    | 41 |
|   | 5.3  | Logical operators<br>.                 | 42 |
|   | 5.4  | Conditional execution<br>.             | 42 |
|   | 5.5  | Alternative execution                  | 43 |
|   | 5.6  | Chained conditionals                   | 43 |
|   | 5.7  | Nested conditionals                    | 43 |
|   | 5.8  | Recursion                              | 44 |
|   | 5.9  | Stack diagrams for recursive functions | 45 |
|   | 5.10 | Infinite recursion<br>.                | 46 |
|   | 5.11 | Keyboard input<br>.                    | 46 |
|   | 5.12 | Debugging                              | 47 |
|   | 5.13 | Glossary<br>.                          | 48 |
|   | 5.14 | Exercises<br>.                         | 49 |
|   |      |                                        |    |
| 6 |      | Fruitful functions                     | 51 |
|   | 6.1  | Return values<br>.                     | 51 |
|   | 6.2  | Incremental development<br>.           | 52 |
|   | 6.3  | Composition                            | 54 |
|   | 6.4  | Boolean functions                      | 54 |
|   | 6.5  |                                        |    |
|   |      | More recursion                         | 55 |
|   | 6.6  | Leap of faith<br>.                     | 57 |
|   | 6.7  | One more example<br>.                  | 57 |
|   | 6.8  | Checking types<br>.                    | 58 |
|   | 6.9  | Debugging                              | 59 |
|   | 6.10 | Glossary<br>.                          | 60 |

| 7 | Iteration                   |                            | 63 |  |  |
|---|-----------------------------|----------------------------|----|--|--|
|   | 7.1                         | Multiple assignment<br>.   | 63 |  |  |
|   | 7.2                         | Updating variables<br>.    | 64 |  |  |
|   | 7.3                         | The while statement<br>.   | 64 |  |  |
|   | 7.4                         | break<br>.                 | 65 |  |  |
|   | 7.5                         | Square roots<br>.          | 66 |  |  |
|   | 7.6                         | Algorithms                 | 67 |  |  |
|   | 7.7                         | Debugging                  | 68 |  |  |
|   | 7.8                         | Glossary<br>.              | 68 |  |  |
|   | 7.9                         | Exercises<br>.             | 69 |  |  |
| 8 | Strings                     |                            | 71 |  |  |
|   | 8.1                         | A string is a sequence     | 71 |  |  |
|   | 8.2                         | len<br>.                   | 71 |  |  |
|   | 8.3                         | Traversal with a for loop  | 72 |  |  |
|   | 8.4                         | String slices<br>.         | 73 |  |  |
|   | 8.5                         | Strings are immutable<br>. | 74 |  |  |
|   | 8.6                         | Searching                  | 74 |  |  |
|   | 8.7                         | Looping and counting<br>.  | 75 |  |  |
|   | 8.8                         | String methods<br>.        | 75 |  |  |
|   | 8.9                         | The in operator<br>.       | 76 |  |  |
|   | 8.10                        | String comparison          | 76 |  |  |
|   | 8.11                        | Debugging                  | 77 |  |  |
|   | 8.12                        | Glossary<br>.              | 78 |  |  |
|   | 8.13                        | Exercises<br>.             | 79 |  |  |
| 9 | Case study: word play<br>81 |                            |    |  |  |
|   | 9.1                         | Reading word lists<br>.    | 81 |  |  |
|   | 9.2                         | Exercises<br>.             | 82 |  |  |
|   | 9.3                         | Search                     | 82 |  |  |
|   | 9.4                         | Looping with indices       | 83 |  |  |
|   | 9.5                         | Debugging                  | 85 |  |  |
|   | 9.6                         | Glossary<br>.              | 85 |  |  |
|   | 9.7                         | Exercises<br>.             | 86 |  |  |

| 10 Lists |                                 | 87  |
|----------|---------------------------------|-----|
| 10.1     | A list is a sequence<br>.       | 87  |
| 10.2     | Lists are mutable<br>.          | 87  |
| 10.3     | Traversing a list<br>.          | 89  |
| 10.4     | List operations                 | 89  |
| 10.5     | List slices                     | 89  |
| 10.6     | List methods                    | 90  |
| 10.7     | Map, filter and reduce<br>.     | 91  |
| 10.8     | Deleting elements               | 92  |
| 10.9     | Lists and strings               | 93  |
| 10.10    | Objects and values<br>.         | 93  |
| 10.11    | Aliasing                        | 94  |
| 10.12    | List arguments                  | 95  |
| 10.13    | Debugging                       | 96  |
| 10.14    | Glossary<br>.                   | 97  |
| 10.15    | Exercises<br>.                  | 98  |
|          |                                 |     |
|          | 11 Dictionaries                 | 101 |
| 11.1     | Dictionary as a set of counters | 102 |
| 11.2     | Looping and dictionaries        | 103 |
| 11.3     | Reverse lookup<br>.             | 104 |
| 11.4     | Dictionaries and lists<br>.     | 105 |
| 11.5     | Memos<br>.                      | 106 |
| 11.6     | Global variables                | 108 |
| 11.7     | Long integers<br>.              | 109 |
| 11.8     | Debugging                       | 109 |
| 11.9     | Glossary<br>.                   | 110 |
| 11.10    | Exercises<br>.                  | 111 |

| 12 Tuples    |                                                         | 113        |
|--------------|---------------------------------------------------------|------------|
| 12.1         | Tuples are immutable                                    | 113        |
| 12.2         | Tuple assignment<br>.                                   | 114        |
| 12.3         | Tuples as return values                                 | 115        |
| 12.4         | Variable-length argument tuples<br>.                    | 115        |
| 12.5         | Lists and tuples<br>.                                   | 116        |
| 12.6         | Dictionaries and tuples                                 | 117        |
| 12.7         | Comparing tuples                                        | 118        |
| 12.8         | Sequences of sequences                                  | 119        |
| 12.9         | Debugging                                               | 120        |
| 12.10        | Glossary<br>.                                           | 121        |
| 12.11        | Exercises<br>.                                          | 121        |
|              | 13 Case study: data structure selection                 | 123        |
|              |                                                         |            |
| 13.1         | Word frequency analysis                                 | 123        |
| 13.2<br>13.3 | Random numbers<br>Word histogram                        | 124<br>125 |
| 13.4         | Most common words                                       | 126        |
|              |                                                         |            |
| 13.5<br>13.6 | Optional parameters<br>.<br>Dictionary subtraction<br>. | 126<br>127 |
| 13.7         | Random words<br>.                                       | 127        |
| 13.8         | Markov analysis                                         | 128        |
| 13.9         | Data structures                                         | 129        |
| 13.10        | Debugging                                               | 131        |
| 13.11        | Glossary<br>.                                           | 132        |
| 13.12        | Exercises<br>.                                          | 132        |
|              |                                                         |            |
| 14 Files     |                                                         | 133        |
| 14.1         | Persistence                                             | 133        |
| 14.2         | Reading and writing<br>.                                | 133        |
| 14.3         | Format operator                                         | 134        |
| 14.4         | Filenames and paths<br>.                                | 135        |

| 14.5  | Catching exceptions             | 136 |
|-------|---------------------------------|-----|
| 14.6  | Databases                       | 137 |
| 14.7  | Pickling                        | 137 |
| 14.8  | Pipes<br>.                      | 138 |
| 14.9  | Writing modules                 | 139 |
| 14.10 | Debugging                       | 140 |
| 14.11 | Glossary<br>.                   | 141 |
| 14.12 | Exercises<br>.                  | 141 |
|       |                                 |     |
|       | 15 Classes and objects          | 143 |
| 15.1  | User-defined types<br>.         | 143 |
| 15.2  | Attributes<br>.                 | 144 |
| 15.3  | Rectangles<br>.                 | 145 |
| 15.4  | Instances as return values<br>. | 146 |
| 15.5  | Objects are mutable             | 146 |
| 15.6  | Copying<br>.                    | 147 |
| 15.7  | Debugging                       | 148 |
| 15.8  | Glossary<br>.                   | 149 |
| 15.9  | Exercises<br>.                  | 149 |
|       | 16 Classes and functions        | 151 |
|       |                                 |     |
| 16.1  | Time                            | 151 |
| 16.2  | Pure functions                  | 151 |
| 16.3  | Modifiers                       | 153 |
| 16.4  | Prototyping versus planning     | 154 |
| 16.5  | Debugging                       | 155 |
| 16.6  | Glossary<br>.                   | 155 |
| 16.7  | Exercises<br>.                  | 156 |

|                | 17 Classes and methods            | 157        |
|----------------|-----------------------------------|------------|
| 17.1           | Object-oriented features<br>.     | 157        |
| 17.2           | Printing objects<br>.             | 158        |
| 17.3           | Another example<br>.              | 159        |
| 17.4           | A more complicated example<br>.   | 160        |
| 17.5           | The init method<br>.              | 160        |
| 17.6           | The __str__ method<br>.           | 161        |
| 17.7           | Operator overloading              | 161        |
| 17.8           | Type-based dispatch<br>.          | 162        |
| 17.9           | Polymorphism                      | 163        |
| 17.10          | Debugging                         | 164        |
| 17.11          | Interface and implementation<br>. | 164        |
| 17.12          | Glossary<br>.                     | 165        |
| 17.13          | Exercises<br>.                    | 165        |
|                |                                   |            |
|                |                                   |            |
| 18 Inheritance |                                   | 167        |
| 18.1           | Card objects<br>.                 | 167        |
| 18.2           | Class attributes<br>.             | 168        |
| 18.3           | Comparing cards<br>.              | 169        |
| 18.4           | Decks                             | 170        |
| 18.5           | Printing the deck<br>.            | 171        |
| 18.6           | Add, remove, shuffle and sort     | 171        |
| 18.7           | Inheritance                       | 172        |
| 18.8           | Class diagrams<br>.               | 173        |
| 18.9           | Debugging                         | 174        |
| 18.10          | Data encapsulation<br>.           | 175        |
| 18.11<br>18.12 | Glossary<br>.<br>Exercises<br>.   | 176<br>177 |

|   |                  | 19 Case study: Tkinter                   | 179 |
|---|------------------|------------------------------------------|-----|
|   | 19.1             | GUI<br>.                                 | 179 |
|   | 19.2             | Buttons and callbacks                    | 180 |
|   | 19.3             | Canvas widgets<br>.                      | 181 |
|   | 19.4             | Coordinate sequences                     | 182 |
|   | 19.5             | More widgets<br>.                        | 182 |
|   | 19.6             | Packing widgets                          | 183 |
|   | 19.7             | Menus and Callables<br>.                 | 185 |
|   | 19.8             | Binding                                  | 186 |
|   | 19.9             | Debugging                                | 188 |
|   | 19.10            | Glossary<br>.                            | 189 |
|   | 19.11            | Exercises<br>.                           | 190 |
| A | Debugging<br>193 |                                          |     |
|   | A.1              | Syntax errors                            | 193 |
|   | A.2              | Runtime errors                           | 195 |
|   | A.3              | Semantic errors<br>.                     | 198 |
| B |                  | Analysis of Algorithms                   | 201 |
|   | B.1              | Order of growth                          | 202 |
|   | B.2              | Analysis of basic Python operations<br>. | 204 |
|   | B.3              | Analysis of search algorithms<br>.       | 205 |
|   | B.4              | Hashtables                               | 206 |
| C | Lumpy            |                                          | 211 |
|   | C.1              | State diagram<br>.                       | 211 |
|   | C.2              | Stack diagram<br>.                       | 212 |
|   | C.3              | Object diagrams                          | 213 |
|   | C.4              | Function and class objects<br>.          | 215 |
|   | C.5              | Class Diagrams<br>.                      | 216 |
|   |                  |                                          |     |