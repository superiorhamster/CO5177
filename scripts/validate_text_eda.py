"""Recompute EDA truncation tables and check feature diagnostics against their exports."""
from __future__ import annotations
import argparse
import ast
import csv
import hashlib
import json
import math
from pathlib import Path


def rows(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def quantile(values, fraction):
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    left = int(position)
    return ordered[left] + (ordered[min(left + 1, len(ordered) - 1)] - ordered[left]) * (position - left)


def main(directory):
    source = json.loads((directory / 'source.json').read_text())
    assert source['cpu_only'] and source['test_usage'] == 'schema and text overlap only'
    samples = rows(directory / 'sample_token_diagnostics.csv')
    audit = {r['dataset']: r for r in rows(directory / 'raw_audit.csv')}
    for dataset in ('Base', 'Augmented'):
        group = [r for r in samples if r['dataset'] == dataset]
        assert len(group) == int(audit[dataset]['rows'])
        assert len({r['sample_id'] for r in group}) == len(group)
        for row in group:
            assert all(0 <= float(row[key]) <= 1 for key in ('pretrained_oov_fraction', 'vocab_unk_fraction'))
    for row in rows(directory / 'sequence_limits.csv'):
        field = 'cbow_length' if row['embedder'] == 'CBOW' else 'bpe_length'
        lengths = [int(r[field]) for r in samples if r['dataset'] == row['dataset']]
        limit = int(row['limit'])
        removed = sum(max(0, value - limit) for value in lengths)
        affected = sum(value > limit for value in lengths)
        expected = {'median': quantile(lengths, .5), 'p90': quantile(lengths, .9),
                    'p95': quantile(lengths, .95), 'p99': quantile(lengths, .99),
                    'maximum': max(lengths), 'truncated_documents': affected,
                    'truncated_percent': 100 * affected / len(lengths),
                    'tokens_removed': removed, 'tokens_removed_percent': 100 * removed / sum(lengths)}
        for key, value in expected.items():
            assert math.isclose(value, float(row[key]), abs_tol=1e-9), (row['dataset'], row['embedder'], key)
    denominators = {}
    for row in rows(directory / 'tfidf_diagnostics.csv'):
        count = int(audit[row['dataset']]['rows'])
        features, nnz = int(row['features']), int(row['nnz'])
        assert features <= int(row['max_features']) and 0 < nnz <= count * features
        assert math.isclose(float(row['sparsity']), 1 - nnz / (count * features), abs_tol=1e-12)
        assert int(row['dense_batch128_bytes']) == 128 * features * 4
        key = (row['dataset'], row['analyzer'])
        denominator = nnz / float(row['feature_occurrence_coverage'])
        if key in denominators:
            assert math.isclose(denominator, denominators[key], abs_tol=1e-6)
        denominators[key] = denominator
        assert 0 <= int(row['empty_documents']) < count
    policy = json.loads((directory / 'preprocessing_policy.json').read_text())
    assert policy['eda_sources'] == source['sources']
    notebook_path = Path(__file__).resolve().parents[1] / 'ipynb/text/sentimentanalysis_eda.ipynb'
    notebook = json.loads(notebook_path.read_text())
    code = ''.join(''.join(c['source']) for c in notebook['cells'] if c['cell_type'] == 'code')
    assert hashlib.sha256(code.encode()).hexdigest() == policy['eda_notebook_code_sha256']
    if policy['version'] == 'vlsp-eda-v3-six-raincloud':
        proof = json.loads((directory / 'raincloud_verification.json').read_text())
        assert proof['status'] == 'passed' and proof['runtime'] == 'CPU'
        assert proof['source_csv_sha256'] == hashlib.sha256((directory / 'sample_token_diagnostics.csv').read_bytes()).hexdigest()
        cell = next(''.join(c['source']) for c in notebook['cells'] if 'def plot_cbow_raincloud(' in ''.join(c['source']))
        function = next(node for node in ast.parse(cell).body if isinstance(node, ast.FunctionDef) and node.name == 'plot_cbow_raincloud')
        function_source = ast.get_source_segment(cell, function).strip() + '\n'
        assert hashlib.sha256(function_source.encode()).hexdigest() == proof['plot_function_sha256']
        summary = rows(directory / 'cbow-raincloud-summary.csv')
        assert len(summary) == 4
        for row in summary:
            values = [float(r[row['metric']]) for r in samples if r['dataset'] == row['dataset']]
            assert int(row['n']) == len(values) and int(row['display_points']) == min(1500, len(values))
            assert math.isclose(float(row['zero_fraction']), sum(v == 0 for v in values) / len(values))
            for field, fraction in [('q1', .25), ('median', .5), ('q3', .75)]:
                assert math.isclose(float(row[field]), quantile(values, fraction), abs_tol=1e-12)
        assert notebook['metadata']['visualization_smoke']['status'] == 'passed'
    else:
        assert notebook['metadata']['verified_execution']['runtime'] == 'CPU'
    assert not [o for c in notebook['cells'] for o in c.get('outputs', []) if o.get('output_type') == 'error']
    print('EDA passed: raw counts, sample IDs, all truncation quantiles/rates, TF-IDF sparsity/memory/coverage and policy provenance.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    main(parser.parse_args().directory)
