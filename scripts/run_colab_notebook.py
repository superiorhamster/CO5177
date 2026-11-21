"""Run a notebook on an owned T4, collect results immediately, then release the VM."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('notebook', type=Path)
    parser.add_argument('--kind', choices=['text', 'image'], required=True)
    parser.add_argument('--session', required=True)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--collector', type=Path, default=Path(__file__).with_name('collect_notebook_results.py'))
    args = parser.parse_args()
    directory = args.notebook.resolve().parent
    base = ['colab', '--config', str(args.config)]
    def run(arguments, **kwargs):
        print('Colab:', arguments[0], flush=True)
        subprocess.run(base + arguments, check=True, **kwargs)
    def retry(arguments, output_path=None):
        for attempt in range(3):
            try:
                if output_path:
                    with output_path.open('wb') as stream:
                        run(arguments, stdin=subprocess.DEVNULL, stdout=stream)
                else:
                    run(arguments)
                return
            except subprocess.CalledProcessError:
                if attempt == 2:
                    raise
                time.sleep(3)
    created = False
    state = {'status': 'starting', 'session': args.session, 'kind': args.kind}
    try:
        run(['new', '-s', args.session, '--gpu', 'T4'])
        created = True
        state['status'] = 'executing'
        (directory / 'driver.json').write_text(json.dumps(state, indent=2))
        with (directory / 'execution.log').open('w') as log:
            run(['exec', '-s', args.session, '--env', 'NOTEBOOK_SMOKE=0', '--timeout', '0', '-f', str(args.notebook.resolve())],
                stdout=log, stderr=subprocess.STDOUT)
        output = args.notebook.with_name(args.notebook.stem + '_output.ipynb')
        notebook = json.loads(output.read_text())
        errors = [(i, out.get('ename'), out.get('evalue')) for i, cell in enumerate(notebook['cells'])
                  for out in cell.get('outputs', []) if out.get('output_type') == 'error']
        if errors:
            raise RuntimeError(f'Notebook cell errors: {errors}')
        state['status'] = 'collecting'
        (directory / 'driver.json').write_text(json.dumps(state, indent=2))
        run(['exec', '-s', args.session, '--env', f'ARCHIVE_KIND={args.kind}', '--env', 'ARCHIVE_MODE=full',
             '--timeout', '0', '-f', str(args.collector.resolve())])
        retry(['download', '-s', args.session, f'/content/oxford-{args.kind}-full.zip', str(directory / 'artifacts.zip')])
        retry(['ssh', '-s', args.session, '--', 'cat', f'/content/oxford-{args.kind}-selected-checkpoints.zip'],
              directory / 'selected-checkpoints.zip')
        state['status'] = 'passed'
    except Exception as error:
        state.update(status='failed', error=str(error))
        raise
    finally:
        if created:
            try:
                run(['stop', '-s', args.session])
                state['vm_released'] = True
            except subprocess.CalledProcessError:
                state['vm_released'] = False
        (directory / 'driver.json').write_text(json.dumps(state, indent=2) + '\n')


if __name__ == '__main__':
    main()
