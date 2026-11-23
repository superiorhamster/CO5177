"""Update the existing Vietnamese reports from a verified, full Colab run."""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import shutil
import struct
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from validate_oxford_notebooks import check_image, check_text, read_csv

ROOT = Path(__file__).resolve().parents[1]
IMAGE_NAMES = {'mobilenet_v3_small': 'MobileNetV3-Small', 'vit_b_16': 'ViT-B/16'}


def esc(value):
    return html.escape(str(value), quote=True)


def is_number(val):
    s = str(val).strip()
    if not s:
        return False
    s = s.rstrip('%').replace('.', '').replace(',', '.')
    try:
        float(s)
        return True
    except ValueError:
        return False


def table(headers, rows, caption, identifier=None):
    heading_id = f' id="{identifier}"' if identifier else ''
    return (f'<h3{heading_id}>{esc(caption)}</h3><div class="table-wrap report-table" tabindex="0" role="region" '
            f'aria-label="{esc(caption)}"><table><caption class="visually-hidden">{esc(caption)}</caption><thead><tr>'
            + ''.join(f'<th scope="col">{esc(value)}</th>' for value in headers) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<th scope="row">{esc(v)}</th>' if j == 0 else (f'<td class="report-number">{esc(v)}</td>' if is_number(v) else f'<td>{esc(v)}</td>')
                                       for j, v in enumerate(row)) + '</tr>' for row in rows)
            + '</tbody></table></div>')


def copy_evidence(source, destination):
    destination.mkdir(parents=True, exist_ok=True)
    for path in source.rglob('*'):
        if path.is_file() and path.suffix in {'.csv', '.json', '.png'} and 'pretrained' not in path.relative_to(source).parts:
            target = destination / path.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def figure(path, caption):
    if not path.is_file():
        raise FileNotFoundError(f'Missing figure: {path}')
    width, height = struct.unpack('>II', path.read_bytes()[16:24])
    relative = '../assets/' + path.relative_to(ROOT / 'pages/assets').as_posix()
    return (f'<figure class="report-figure report-figure-wide"><a class="figure-image-link" href="{relative}" '
            f'aria-label="Mở hình: {esc(caption)}"><img src="{relative}" width="{width}" height="{height}" '
            f'loading="lazy" decoding="async" alt="{esc(caption)}"></a><figcaption>{esc(caption)}</figcaption></figure>')


def resources(old, notebook_name, date):
    section = re.search(r'<section id="resources".*?</section>', old, re.S).group()
    colab = re.search(r'href="(https://colab.research.google.com/[^"]+)"', section)
    old_link = (f'<a class="text-link" href="{colab[1]}">Mở notebook trên Colab ↗</a> ' if colab else '')
    # Preserve PDF and video resource rows, including their actual statuses/URLs.
    remaining = re.search(r'(<div class="resource-item">\s*<div>\s*<h3>PDF report</h3>.*?)</section>', section, re.S)[1]
    return (f'<section id="resources" class="resources" aria-labelledby="resources-title">'
            f'<div class="compact-heading"><h2 id="resources-title">Tài liệu bài tập</h2>'
            f'<p>Notebook có output Run all mới trên Colab T4 ngày {esc(date)}. Colab mở notebook từ nhánh main trên GitHub.</p></div>'
            f'<div class="resource-item"><div><h3>Notebook</h3><p>Đủ 11 mục theo mẫu Oxford Pets; output và kết luận từ lần chạy mới.</p></div>'
            f'<div class="resource-actions">{old_link}<a class="text-link" href="../notebooks/{notebook_name}" download>'
            f'Tải notebook có output (.ipynb)</a></div></div>{remaining}</section>')


def section(identifier, title, body, step):
    return (f'<section id="{identifier}" class="pipeline-section" aria-labelledby="{identifier}-title">'
            f'<div class="pipeline-heading"><span class="step-number" aria-hidden="true">{step:02}</span>'
            f'<h2 id="{identifier}-title">{esc(title)}</h2></div>{body}</section>')


def run_date(run_id):
    return datetime.strptime(run_id, '%Y%m%dT%H%M%SZ').replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo('Asia/Ho_Chi_Minh')).strftime('%d/%m/%Y')


def install_report(kind, inner, old, asset_dir, notebook_name):
    page = ROOT / 'pages/projects' / f'{kind}.html'
    before_ids = set(re.findall(r'\bid="([^"]+)"', old))
    old_body = re.search(r'<main\b[^>]*>(.*?)</main>', old, re.S)[1]
    # Keep the existing member/requirements sidebar and previous/next report navigation.
    old_tail = old_body.split('</article>', 1)[1].strip()
    assert inner.endswith('</article></div>')
    inner = inner[:-len('</article></div>')] + '</article>\n' + old_tail
    formatted = '\n' + inner.replace('><', '>\n<') + '\n'
    new = re.sub(r'(<main\b[^>]*>).*?(</main>)', lambda m: m[1] + formatted + m[2], old, count=1, flags=re.S)
    after_ids = set(re.findall(r'\bid="([^"]+)"', new))
    assert before_ids <= after_ids, ('Lost anchors', before_ids - after_ids)
    page.write_text(new)
    source_nb = ROOT / 'ipynb' / kind / notebook_name
    shutil.copy2(source_nb, ROOT / 'pages/notebooks' / notebook_name)
    metadata = json.loads((asset_dir / 'source.json').read_text())
    metadata['notebook_sha256'] = hashlib.sha256(source_nb.read_bytes()).hexdigest()
    (asset_dir / 'source.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')


def text_report(source, eda_source=None):
    if not (source / 'run.json').is_file():
        subs = sorted(source.glob('full-*/run.json'))
        if subs:
            source = subs[-1].parent
    check_text(source)
    metadata = json.loads((source / 'run.json').read_text())
    if metadata.get('preprocessing', {}).get('version') in {'vlsp-eda-v2','vlsp-eda-v3-six-raincloud'} and eda_source is None:
        raise ValueError('Pipeline v2 cần --eda-results để đồng bộ bằng chứng EDA CPU.')
    assert not metadata['smoke_test']
    run_id = metadata['run_id']
    date = run_date(run_id)
    run_count = 2 * len(metadata['architectures'])
    six = run_count == 6
    destination = ROOT / 'pages/assets/vlsp-sentiment/oxford' / run_id
    copy_evidence(source, destination)
    (destination / 'source.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
    eda_destination = None
    if eda_source is not None:
        assert metadata['preprocessing']['version'] in {'vlsp-eda-v2','vlsp-eda-v3-six-raincloud'}
        eda_info = json.loads((eda_source / 'source.json').read_text())
        assert eda_info['cpu_only'] and eda_info['sources'] == metadata['preprocessing']['eda_sources']
        eda_destination = ROOT / 'pages/assets/vlsp-sentiment/eda-v2' / run_id
        copy_evidence(eda_source, eda_destination)
    rows = read_csv(source / 'summary.csv')
    best = max(rows, key=lambda r: float(r['macro_f1']))
    audit = {r['split']: r for r in read_csv(source / 'data_audit.csv')}
    deltas = read_csv(source / 'augmentation_delta.csv')
    old = (ROOT / 'pages/projects/text.html').read_text(encoding='utf-8-sig')
    hero = ('<nav class="breadcrumb" aria-label="Điều hướng phân cấp"><a href="../../index.html">Trang chủ</a> / Text</nav>'
            '<section class="project-hero" aria-labelledby="project-title"><div><p class="eyebrow">CO5177 / TEXT / SLIGHTSEEK</p>'
            '<h1 id="project-title">Phân tích cảm xúc tiếng Việt — sáu kiến trúc, 12 lượt chạy</h1>'
            '<p class="hero-description">VLSP v5; so sánh Base và Augmented với cùng test. Notebook theo 11 bước Oxford Pets, từ dữ liệu đến phân tích lỗi và giải thích.</p>'
            f'<p class="status-badge">Đã Run all trên Colab T4 · {date} · seed 42</p></div></section>')
    if six:
        hero = hero.replace('sáu kiến trúc, 12 lượt chạy','ba pipeline, 6 lượt chạy')
    raw_counts = [(name, audit[name]['input_rows'], metadata['sample_counts'][name]) for name in ['Base', 'Augmented', 'Test']]
    dataset = ('<p>Nguồn: <a href="https://www.kaggle.com/datasets/anhphmduy/vlsp-sentiment-dataset">VLSP Sentiment Dataset v5</a>. '
               'Nhãn −1: tiêu cực, 0: trung lập, +1: tích cực. Số dòng đọc từ CSV và số dòng sử dụng được báo riêng.</p>'
               + table(['Tập', 'Dòng gốc', 'Dòng sử dụng'], raw_counts, 'Quy mô dữ liệu')
               + '<h3 id="eda">Khám phá dữ liệu</h3>')
    if eda_destination is None:
        figures = [(destination / 'eda' / filename, caption) for filename, caption in [
            ('eda-raw-lengths.png', 'Độ dài văn bản gốc theo nhãn.'),
            ('eda-labels.png', 'Phân bố nhãn trước và sau kiểm toán.'),
            ('eda-cleaning-audit.png', 'Kiểm toán dữ liệu: các nhóm có thể chồng lấn.'),
            ('eda-lexical.png', 'Tín hiệu từ vựng và bigram theo lớp.'),
            ('eda-class-similarity.png', 'Cosine giữa centroid TF-IDF của Base fit.'),
            ('eda-tokenizers.png', 'Độ dài PyVi và PhoBERT BPE.')]]
    else:
        dataset += '<p>EDA chạy trước huấn luyện trên Colab CPU. Các phân tích theo nhãn chỉ dùng Base/Augmented; test chỉ phục vụ kiểm toán schema và giao văn bản.</p>'
        figures = [(eda_destination / filename, caption) for filename, caption in [
            ('labels.png', 'Phân bố nhãn của Base/Augmented gốc.'),
            ('lengths.png', 'ECDF độ dài văn bản gốc: đọc cùng đuôi dài và ví dụ câu.'),
            ('audit.png', 'Câu rỗng, bản sao và giao test theo văn bản; các nhóm có thể chồng lấn.'),
            ('signals.png', 'Tỷ lệ câu có phủ định, teencode, kéo dài và biểu tượng theo lớp; không suy nghĩa từ tần suất.'),
            ('rule-impacts.png', 'Tỷ lệ câu thay đổi so với gốc; mỗi quy tắc được thử cùng nền NFC/khoảng trắng.'),
            ('tfidf-coverage.png', 'Độ phủ lượt đặc trưng-văn bản theo giới hạn vocabulary, min_df=1; fit trên từng tập phát triển.'),
            ('tfidf-df.png', 'Document frequency theo analyzer word: đường tích lũy cho thấy tỷ trọng đặc trưng hiếm.'),
            ('token-limits.png', 'ECDF số từ PyVi và token PhoBERT BPE, gồm special tokens; vạch đỏ là giới hạn 300/256.'),
            ('cbow-coverage.png', 'Raincloud CBOW trên Base/Augmented gốc: nửa mật độ, median/IQR và điểm jitter; mật độ/box dùng toàn bộ dữ liệu, điểm tối đa 1.500/nhóm (seed 42), tỷ lệ bằng 0 ghi riêng.' if six else 'Phân bố OOV pretrained và UNK vocabulary từng câu; hai chỉ số không tương đương.')]]
        tfidf = [r for r in read_csv(eda_source / 'tfidf_diagnostics.csv') if r['min_df'] == '1' and r['analyzer'] == 'word+emoticon']
        dataset += table(['Tập', 'Giới hạn đặc trưng', 'Độ phủ (%)', 'Câu mất đặc trưng', 'Dense batch 128 (MB)'],
                         [[r['dataset'], r['max_features'], f'{100*float(r["feature_occurrence_coverage"]):.2f}', r['empty_documents'], f'{int(r["dense_batch128_bytes"])/1e6:.2f}'] for r in tfidf], 'Độ phủ TF-IDF trên dữ liệu phát triển')
        limits = [r for r in read_csv(eda_source / 'sequence_limits.csv') if (r['embedder'], r['limit']) in {('CBOW','300'),('PhoBERT','256')}]
        dataset += table(['Tập', 'Embedder', 'Giới hạn', 'Câu bị cắt (%)', 'Lượt token bị mất (%)', 'p99'],
                         [[r['dataset'],r['embedder'],r['limit'],f'{float(r["truncated_percent"]):.2f}',f'{float(r["tokens_removed_percent"]):.2f}',f'{float(r["p99"]):.1f}'] for r in limits], 'Mức mất thông tin do cắt chuỗi')
    for path, caption in figures:
        dataset += figure(path, caption)
    mode_label = {
        'fixed_configuration': 'cấu hình cố định, thiếu lineage',
        'grouped_validation': 'validation chung theo nhóm nguồn',
        'stratified_validation_no_lineage': 'stratified validation 20% theo từng tập (thiếu lineage)',
    }[metadata['fit_mode']]
    if metadata['fit_mode'] == 'fixed_configuration':
        mode_note = 'Thiếu lineage: không chia validation ngẫu nhiên từ Augmented; chạy 15 epoch CNN/LSTM, 6 epoch PhoBERT và dùng epoch cuối.'
    elif metadata['fit_mode'] == 'stratified_validation_no_lineage':
        mode_note = 'Tách 20% stratified validation riêng cho mỗi tập Base/Augmented (kiểm tra không trùng khóa chuẩn hóa với train/test) để bật early stopping theo validation macro-F1 (CNN + BiLSTM tối đa 15 epoch, patience 4; PhoBERT tối đa 6 epoch, patience 2). Giới hạn: thiếu lineage nên trên Augmented vẫn có thể tồn tại câu gần trùng giữa train và validation.'
    else:
        mode_note = 'Validation chung 20% theo nhóm nguồn; chọn checkpoint bằng validation macro-F1.'
    preparation = ('<p>Giữ văn bản gốc; chuẩn NFC và khoảng trắng. Không thay đồng loạt teencode/emoticon thành từ cảm xúc, không rút chữ kéo dài hoặc xóa ký hiệu. '
                   'Dữ liệu phát triển được kiểm toán lại về câu rỗng, trùng test và mâu thuẫn nhãn trước khi chia tập.</p>'
                   + table(['Embedder', 'Đầu vào và quyết định từ EDA', 'Giới hạn'], [
                       ('TF-IDF','Chữ thường; analyzer giữ emoticon; unigram/bigram, min_df=1, tối đa 20.000 đặc trưng sparse float32, đưa thẳng vào LinearSVC (không nén PCA/SVD).','Coverage trong tập fit không bảo đảm tăng F1; chỉ thử trên đặc trưng n-gram thưa.'),
                       ('CBOW','Chữ thường rồi PyVi; vocabulary 10.000 fit riêng, PAD/UNK, embedding trainable độc lập, masking/packing, tối đa 300 từ.','Một số ít câu dài gây mất lượng token đáng kể; OOV pretrained khác UNK vocabulary.'),
                       ('PhoBERT','Giữ hoa/thường; RDRSegmenter trước BPE, tối đa 256 token gồm special tokens, effective batch 32.','Giới hạn kiến trúc; không loại câu dài để làm đẹp chỉ số.')], 'Xử lý riêng cho từng embedder')
                   + f'<p>Protocol: <strong>{mode_label}</strong>. {mode_note}'
                   + ' Chỉ đánh giá test sau huấn luyện; TF-IDF và vocabulary fit riêng trên tập huấn luyện từng phiên bản.</p>')
    if eda_destination is not None:
        eda_base = '../assets/' + eda_destination.relative_to(ROOT / 'pages/assets').as_posix()
        preparation += '<p>' + ' · '.join(f'<a href="{eda_base}/{name}" download>{label}</a>' for name,label in [('rule_impacts.csv','Tác động từng quy tắc'),('rule_examples.csv','Ví dụ trước/sau'),('rule_collisions.csv','Va chạm chuẩn hóa'),('tfidf_diagnostics.csv','Chẩn đoán TF-IDF'),('embedder_rule_comparison.csv','Quy tắc và độ phủ embedder'),('cbow_oov.csv','Từ OOV CBOW'),('truncation_examples.csv','Nội dung bị cắt'),('preprocessing_policy.json','Policy đã chốt')]) + '</p>'
    if six:
        preparation += '<p>Ba pipeline: TF-IDF → LinearSVC (20.000 đặc trưng sparse); CBOW → Conv1d(128, kernel=3) + BiLSTM(64×2) + Dropout(0,5), batch 64, bỏ padding bằng độ dài thật; PhoBERT-base-v2 effective batch 32.</p>'
    analysis = ('<p>Sáu kiến trúc: TF-IDF + LinearSVC, TF-IDF + 1D-CNN, TextCNN, BiLSTM, CNN+BiLSTM và PhoBERT-base-v2. '
                'TF-IDF + CNN tích chập theo trục đặc trưng từ vựng; trục này không biểu diễn thứ tự từ trong câu.</p>'
                '<p>Thời gian train tính từ fit bộ xử lý/khởi tạo mô hình đến hết train và validation; không gồm nạp CBOW chung hoặc test. '
                'Lượt đầu có thể gồm tải pretrained. Các số này không phải phép đo latency phục vụ production.</p>'
                '<h3 id="learning-curves">Đường học</h3><p>Loss và metrics theo epoch thật; vạch đứt nét đánh dấu checkpoint được chọn bằng validation macro-F1 (hoặc epoch cuối nếu thiếu validation). LinearSVC fit một lần, không có đường học epoch tương đương.</p>')
    if six:
        begin = analysis.index('</p>') + 4
        analysis = '<p>Ba pipeline: TF-IDF → LinearSVC; CBOW → CNN + BiLSTM; PhoBERT-base-v2. Mỗi pipeline chạy trên Base/Augmented.</p>' + analysis[begin:]
    for summary_path in sorted(destination.glob('models/*/augmented/training_summary.json')):
        result = json.loads(summary_path.read_text())
        plot = summary_path.parent / 'learning_curves.png'
        if plot.exists():
            analysis += figure(plot, f'{result["architecture"]} · Augmented · checkpoint epoch {result["selected_epoch"]}.')
    analysis += table(['Mô hình', 'Dữ liệu', 'Accuracy (%)', 'P macro (%)', 'R macro (%)', 'F1 macro (%)', 'Train (s)'],
                      [[r['architecture'], r['dataset'], *[f'{100 * float(r[k]):.2f}' for k in ['accuracy', 'macro_precision', 'macro_recall', 'macro_f1']],
                        f'{float(r["train_seconds"]):.1f}'] for r in sorted(rows, key=lambda r: -float(r['macro_f1']))],
                      'Kết quả cùng tập test', 'results')
    analysis += figure(destination / 'model-comparison.png', f'Test macro-F1 của đủ {run_count} cấu hình; mọi cấu hình dùng cùng test.')
    analysis += table(['Mô hình', 'Base F1 (%)', 'Augmented F1 (%)', 'Δ (điểm %)'],
                      [[r['architecture'], f'{100 * float(r["Base"]):.2f}', f'{100 * float(r["Augmented"]):.2f}', f'{float(r["delta_pp"]):+.2f}'] for r in deltas],
                      'Ảnh hưởng của Augmented so với Base')
    analysis += figure(destination / 'confusion-matrices.png', f'Ma trận nhầm lẫn {run_count} lượt: hàng là nhãn thật, cột là dự đoán.')
    wrong = [r for r in read_csv(source / 'errors.csv') if r['architecture'] == 'PhoBERT-base-v2' and r['dataset'] == 'Augmented']
    analysis += table(['sample_id', 'Văn bản gốc', 'Nhãn thật', 'Dự đoán'],
                      [[r['sample_id'], r['text'][:500], r['true_label'], r['predicted_label']] for r in sorted(wrong, key=lambda r: r['sample_id'])[:5]],
                      f'Phân tích lỗi: PhoBERT Augmented có {len(wrong)}/{metadata["sample_counts"]["Test"]} câu sai', 'errors')
    analysis += '<h3 id="explanations">Giải thích mô hình đại diện</h3><p>Trọng số LinearSVC phản ánh điểm quyết định, không phải xác suất. PhoBERT dùng mức giảm xác suất lớp dự đoán ban đầu khi bỏ từng từ trong các câu ngắn được chọn xác định.</p>'
    analysis += figure(destination / 'explanations/svc-weights.png', 'Những từ có trọng số dương cao của LinearSVC Augmented theo từng lớp (trực tiếp trên TF-IDF 20.000 đặc trưng).')
    for path in sorted((destination / 'explanations').glob('phobert-*.png')):
        analysis += figure(path, 'PhoBERT Augmented: thay đổi xác suất khi bỏ từng từ; giá trị dương nghĩa từ đang hỗ trợ lớp dự đoán.')
    asset_base = '../assets/' + destination.relative_to(ROOT / 'pages/assets').as_posix()
    downloads = ' · '.join(f'<a href="{asset_base}/{name}" download>{label}</a>' for name, label in [
        ('summary.csv', 'CSV tổng hợp'), ('per_class_metrics.csv', 'CSV từng lớp'), ('predictions.csv', 'Dự đoán'),
        ('augmentation_delta.csv', 'Chênh lệch Base/Augmented'), ('run.json', 'Nguồn lần chạy')])
    conclusion = (f'<p>Trong lần chạy seed 42, <strong>{esc(best["architecture"])} ({esc(best["dataset"])})</strong> '
                  f'đạt macro-F1 cao nhất {100 * float(best["macro_f1"]):.2f}%, accuracy {100 * float(best["accuracy"]):.2f}%.</p>'
                  '<p>Một seed, nguồn augmentation và khả năng gần trùng còn hạn chế kết luận. Các số liệu mô tả lần chạy hiện tại; không suy ra mọi augmentation đều có ích. '
                  'Tiếp theo có thể bổ sung lineage, chạy nhiều seed và kiểm tra thủ công các cặp nhãn nhầm.</p>'
                  f'<p>{downloads}</p><p>Nhóm SlightSeek: Phạm Duy Anh (2310139), Nguyễn Phan Tuấn Duy (2310491).</p>')
    previous_path = ROOT / 'pages/assets/vlsp-sentiment/oxford/20261120T161056Z/summary.csv'
    if previous_path.exists():
        previous = {(r['architecture'],r['dataset']):r for r in read_csv(previous_path)}
        comparisons = []
        for row in rows:
            old_row = previous.get((row['architecture'],row['dataset']))
            old_f1 = f'{100*float(old_row["macro_f1"]):.2f}' if old_row else '—'
            delta = f'{100*(float(row["macro_f1"])-float(old_row["macro_f1"])):+.2f}' if old_row else '—'
            comparisons.append([row['architecture'],row['dataset'],old_f1,f'{100*float(row["macro_f1"]):.2f}',delta])
        conclusion += table(['Mô hình', 'Tập', 'F1 cũ (%)', 'F1 mới (%)', 'Chênh lệch (điểm %)'], comparisons, 'Đối chiếu pipeline trước ngày 20/11/2026')
        conclusion += '<p>Dấu — nghĩa pipeline không có đối ứng trong lần chạy cũ. Thay đổi đồng thời kiến trúc, xử lý, đặc trưng và mẫu fit; đối chiếu này mô tả kết quả, không cô lập tác động từng thay đổi. <a href="../assets/vlsp-sentiment/oxford/20261120T161056Z/summary.csv">CSV lần chạy trước</a>.</p>'
    resource_html = resources(old, 'sentimentanalysis.ipynb', date)
    if eda_destination is not None:
        eda_row = '<div class="resource-item"><div><h3>Notebook EDA (CPU)</h3><p>Khảo sát gốc, đối chiếu quy tắc, độ phủ TF-IDF/CBOW và mức cắt PhoBERT trước huấn luyện.</p></div><div class="resource-actions"><a class="text-link" href="https://colab.research.google.com/github/superiorhamster/CO5177/blob/main/ipynb/text/sentimentanalysis_eda.ipynb">Mở EDA trên Colab ↗</a> <a class="text-link" href="../notebooks/sentimentanalysis_eda.ipynb" download>Tải notebook EDA có output</a></div></div>'
        # Existing resources() keeps PDF/video rows; insert immediately before PDF.
        marker = re.search(r'<div class="resource-item">\s*<div>\s*<h3>PDF report</h3>', resource_html).start()
        resource_html = resource_html[:marker] + eda_row + resource_html[marker:]
        shutil.copy2(ROOT / 'ipynb/text/sentimentanalysis_eda.ipynb', ROOT / 'pages/notebooks/sentimentanalysis_eda.ipynb')
    inner = hero + '<div class="project-layout"><article class="project-content">' + resource_html
    inner += section('dataset', 'Mô tả tập dữ liệu và EDA', dataset, 1)
    inner += section('preparation', 'Chuẩn bị dữ liệu', preparation, 2)
    inner += section('analysis', 'Mô hình, đường học và kết quả', analysis, 3)
    inner += section('conclusions', 'Kết luận và nguồn kết quả', conclusion, 4) + '</article></div>'
    install_report('text', inner, old, destination, 'sentimentanalysis.ipynb')


def image_report(source):
    check_image(source)
    verification = json.loads((source / 'verification.json').read_text())
    assert not verification['smoke_test']
    execution = json.loads((ROOT / 'ipynb/image/intel_image_classification_trained.ipynb').read_text())['metadata']['verified_execution']
    run_id = execution['run_id']
    date = run_date(run_id)
    destination = ROOT / 'pages/assets/intel-image/oxford' / run_id
    copy_evidence(source, destination)
    (destination / 'source.json').write_text(json.dumps(execution, ensure_ascii=False, indent=2) + '\n')
    info = json.loads((source / 'dataset_source.json').read_text())
    rows = read_csv(source / 'model_comparison.csv')
    manifest = read_csv(source / 'split_manifest.csv')
    counts = {name: sum(r['split'] == name for r in manifest) for name in ['train', 'val', 'test']}
    best = max(rows, key=lambda r: float(r['macro_f1']))
    old = (ROOT / 'pages/projects/image.html').read_text(encoding='utf-8-sig')
    hero = ('<nav class="breadcrumb" aria-label="Điều hướng phân cấp"><a href="../../index.html">Trang chủ</a> / Image</nav>'
            '<section class="project-hero" aria-labelledby="project-title"><div><p class="eyebrow">CO5177 / IMAGE / SLIGHTSEEK</p>'
            '<h1 id="project-title">Phân loại ảnh cảnh Intel — MobileNetV3-Small và ViT-B/16</h1>'
            '<p class="hero-description">Hai mô hình pretrained trên cùng sáu lớp; notebook theo 11 bước Oxford Pets, từ dữ liệu đến Grad-CAM.</p>'
            f'<p class="status-badge">Đã Run all mới từ pretrained weights · Colab T4 · {date} · seed 42</p></div></section>')
    dataset = (f'<p>Intel Image Classification v{info["resolved_version"]}; các lớp {esc(", ".join(info["class_names"]))}. '
               f'Tập gốc có {info["loaded_splits"]["train"]:,} ảnh train và {info["loaded_splits"]["test"]:,} ảnh test. '
               'Ảnh seg_pred không tham gia thực nghiệm có giám sát.</p><h3 id="eda">Khám phá ảnh gốc</h3>')
    for filename, caption in [('eda-samples.png', 'Ảnh mẫu từ train gốc theo sáu lớp.'),
                              ('eda-geometry.png', 'Kích thước và tỷ lệ khung hình ảnh gốc.'),
                              ('eda-quality.png', 'Độ sáng, tương phản và Laplacian variance; đọc cùng ảnh cực trị.'),
                              ('eda-class-counts.png', 'Số ảnh theo lớp trước và sau làm sạch/chia tập.')]:
        dataset += figure(destination / 'eda' / filename, caption)
    dataset += '<h3 id="eda-decisions-title">Quyết định từ EDA</h3><p>Hash pixel phát hiện trùng chính xác; không bao quát gần trùng. Ảnh tối hoặc ít cạnh cần xem nội dung trước khi quyết định xử lý. Resize lên 224×224 không tạo thêm chi tiết.</p>'
    removals = read_csv(source / 'cleaning_log.csv')
    reasons = {reason: sum(r['reason'] == reason for r in removals) for reason in sorted({r['reason'] for r in removals})}
    reason_names = {'train_duplicate_of_test': 'ảnh trùng test', 'train_conflicting_labels': 'ảnh thuộc nhóm mâu thuẫn nhãn',
                    'train_exact_duplicate': 'bản sao cùng nhãn'}
    reason_text = '; '.join(f'{count} {reason_names[reason]}' for reason, count in reasons.items())
    preparation = (f'<p>Đã loại {len(removals)} ảnh train: {esc(reason_text)}. Giữ test gốc hợp lệ; chia train/validation stratified seed 42.</p>'
                   + table(['Split', 'Số ảnh'], list(counts.items()), 'Các tập sử dụng', 'split-table-title')
                   + table(['Tập', 'Preprocessing'], [('Train', 'RandomResizedCrop 224, lật ngang, ColorJitter nhẹ, chuẩn hóa ImageNet'),
                                                    ('Validation/Test', 'Resize, center crop 224 và chuẩn hóa theo pretrained weights')],
                           'Transform và augmentation', 'transforms-table-title')
                   + figure(destination / 'eda/eda-transforms.png', 'Ảnh gốc và đầu vào sau transforms thực tế.'))
    analysis = ('<p>Cả hai mô hình dùng ImageNet pretrained và head sáu lớp. Huấn luyện 3 epoch head (backbone frozen/eval), '
                'sau đó tối đa 15 epoch fine-tuning với LR backbone 1e-5, LR head 1e-4. Batch 16, accumulation 2, hai worker. '
                'Chọn checkpoint bằng validation macro-F1; hòa điểm chọn head; patience fine-tuning 4.</p>')
    stage_rows = []
    all_split_rows, per_class_rows = [], []
    for name in ['mobilenet_v3_small', 'vit_b_16']:
        stages = read_csv(source / name / 'stage_results.csv')
        stage_rows.extend([[IMAGE_NAMES[name], 'classifier' if r['stage'] == 'head' else 'fine-tuning', r['best_epoch'],
                            f'{100 * float(r["val_macro_f1"]):.2f}', 'Có' if r['selected'].lower() == 'true' else '—'] for r in stages])
        all_split_rows.extend({'model': name, **r} for r in read_csv(source / name / 'overall_metrics.csv'))
        per_class_rows.extend({'model': name, **r} for r in read_csv(source / name / 'per_class_metrics.csv'))
        analysis += figure(destination / 'figures' / f'{name}_learning_curves.png', f'{IMAGE_NAMES[name]}: đường học train/validation, vạch đứt đánh dấu mở backbone.')
    for filename, data in [('overall_metrics.csv', all_split_rows), ('per_class_metrics.csv', per_class_rows)]:
        with (destination / filename).open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)
    analysis += table(['Mô hình', 'Stage', 'Epoch tốt nhất', 'Val F1 (%)', 'Được chọn'], stage_rows, 'Checkpoint và hiệu quả fine-tuning')
    analysis += table(['Mô hình', 'Split', 'Loss', 'Accuracy (%)', 'F1 macro (%)'],
                      [[IMAGE_NAMES[r['model']], r['split'], f'{float(r["loss"]):.4f}', f'{100 * float(r["accuracy"]):.2f}',
                        f'{100 * float(r["macro_f1"]):.2f}'] for r in all_split_rows], 'Checkpoint cuối trên ba tập, preprocessing xác định')
    analysis += table(['Mô hình', 'Accuracy (%)', 'P macro (%)', 'R macro (%)', 'F1 macro (%)', 'Tham số', 'Train (s)'],
                      [[IMAGE_NAMES[r['model']], *[f'{100 * float(r[k]):.2f}' for k in ['accuracy', 'macro_precision', 'macro_recall', 'macro_f1']],
                        f'{int(r["parameters"]):,}', f'{float(r["training_seconds"]):.1f}'] for r in rows], 'So sánh trên cùng test', 'results-table-title')
    analysis += figure(destination / 'figures/model_comparison.png', 'So sánh các test metrics của hai checkpoint được chọn bằng validation.')
    analysis += table(['Mô hình', 'Lớp', 'Precision (%)', 'Recall (%)', 'F1 (%)', 'Support'],
                      [[IMAGE_NAMES[r['model']], r['class_name'], *[f'{100 * float(r[k]):.2f}' for k in ['precision', 'recall', 'f1']], r['support']]
                       for r in per_class_rows if r['split'] == 'test'], 'Kết quả từng lớp trên test', 'class-f1-table-title')
    analysis += '<h3 id="errors">Ma trận nhầm lẫn và ảnh sai</h3>'
    for name in ['mobilenet_v3_small', 'vit_b_16']:
        analysis += figure(destination / 'figures' / f'{name}_confusion.png', f'{IMAGE_NAMES[name]}: hàng là lớp thật, cột là dự đoán; số lượng và tỷ lệ theo hàng.')
        error_plot = destination / 'figures' / f'{name}_errors.png'
        if error_plot.exists():
            analysis += figure(error_plot, f'{IMAGE_NAMES[name]}: ảnh sai tự tin nhất; hiển thị đúng crop mô hình nhìn thấy.')
    analysis += '<h3 id="explanations">Giải thích MobileNet bằng Grad-CAM</h3>'
    analysis += figure(destination / 'figures/mobilenet_v3_small_gradcam.png', 'Grad-CAM trên features[-1], nhắm lớp dự đoán và chồng lên crop 224×224. Trọng số không thay đổi sau giải thích.')
    asset_base = '../assets/' + destination.relative_to(ROOT / 'pages/assets').as_posix()
    conclusion = (f'<p>Trong lần chạy seed 42 trên {counts["test"]:,} ảnh test, <strong>{esc(IMAGE_NAMES[best["model"]])}</strong> '
                  f'đạt macro-F1 cao nhất {100 * float(best["macro_f1"]):.2f}%, accuracy {100 * float(best["accuracy"]):.2f}%.</p>'
                  '<p>Một seed, hash pixel chưa bao quát gần trùng và crop có thể bỏ nội dung. Các thí nghiệm tiếp theo có thể chạy nhiều seed, '
                  'kiểm tra gần trùng và chọn crop/augmentation bằng validation.</p>'
                  '<h3 id="evidence-sources-title">Nguồn và kiểm chứng</h3>'
                  '<p>Notebook kiểm tra checkpoint, history, dự đoán và confusion matrix; metrics trên website được tính lại từ CSV.</p>'
                  f'<p><a href="{asset_base}/model_comparison.csv" download>CSV so sánh</a> · '
                  f'<a href="{asset_base}/overall_metrics.csv" download>CSV ba split</a> · '
                  f'<a href="{asset_base}/per_class_metrics.csv" download>CSV từng lớp</a> · '
                  f'<a href="{asset_base}/source.json" download>Thông tin lần chạy</a> · '
                  f'<a href="{asset_base}/split_manifest.csv" download>Split manifest</a></p>'
                  '<p>Nhóm SlightSeek: Phạm Duy Anh (2310139), Nguyễn Phan Tuấn Duy (2310491).</p>')
    inner = hero + '<div class="project-layout"><article class="project-content">' + resources(old, 'intel_image_classification_trained.ipynb', date)
    inner += section('dataset', 'Mô tả tập dữ liệu và EDA', dataset, 1)
    inner += section('preparation', 'Chuẩn bị dữ liệu', preparation, 2)
    inner += section('analysis', 'Mô hình và kết quả', analysis, 3)
    inner += section('conclusions', 'Kết luận và nguồn kết quả', conclusion, 4) + '</article></div>'
    install_report('image', inner, old, destination, 'intel_image_classification_trained.ipynb')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--text-results', type=Path)
    parser.add_argument('--image-results', type=Path)
    parser.add_argument('--eda-results', type=Path)
    args = parser.parse_args()
    if args.text_results:
        text_report(args.text_results, args.eda_results)
    if args.image_results:
        image_report(args.image_results)


if __name__ == '__main__':
    main()
