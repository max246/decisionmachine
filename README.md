Decision Machine
===============

The decision machine was an interactive installation made for Museum of the shared now and collaboration with Nicola.
In the repo you will find all the python, arduino and 3d model files to make the same thing by yourself.


Structure
=========

Twitter:
- main.py 
This start the main software that is looking for a twitter in real time that contains #yes or #no hashtag from a specific user.
Check the counter.cfg to change all the parameters.
- counterYes.py and counterNo.py
This start the communication with the arduino

Streaming:
- run.py
This start the ffmpeg streaming, the link is removed but you can replace with UStream link or another service

Arduino:
Just upload this file into your arduino and whatever counterYes or counterNo is sending, it will read it
The normal communication is:  UXXXX  where X is the number, example  U10 to send number 10.

STL:
All files to print containers, support, motor bracket, etc..



Link
====

www.max246.ch
http://projectsmax246.blogspot.co.uk/2014/10/marble-dispenser.html

