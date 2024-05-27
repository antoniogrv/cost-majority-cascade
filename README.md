# Setup (Miniconda)

```python
conda create -n rs python=3.7.0
conda activate rs
pip install -r requirements.txt
```

# Esempio di utilizzo

```python
python main.py [-h] [-g] [-v] [-k THRESHOLD] [-e EDGES] [-c CIRCLES] [-cf {1,2,3}] [-sf {1,2,3}] [-a {1,2,3}]
```

```python
### Esegue il runner con i parametri di default
python main.py

### Abilita la modalità verbosa
python main.py -v

### Abilita la stampa di debug del grafo
python main.py -g

### Seleziona ed utilizza un grafo personalizzato
python main.py --edges=sample_networks/0.edges --circles=sample_networks/0.circles

### Seleziona uno specifico algoritmo di individuazione del seed set
python main.py -a=1 # Cost-Seeds-Greedy
python main.py -a=2 # WTSS
python main.py -a=3 # My-Seeds

### Seleziona specifiche funzioni di costo e funzioni submodulari (es. 1, 2, 3)
python main.py -cf=1
python main.py -sf=2
python main.py -cf=1 -sf=3
```