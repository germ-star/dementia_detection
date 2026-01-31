import re
import pandas as pd
from collections import Counter

def augment_complete(text):
    """
    handle all CHAT codes, use the temp markers and then convert
    """
    
    
    # all 3 different PAUSES we have in the transcripts (.) (..) (...)
    text = re.sub(r'\(\.\.\.+\)', ' __LONGPAUSE__ ', text)
    text = re.sub(r'\(\.\.\)', ' __MEDIUMPAUSE__ ', text)
    text = re.sub(r'\(\.\)', ' __SHORTPAUSE__ ', text)
    
    # Fillers: &-uh, &-um, &-hm, &-you_know
    text = re.sub(r'&-uh\b', ' __FILLER__ ', text, flags=re.IGNORECASE)
    text = re.sub(r'&-um\b', ' __FILLER__ ', text, flags=re.IGNORECASE)
    text = re.sub(r'&-hm\b', ' __FILLER__ ', text, flags=re.IGNORECASE)
    text = re.sub(r'&-you_know\b', ' __FILLER__ ', text, flags=re.IGNORECASE)
    text = re.sub(r'&-\w+', ' __FILLER__ ', text)
    
    # fragments: &+s, &+w, &+th
    text = re.sub(r'&\+\w+', ' __FRAGMENT__ ', text)
    
    # Repetition: [/] [//] [///]
    text = re.sub(r'\[/+\]', ' __REPEAT__ ', text)
    
    # Incomplete common words: dryin(g), fallin(g)
    text = re.sub(r'\b\w+\([^)]+\)', ' __INCOMPLETE__ ', text)
    
    # Trailing: +... +..
    text = re.sub(r'\+\.\.\.+', ' __TRAILING__ ', text)
    text = re.sub(r'\+\.\.', ' __TRAILING__ ', text)
    
    # Interruption: +//. 
    text = re.sub(r'\+//\.', ' __RESTART__ ', text)
    text = re.sub(r'\+/\.?', '', text)
    
   
    # all the remaining codes were removed from the transcripts as they provide noise.

    text = re.sub(r'\[:[^\]]+\]', '', text)      # [: stool]
    text = re.sub(r'\[\+[^\]]*\]', '', text)     # [+ exc]
    text = re.sub(r'\[\*[^\]]*\]', '', text)     # [* s:r]
    text = re.sub(r'\[=![^\]]*\]', '', text)     # [=! action]
    text = re.sub(r'\[\?[^\]]*\]', '', text)     # [?]
    text = re.sub(r'\[[^\]]*\]', '', text)       # any other remaining [...]
    
    text = re.sub(r'<([^>]+)>', r'\1', text)     
    
    text = re.sub(r'@[a-z]', '', text)           # @u, @o
    text = re.sub(r'\x15+', '', text)            # Timestamps
    text = re.sub(r'\d+_\d+', '', text)
    text = re.sub(r'&=\w+', '', text)            # &=laughs
    text = re.sub(r'&\*\w+:\w+', '', text)       # &*INV:okay
    text = re.sub(r'&\S+', '', text)             # any remaining &...
    
    text = re.sub(r'\([^)]*\)', '', text)        # remaining (...)
    text = re.sub(r'\.{2,}', ' __TRAILING__ ', text)  # ... or ..
    
    # now, we convert temp markers  we decided to keep to special tokens
    
    text = text.replace('__FILLER__', '[FILLER]')
    text = text.replace('__FRAGMENT__', '[FRAGMENT]')
    text = text.replace('__REPEAT__', '[REPEAT]')
    text = text.replace('__INCOMPLETE__', '[INCOMPLETE]')
    text = text.replace('__SHORTPAUSE__', '[SHORT_PAUSE]')
    text = text.replace('__MEDIUMPAUSE__', '[MEDIUM_PAUSE]')
    text = text.replace('__LONGPAUSE__', '[LONG_PAUSE]')
    text = text.replace('__TRAILING__', '[TRAILING]')
    text = text.replace('__RESTART__', '[RESTART]')
    
    # clearing the whitespace
    
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

    
   
