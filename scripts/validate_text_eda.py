"""Recompute EDA truncation, TF-IDF coverage, and CBOW OOV/UNK tables against exported artifacts."""
from __future__ import annotations

import argparse
import csv
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
    expected_charts = [
        'eda_balance_audit.png',
        'eda_lengths_limits.png',
        'eda_signals_ngrams.png',
        'eda_feature_representations.png',
    ]
    assert source.get('charts') == expected_charts, source.get('charts')
    for chart in expected_charts:
        assert (directory / chart).is_file(), f'Missing EDA chart: {chart}'

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
        expected = {
            'median': quantile(lengths, 0.5),
            'p90': quantile(lengths, 0.9),
            'p95': quantile(lengths, 0.95),
            'p99': quantile(lengths, 0.99),
            'maximum': max(lengths),
            'truncated_documents': affected,
            'truncated_percent': 100 * affected / len(lengths),
            'tokens_removed': removed,
            'tokens_removed_percent': 100 * removed / sum(lengths),
        }
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

    for row in rows(directory / 'cbow_vocab_comparison.csv'):
        field = 'pretrained_oov_fraction' if 'Pretrained' in row['stage'] else 'vocab_unk_fraction'
        vals = [float(r[field]) for r in samples if r['dataset'] == row['dataset']]
        assert math.isclose(float(row['docs_affected_pct']), 100 * sum(v > 0 for v in vals) / len(vals), abs_tol=1e-9)
        assert math.isclose(float(row['mean_rate_pct']), 100 * sum(vals) / len(vals), abs_tol=1e-9)
        assert math.isclose(float(row['median_rate_pct']), 100 * quantile(vals, 0.5), abs_tol=1e-9)
        assert math.isclose(float(row['p90_rate_pct']), 100 * quantile(vals, 0.9), abs_tol=1e-9)

    policy = json.loads((directory / 'preprocessing_policy.json').read_text())
    assert policy['version'] == 'vlsp-eda-v4-compact'
    assert policy['eda_sources'] == source['sources']

    notebook_path = Path(__file__).resolve().parents[1] / 'ipynb/text/sentimentanalysis_eda.ipynb'
    notebook = json.loads(notebook_path.read_text())
    assert notebook['metadata']['verified_execution']['status'] == 'passed'
    assert notebook['metadata']['verified_execution']['runtime'] == 'CPU'
    assert not [o for c in notebook['cells'] for o in c.get('outputs', []) if o.get('output_type') == 'error']
    print('EDA passed: 4 charts, raw counts, sample IDs, truncation quantiles, TF-IDF coverage, CBOW comparison and CPU provenance.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    main(parser.parse_args().directory)
