"""Exercise leakage/lineage edge cases using the functions embedded in the Text notebook."""
from __future__ import annotations

import json
import re
import tempfile
import unicodedata
from itertools import groupby
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold


def main(notebook_path):
    notebook = json.loads(Path(notebook_path).read_text())
    sources = [''.join(cell['source']) for cell in notebook['cells'] if cell['cell_type'] == 'code']
    normalization = next(source for source in sources if 'def audit_inputs(' in source).split('cleaned, audit =')[0].split('assert all(sha256_file')[0]
    splitting = next(source for source in sources if 'def partition_frames(' in source).split('lineage_path =')[0]
    namespace = dict(np=np, pd=pd, re=re, unicodedata=unicodedata, groupby=groupby,
                     StratifiedGroupKFold=StratifiedGroupKFold, SEED=42, LABELS=[-1, 0, 1])
    exec(normalization, namespace)
    exec(splitting, namespace)

    def frame(rows, name):
        value = pd.DataFrame(rows, columns=['label', 'text'])
        value['row'] = np.arange(len(value))
        value['sample_id'] = name + '-' + value.row.astype(str)
        return value

    base = frame([(label, f'{name} văn bản {index}') for label, name in [(-1, 'xấu'), (0, 'thường'), (1, 'tốt')]
                  for index in range(15)], 'base')
    augmented = frame([(row.label, row.text + suffix) for row in base.itertuples()
                       for suffix in ['', ' bản phái sinh']], 'augmented')
    test = frame([(label, f'kiểm tra riêng {name}') for label, name in [(-1, 'xấu'), (0, 'thường'), (1, 'tốt')]], 'test')
    raw = {'Base': base, 'Augmented': augmented, 'Test': test}
    cleaned, _ = namespace['audit_inputs'](raw)
    fixed, validation = namespace['partition_frames'](cleaned, raw, None)
    assert validation is None and len(fixed['Base']) == 45 and len(fixed['Augmented']) == 90
    mapping = pd.DataFrame({'aug_row': augmented.row, 'base_row': np.repeat(base.row.to_numpy(), 2)})
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / 'lineage.csv'
        mapping.to_csv(path, index=False)
        grouped, validation = namespace['partition_frames'](cleaned, raw, path)
        assert set(validation.label) == {-1, 0, 1}
        assert len(validation) == 9 and len(grouped['Base']) == 36 and len(grouped['Augmented']) == 72
        held_parents = set(validation.row)
        assert not set(grouped['Augmented'].row.map(mapping.set_index('aug_row').base_row)) & held_parents
        for fit in grouped.values():
            assert not set(fit.clean_key) & set(validation.clean_key)
        mapping.iloc[:-1].to_csv(path, index=False)
        try:
            namespace['read_lineage'](path, raw)
        except ValueError:
            pass
        else:
            raise AssertionError('Incomplete lineage was accepted')
    if namespace.get('PREPROCESSING_VERSION') == 'vlsp-eda-v2':
        assert namespace['normalize_text']('Ko tốt :)) ❤️') == 'Ko tốt :)) ❤️'
        assert namespace['normalize_text']('  KHÔNG   tốt! ') == 'KHÔNG tốt!'
    # Leakage after normalization must be removed from fit, while original test is retained.
    raw['Test'] = frame([(0, ' KO  tốt '), (-1, 'mẫu test xấu'), (1, 'mẫu test tốt')], 'test')
    raw['Base'] = pd.concat([base, frame([(0, 'ko tốt')], 'overlap')], ignore_index=True)
    cleaned, audit = namespace['audit_inputs'](raw)
    assert len(cleaned['Test']) == 3
    assert not cleaned['Base'].text.eq('ko tốt').any()
    assert audit.loc['Base', 'normalized_overlap_with_test'] == 1
    raw['Test'].loc[0, 'text'] = '   '
    try:
        namespace['audit_inputs'](raw)
    except ValueError:
        pass
    else:
        raise AssertionError('Blank normalized test was accepted')
    print('Passed: fixed protocol, grouped validation, held-out descendants, incomplete lineage, normalized overlap and blank test.')


if __name__ == '__main__':
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'ipynb/text/sentimentanalysis.ipynb')
