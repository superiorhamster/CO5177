"""Validate notebook structure and recompute reported scores from exported predictions."""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import math
import re
import zipfile
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [ROOT / 'ipynb/text/sentimentanalysis.ipynb',
             ROOT / 'ipynb/image/intel_image_classification_trained.ipynb']


def read_csv(path):
    with Path(path).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def metrics(rows, truth_key, prediction_key, labels):
    matrix = Counter((int(row[truth_key]), int(row[prediction_key])) for row in rows)
    assert rows and all(a in labels and b in labels for a, b in matrix)
    correct = sum(matrix[label, label] for label in labels)
    f1s = []
    for label in labels:
        tp = matrix[label, label]
        actual = sum(value for (a, _), value in matrix.items() if a == label)
        predicted = sum(value for (_, b), value in matrix.items() if b == label)
        f1s.append(2 * tp / (actual + predicted) if actual + predicted else 0.)
    return correct / len(rows), sum(f1s) / len(labels), matrix


def report_metrics(matrix, labels):
    precision, recall, f1s, support = [], [], [], []
    for label in labels:
        true_positive = matrix[label, label]
        actual = sum(count for (left, _), count in matrix.items() if left == label)
        predicted = sum(count for (_, right), count in matrix.items() if right == label)
        precision.append(true_positive / predicted if predicted else 0.)
        recall.append(true_positive / actual if actual else 0.)
        f1s.append(2 * true_positive / (actual + predicted) if actual + predicted else 0.)
        support.append(actual)
    return {'macro_precision': sum(precision) / len(labels), 'macro_recall': sum(recall) / len(labels),
            'weighted_f1': sum(value * count for value, count in zip(f1s, support)) / sum(support)}


def check_per_class(rows, matrix, classes, f1_key):
    """Recompute each class, including support, independently of exported reports."""
    exported = {row['class_name']: row for row in rows}
    assert len(exported) == len(rows) == len(classes)
    assert set(exported) == set(classes.values())
    for label, name in classes.items():
        true_positive = matrix[label, label]
        actual = sum(count for (left, _), count in matrix.items() if left == label)
        predicted = sum(count for (_, right), count in matrix.items() if right == label)
        expected = {'precision': true_positive / predicted if predicted else 0.,
                    'recall': true_positive / actual if actual else 0.,
                    f1_key: 2 * true_positive / (actual + predicted) if actual + predicted else 0.,
                    'support': actual}
        for metric, value in expected.items():
            assert math.isclose(value, float(exported[name][metric]), abs_tol=1e-12), (name, metric)


def check_matrix(path, matrix, labels):
    with path.open() as stream:
        exported = list(csv.reader(stream))
    assert exported[0][1:] == [str(label) for label in labels]
    assert [row[0] for row in exported[1:]] == [str(label) for label in labels]
    assert [[matrix[left, right] for right in labels] for left in labels] == [[int(value) for value in row[1:]] for row in exported[1:]]


def check_notebook(path, executed=False):
    notebook = json.loads(path.read_text())
    headings, code_count = [], 0
    for index, cell in enumerate(notebook['cells']):
        source = ''.join(cell['source'])
        if cell['cell_type'] == 'markdown':
            match = re.match(r'# \((\d+)\)', source)
            if match:
                headings.append(int(match[1]))
        else:
            code_count += 1
            ast.parse(source, filename=f'{path.name}:cell{index}')
            assert not any(output.get('output_type') == 'error' for output in cell['outputs']), (path, index)
            assert not re.search(r'fallback_(12_runs|cm)', source), (path, index)
    assert headings == list(range(1, 12)), (path, headings)
    if path.name.startswith('intel_'):
        code = '\n'.join(''.join(c['source']) for c in notebook['cells'] if c['cell_type'] == 'code')
        tree = ast.parse(code)
        config = next(node.value for node in tree.body if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == 'cfg' for target in node.targets))
        keywords = {entry.arg: entry.value for entry in config.keywords}
        assert keywords['resume'].value is False
        assert keywords['dataset_version'].value == 2
        assert 'NOTEBOOK_SMOKE' in ast.unparse(keywords['smoke_test'])
    if executed:
        execution = notebook['metadata']['verified_execution']
        assert execution['status'] == 'passed' and execution['code_cells'] == code_count
        assert not execution['smoke_test']
        assert execution['cells_sha256'] == hashlib.sha256(json.dumps(notebook['cells'], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    print(f'{path.relative_to(ROOT)}: 11 sections, {code_count} code cells, AST/output checks passed')


def check_text(directory):
    run = json.loads((directory / 'run.json').read_text())
    groups = defaultdict(list)
    for row in read_csv(directory / 'predictions.csv'):
        groups[row['architecture'], row['dataset']].append(row)
    expected = {(architecture, dataset) for architecture in run['architectures'] for dataset in ('Base', 'Augmented')}
    assert len(expected) == 12 and set(groups) == expected
    test = [row for row in read_csv(directory / 'split_manifest.csv') if row['split'] == 'Test']
    expected_ids = [row['sample_id'] for row in test]
    assert len(set(expected_ids)) == len(expected_ids)
    summaries = {(row['architecture'], row['dataset']): row for row in read_csv(directory / 'summary.csv')}
    assert set(summaries) == expected
    per_class = read_csv(directory / 'per_class_metrics.csv')
    experiment_paths = {}
    for path in directory.glob('models/*/*/training_summary.json'):
        value = json.loads(path.read_text())
        experiment_paths[value['architecture'], value['dataset']] = path.parent
    for key, rows in groups.items():
        assert [row['sample_id'] for row in rows] == expected_ids
        assert [row['true_label'] for row in rows] == [row['label'] for row in test]
        accuracy, f1, matrix = metrics(rows, 'true_label', 'predicted_label', [-1, 0, 1])
        assert math.isclose(accuracy, float(summaries[key]['accuracy']), abs_tol=1e-12)
        assert math.isclose(f1, float(summaries[key]['macro_f1']), abs_tol=1e-12)
        assert int(summaries[key]['support']) == len(test)
        for metric, value in report_metrics(matrix, [-1, 0, 1]).items():
            assert math.isclose(value, float(summaries[key][metric]), abs_tol=1e-12)
        check_matrix(experiment_paths[key] / 'confusion_counts.csv', matrix, [-1, 0, 1])
        check_per_class([row for row in per_class if (row['architecture'], row['dataset']) == key],
                        matrix, {-1: 'negative', 0: 'neutral', 1: 'positive'}, 'f1-score')
    for training in directory.glob('models/*/*/training_summary.json'):
        value = json.loads(training.read_text())
        if value['history']:
            assert len(value['history']) == len(read_csv(training.parent / 'history.csv'))
            if run['fit_mode'] == 'fixed_configuration':
                expected_epochs = run['epochs']['phobert' if value['architecture'] == 'PhoBERT-base-v2' else 'neural']
                assert len(value['history']) == expected_epochs
                assert value['selected_epoch'] == expected_epochs
                assert not any('val_macro_f1' in row for row in value['history'])
    verification = json.loads((directory / 'verification.json').read_text())
    assert verification['status'] == 'passed' and verification['runs'] == 12
    assert verification['checkpoint_reload'] == 'passed' and verification['explanation_weights_unchanged']
    print(f'Text: all 12 runs recomputed from {len(expected_ids)} shared test IDs')


def check_image(directory):
    manifest = read_csv(directory / 'split_manifest.csv')
    test = [row for row in manifest if row['split'] == 'test']
    classes = dict(enumerate(json.loads((directory / 'dataset_source.json').read_text())['class_names']))
    summary = {row['model']: row for row in read_csv(directory / 'model_comparison.csv')}
    assert set(summary) == {'mobilenet_v3_small', 'vit_b_16'}
    for name, values in summary.items():
        per_class = read_csv(directory / name / 'per_class_metrics.csv')
        split_metrics = {row['split']: row for row in read_csv(directory / name / 'overall_metrics.csv')}
        assert set(split_metrics) == {'train', 'val', 'test'}
        for split, exported in split_metrics.items():
            records = read_csv(directory / name / f'{split}_predictions.csv')
            expected = [row for row in manifest if row['split'] == split]
            assert len({row['sample_id'] for row in records}) == len(records)
            assert [row['sample_id'] for row in records] == [row['sample_id'] for row in expected]
            assert [row['label'] for row in records] == [row['label'] for row in expected]
            accuracy, f1, matrix = metrics(records, 'label', 'prediction', list(classes))
            expected_metrics = {'accuracy': accuracy, 'macro_f1': f1, 'support': len(records),
                                **report_metrics(matrix, list(classes))}
            for metric, value in expected_metrics.items():
                assert math.isclose(value, float(exported[metric]), abs_tol=1e-12), (name, split, metric)
            check_per_class([row for row in per_class if row['split'] == split], matrix, classes, 'f1')
            assert all(row['true_class'] == classes[int(row['label'])]
                       and row['predicted_class'] == classes[int(row['prediction'])] for row in records)
        rows = read_csv(directory / name / 'test_predictions.csv')
        assert [row['sample_id'] for row in rows] == [row['sample_id'] for row in test]
        assert [row['label'] for row in rows] == [row['label'] for row in test]
        accuracy, f1, matrix = metrics(rows, 'label', 'prediction', list(range(6)))
        assert math.isclose(accuracy, float(values['accuracy']), abs_tol=1e-12)
        assert math.isclose(f1, float(values['macro_f1']), abs_tol=1e-12)
        for metric, value in report_metrics(matrix, list(range(6))).items():
            assert math.isclose(value, float(values[metric]), abs_tol=1e-12)
        with (directory / name / 'confusion_counts.csv').open() as stream:
            exported = list(csv.reader(stream))[1:]
        assert [[matrix[i, j] for j in range(6)] for i in range(6)] == [[int(v) for v in row[1:]] for row in exported]
    assert json.loads((directory / 'verification.json').read_text())['status'] == 'passed'
    print(f'Image: both models recomputed from {len(test)} shared test IDs')


def check_report_links():
    class References(HTMLParser):
        def __init__(self):
            super().__init__()
            self.ids, self.links = [], []
        def handle_starttag(self, tag, attributes):
            attrs = dict(attributes)
            if 'id' in attrs:
                self.ids.append(attrs['id'])
            for name in ('href', 'src'):
                if attrs.get(name):
                    self.links.append(attrs[name])
    for name in ('text', 'image'):
        page = ROOT / 'pages/projects' / f'{name}.html'
        parsed = References()
        parsed.feed(page.read_text(encoding='utf-8-sig'))
        assert len(parsed.ids) == len(set(parsed.ids)), ('Duplicate IDs', page)
        for reference in parsed.links:
            url = urlsplit(reference)
            if url.scheme or url.netloc:
                continue
            target = (page.parent / unquote(url.path)).resolve() if url.path else page
            assert target.exists(), (page, reference)
            assert not target.name.endswith(('.pt', '.safetensors', '.joblib'))
            if url.fragment and target.suffix == '.html':
                other = References()
                other.feed(target.read_text(encoding='utf-8-sig'))
                assert unquote(url.fragment) in other.ids, (page, reference)
        print(f'{name} report: local links/assets/fragments passed; IDs are unique')


def check_checkpoint_archive(directory):
    archive_path = directory.parents[1] / 'selected-checkpoints.zip'
    expected = json.loads((directory / 'model_files.json').read_text())
    assert expected, 'No checkpoint fingerprints exported'
    with zipfile.ZipFile(archive_path) as archive:
        for entry in expected:
            info = archive.getinfo(entry['file'])
            assert info.file_size == entry['bytes']
            digest = hashlib.sha256()
            with archive.open(info) as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(block)
            assert digest.hexdigest() == entry['sha256'], entry['file']
    print(f'{archive_path}: {len(expected)} checkpoint/preprocessor SHA-256 checks passed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--text-results', type=Path)
    parser.add_argument('--image-results', type=Path)
    parser.add_argument('--require-executed', action='store_true')
    parser.add_argument('--verify-checkpoints', action='store_true')
    args = parser.parse_args()
    for path in NOTEBOOKS:
        check_notebook(path, args.require_executed)
        if args.require_executed:
            assert path.read_bytes() == (ROOT / 'pages/notebooks' / path.name).read_bytes()
    if args.text_results:
        check_text(args.text_results)
    if args.image_results:
        check_image(args.image_results)
    if args.verify_checkpoints:
        for directory in (args.text_results, args.image_results):
            if directory:
                check_checkpoint_archive(directory)
    if args.require_executed:
        check_report_links()


if __name__ == '__main__':
    main()
