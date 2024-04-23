# Making Critical Making Critical Making

# Overview

The Project mainly consists of hardware part which includes a router(for creating local network),

a printer, a clock, and a computational devices.

The computational devices can include any platform, for the purpose of ease the code below will mainly demonstrate under the platform of mac os.

# Hardware setup

1. connect the router to the plug
2. connect the printer to the plug
3. connect the computer to the wifi emitted by the router
4. connect the computer to the printer in the local net
5. hang the clock
6. and then you are ready to critical making

# Software setup

as for the software part, you need to install python 3.11 first,

you can download them in the official website of python,

for most of the devices python is already embbeded,

you can type in 

```jsx
python
```

or

```jsx
python3 
```

in the terminal to check out whether it has been installed

and then you need to install git for getting the script or you can just download the script from

[https://github.com/longpp17/Critical-Making-Critical-Making/tree/master](https://github.com/longpp17/Critical-Making-Critical-Making/tree/master)

but if you already have git installed, just execute this in the terminal

```jsx
git clone https://github.com/longpp17/Critical-Making-Critical-Making.git
```

and then 

```jsx
cd Critical-Making-Critical-Making
pip3 install -r requirements.txt
```

then create a new text file with your open-ai key inside

```jsx
nano api_key.txt
```

# Execute

enter the directory and then run

```jsx
python main.py <start-time> <time-scale> <mode>
```

start-time should be something like “03:30:00”

mode should be  “test” “cpfighter” or “normal”


# DO WHAT THE FUCK YOU WANT TO
all the code is open sourced under DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE

it’s free to do everything with them, including remaking them
