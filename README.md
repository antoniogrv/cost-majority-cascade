# Cost Majority Cascade

Questa repository esemplifica un [processo di diffusione](https://escholarship.org/uc/item/6r76d0rg) in una rete pesata combinando tre algoritmi di spreading, molteplici funzioni di costo e threshold differenti, come progetto per il corso di Reti Sociali all'Università di Salerno.

### Installazione

Si consiglia l'utilizzo di [Miniconda](https://docs.anaconda.com/free/miniconda/index.html).

```python
conda create -n rs python=3.7.0
conda activate rs
pip install -r requirements.txt
```

### Esempio di utilizzo

```python
main.py [-h] [-g] [-v] [-s] [-k THRESHOLD] [-e EDGES] [-c CIRCLES] [-cf {1,2,3}] [-sf {1,2,3}] [-a {1,2,3}]
```

```python
### Esegue il processo di diffusione con i parametri di default
python main.py

### Abilita la modalità verbosa
python main.py -v

### Abilita la stampa di debug del grafo e salva i risultati
python main.py -g -s

### Seleziona ed utilizza un grafo personalizzato
python main.py -e=networks/sample_networks/0.edges -c=networks/sample_networks/0.circles

### Seleziona uno specifico algoritmo di individuazione del seed set
python main.py -a=1 # Cost-Seeds-Greedy
python main.py -a=2 # WTSS
python main.py -a=3 # My-Seeds

### Seleziona specifiche funzioni di costo e funzioni submodulari (es. 1, 2, 3)
python main.py -cf=1 # Random Costs
python main.py -sf=2 # Second Submodular Function (ref. Costs-Seeds-Greedy)
python main.py -cf=1 -sf=3 # Random Costs & Second Submodular Function
```