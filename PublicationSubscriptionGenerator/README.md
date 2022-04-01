# PublicationSubscriptionGenerator

1. Mod utilizare generator

    Pentru a genera un set de publicatii si subscriptii:
    - se creaza unui fisier yaml de configurare cu structura descrisa la punctul **2.**.
    - se ruleaza comanda `Generator.py -c <config file> -p <publications output file> -s <subscriptions output file>`
    Ex.: `Generator.py -c config.yaml -p Publications.txt -s Subscriptions.txt`

    **Generator.py** - scriptul care genereaza seturile de publicatii si subscriptii
    
    **Generator.py -h**
    
```
usage: Generator.py [-h] -c CONFIG [-p PUBLICATIONS] [-s SUBSCRIPTIONS]

Tool for generating publications and subscriptions

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to yaml configuration file
  -p PUBLICATIONS, --publications PUBLICATIONS
                        File path where publications will be stored. Defaults to 'Publications.txt'
  -s SUBSCRIPTIONS, --subscriptions SUBSCRIPTIONS
                        File path where subscriptions will be stored. Defaults to 'Publications.txt'
```

2. Structura fisier configurare. Un exemplu concret: **config.yaml**

```
# numarul de publicatii care vor fi generate
publications: int
# numarul de subscriptii care vor fi generate
subscriptions: int
# lista de campuri ale unei publicatii care se vor regasi si in subscriptii si diversi parametri pentru generare
fields:
  company:
    # Tipul de date al campului
    type: str
    # Valori posibile pentru campul "company"
    choices: list
    # Frecventa cu care se va regasi in subscriptii. Numarul de subscriptii care vor contine campul "company" va fi
    #     math.ceil(subscriptions * frequency)
    # Ar trebui sa fie specificata o valoare mai mica decat 1.0
    frequency: double
    # Frecventa minima a operatorului "=" pentru campul "company" in subscriptiile generate
    # Ar trebui sa fie specificata o valoare mai mica decat 1.0
    equals: double
    # Operatori acceptati in subscriptii pentru campul "company"
    operators: list
  value:
    type: str
    # Valoarea MINIMA acceptata penru campul "value" de tip double
    min: double
    # Valoare MAXIMA accceptata pentru campul "value" de tip double
    max: double
    frequency: double
    operators: list
  drop:
    type: str
    min: double
    max: double
    frequency: double
    operators: list
  variation:
    type: str
    min: double
    max: double
    frequency: double
    operators: list
  date:
    type: str
    choices: list
    frequency: double
    operators: list
```
