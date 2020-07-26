# Question Cards
## About
This project takes a txt with questions as input and outputs the questions as a card in pdf format, readyto print on a site like https://www.printenbind.nl/losbladig/speelkaarten. This project was inspired by the 36 questions that lead to love. 
## What more
I've used it for generating cards, but you can change the code to fit your needs. You can use it to generate a lot of illustrations with only a small difference (e.g. text changed on each of them). I first wanted to use svg's to define the template, but that didn't have good options for text wrapping, so HTML was the way to go.
## Installing and running
This instructions are for Ubuntu, but are similar on other linux distros. 
### Getting the project
```bash
git clone https://github.com/arnodeceuninck/question-cards
cd question-cards
```
### Installing dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
sudo apt-get install wkhtmltopdf
```
### Running the script
```bash
python3 main.py
```

## Using your own questions
You can change the content of `questions.txt` to use your own questions to generate cards.