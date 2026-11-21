"""Run on Colab after a successful notebook; export evidence without publishing weights."""
import hashlib
import json
import os
import zipfile
from pathlib import Path

kind = os.environ['ARCHIVE_KIND']
mode = os.environ['ARCHIVE_MODE']
if kind == 'text':
    source = sorted(Path('/content/vlsp_oxford_results').glob(mode + '-*'))[-1]
else:
    source = Path('/content/intel_transfer_results') / mode
verification = json.loads((source / 'verification.json').read_text())
assert verification['status'] == 'passed'
assert verification['smoke_test'] == (mode == 'smoke')
model_files = []
for path in source.rglob('*'):
    if path.is_file() and (path.name == 'best.pt' or path.suffix in {'.safetensors', '.joblib'}):
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(block)
        model_files.append({'file': path.relative_to(source).as_posix(), 'sha256': digest.hexdigest(), 'bytes': path.stat().st_size})
(source / 'model_files.json').write_text(json.dumps(model_files, indent=2))
target = Path('/content') / f'oxford-{kind}-{mode}.zip'
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in source.rglob('*'):
        if path.is_file() and path.suffix in {'.csv', '.json', '.png'} and 'pretrained' not in path.relative_to(source).parts:
            archive.write(path, path.relative_to(source.parent))
print('Evidence:', source, '->', target, '| bytes', target.stat().st_size)
if mode == 'full':
    checkpoint_target = Path('/content') / f'oxford-{kind}-selected-checkpoints.zip'
    with zipfile.ZipFile(checkpoint_target, 'w', zipfile.ZIP_DEFLATED, compresslevel=1) as archive:
        for path in source.rglob('*'):
            if not path.is_file():
                continue
            relative = path.relative_to(source)
            if kind == 'text':
                selected = relative.parts[0] == 'models'
            else:
                selected = relative.parts[0] in {'mobilenet_v3_small', 'vit_b_16'} and path.name in {
                    'best.pt', 'training_summary.json', 'history.csv', 'stage_results.csv'}
                selected = selected or path.name in {'config.json', 'experiment.json', 'dataset_source.json'}
            if selected:
                archive.write(path, relative)
    print('Selected checkpoints:', checkpoint_target, '| bytes', checkpoint_target.stat().st_size)
