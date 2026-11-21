"""Bind a Colab output notebook to its executed source, log and verified artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tidy_outputs(notebook):
    """Keep evidence/epoch summaries; remove transient batch/download progress displays."""
    removed = 0
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        outputs = []
        for output in cell.get('outputs', []):
            data = output.get('data', {})
            if 'application/vnd.jupyter.widget-view+json' in data and not any(key in data for key in ['image/png', 'image/jpeg', 'text/html']):
                removed += 1
                continue
            if output.get('output_type') == 'stream':
                value = output['text']
                value = ''.join(value) if isinstance(value, list) else value
                lines = value.replace('\r', '\n').splitlines(keepends=True)
                filtered = [line for line in lines if line.strip() and not re.match(r'^\s*[^|\n]*\d{1,3}%\|.*\[[^]]+\]\s*$', line)]
                removed += len(lines) - len(filtered)
                value = ''.join(filtered)
                if not value:
                    continue
                output = {**output, 'text': value}
                if outputs and outputs[-1].get('output_type') == 'stream' and outputs[-1]['name'] == output['name']:
                    outputs[-1]['text'] += value
                    continue
            outputs.append(output)
        cell['outputs'] = outputs
    return removed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('log', type=Path)
    parser.add_argument('artifacts', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    original = json.loads(args.input.read_text())
    notebook = json.loads(args.output.read_text())
    assert [(c['cell_type'], c['source']) for c in original['cells']] == [(c['cell_type'], c['source']) for c in notebook['cells']]
    if args.destination.exists():
        current = json.loads(args.destination.read_text())
        assert [(c['cell_type'], c['source']) for c in current['cells']] == [(c['cell_type'], c['source']) for c in original['cells']], 'Notebook source changed after dispatch; preserve those edits before installing outputs.'
    assert not [(i, o) for i, c in enumerate(notebook['cells']) for o in c.get('outputs', []) if o.get('output_type') == 'error']
    code_count = sum(c['cell_type'] == 'code' for c in original['cells'])
    logged = re.findall(r'\[colab\] Executing cell (\d+)/(\d+)', args.log.read_text())
    assert logged == [(str(index), str(code_count)) for index in range(1, code_count + 1)]
    verification = json.loads((args.artifacts / 'verification.json').read_text())
    assert verification['status'] == 'passed' and not verification['smoke_test']
    environment = json.loads((args.artifacts / 'environment.json').read_text())
    assert 'T4' in environment['gpu']
    removed_progress = tidy_outputs(notebook)
    notebook['metadata']['verified_execution'] = {
        'status': 'passed', 'run_id': args.run_id, 'smoke_test': False,
        'completed_utc': datetime.fromtimestamp(args.output.stat().st_mtime, timezone.utc).isoformat(),
        'recorded_utc': datetime.now(timezone.utc).isoformat(),
        'source_sha256': digest(args.input), 'log_sha256': digest(args.log),
        'cells_sha256': hashlib.sha256(json.dumps(notebook['cells'], ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
        'code_cells': code_count, 'gpu': environment['gpu'], 'seed': 42,
        'verification_sha256': digest(args.artifacts / 'verification.json'),
        'output_cleanup': {'removed_progress_fragments': removed_progress, 'raw_output_preserved': args.output.name},
        'execution_method': 'colab CLI exec, sequential cells, clean kernel',
    }
    # The CLI does not record kernel execution counts. Preserve null rather than invent counts.
    args.destination.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + '\n')
    print('Recorded verified execution:', args.destination)


if __name__ == '__main__':
    main()
