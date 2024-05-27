# Setup (Miniconda)

```python
conda create -n rs python=3.7.0
conda activate rs
pip install -r requirements.txt
```

# Esempio di utilizzo

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

### Seleziona una particolare funzione di costo (1, 2, 3)
python main.py -cf=1
```