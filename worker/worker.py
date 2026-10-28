"""Small NDVI batch demonstration; input values are supplied as a JSON array."""
import json
import os
from pathlib import Path

source = Path(os.getenv('NDVI_INPUT', '/data/ndvi-input.json'))
output = Path(os.getenv('NDVI_OUTPUT', '/data/results/ndvi-summary.json'))
values = json.loads(source.read_text())
if not isinstance(values, list) or not values or any(not isinstance(v, (int, float)) for v in values):
    raise ValueError('Input must be a non-empty JSON array of numeric NDVI values')
output.parent.mkdir(parents=True, exist_ok=True)
summary = {'count': len(values), 'mean_ndvi': sum(values) / len(values)}
output.write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
