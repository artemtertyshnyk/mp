import pandas as pd
import numpy as np
import json

def normalize_frequencies():
    df = pd.read_csv('unigram_freq.csv')
    
    frequencies = df['count'].values
    
    min_freq = np.min(frequencies)
    max_freq = np.max(frequencies)
    
    normalized = 1 + ((frequencies - min_freq) * (10000 - 1)) / (max_freq - min_freq)
    
    normalized = normalized.round().astype(int).tolist()
    
    freq_dict = dict(zip(df['word'], normalized))
    
    with open('word_frequencies.json', 'w') as f:
        json.dump(freq_dict, f, indent=2)
    
    return freq_dict

normalize_frequencies()