## Auction house parser

Parses a log file from an auction house and returns information about each auction.

### Instructions

```python
from auctionhouse import Parser

parser = Parser()
result = parser.parse('/path/to/input.txt')
for line in result:
    print(line)
```

### Tests

Tests can be run with:

```
python -m unittest
```
