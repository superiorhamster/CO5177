# Handoff: Chạy full sáu lượt Text và đồng bộ website Raincloud

## Session Metadata
- Workspace: `/home/anhpd/Project/Group/LapTrinhAIDS/Assignment`
- Ngày: 21/11/2026, Asia/Ho_Chi_Minh; branch main.
- Tài liệu này thay thế bộ ba/số lượt trong handoff trước. Người dùng đã xác nhận chính xác ba pipeline bên dưới.

## Current State Summary
Raincloud đã được thay trong notebook EDA và smoke trên Colab CPU bằng toàn bộ CSV 15.249 câu. Notebook full đã chuyển từ 12 lượt sang sáu lượt và smoke thành công trên Colab T4. Cả hai phiên đã giải phóng. Chưa chạy full sáu lượt và chưa thay số liệu hoặc notebook tải xuống của website. Website hiện vẫn phản ánh lượt full 12 cấu hình trước đó. Hãy hoàn thành lượt full sáu cấu hình, thu checkpoint/output, kiểm chứng và cập nhật trang Text; không chỉ lập kế hoạch hoặc dừng ở báo cáo tiến độ.

## Important Context
Đọc AGENTS.md, README.md và docs/CONTENT_EDITING_GUIDE.md. Giữ UI tiếng Việt, BK logo, accessibility/print, markers, sidebar, anchor và PDF/video pending. Chỉ Text trong phạm vi; không sửa Image/Tabular. Không commit, push, deploy, mua compute units, đổi gói hoặc chuyển sang GPU trả phí. Chỉ dùng T4 miễn phí; nếu không được cấp, lưu trạng thái và báo lỗi thật.

### Decisions Made
Đúng 3 pipeline × Base/Augmented = 6 lượt:
1. TF-IDF → TruncatedSVD → LinearSVC. TF-IDF sparse float32, analyzer word+emoticon, unigram/bigram, min_df=1, max_features=20.000. SVD tối đa 300 thành phần, thực tế min(300, n_fit−1, n_features−1), random_state=42; chỉ fit trên train riêng mỗi phiên bản.
2. CBOW → GRU: lowercase + PyVi, vocabulary 10.000 fit riêng, PAD/UNK, embedding pretrained khi có/trainable/clone độc lập, max 300 từ, GRU một chiều hidden64, batch64, pack theo độ dài thật, dropout0.5. Full 4 epoch khi thiếu lineage.
3. PhoBERT-base-v2: giữ hoa/thường, RDRSegmenter trước BPE, max256 gồm special tokens, effective batch32. Full 3 epoch khi thiếu lineage.

Seed42, giữ văn bản gốc, NFC/khoảng trắng, không thay teencode/emoticon thành từ cảm xúc hoặc rút chữ kéo dài. Policy `vlsp-eda-v3-six-raincloud` được nhúng vào notebook. Có lineage thì validation chung theo nhóm nguồn và chọn validation macro-F1; hiện dữ liệu thiếu lineage nên dùng epoch cuối cố định. Không chọn cấu hình bằng nhãn/điểm test. Full phải giữ nguyên 1.050 sample ID test gốc; không dùng 6 mẫu smoke làm kết quả full.

## Work Completed
### Critical Files
- `ipynb/text/sentimentanalysis.ipynb`: nguồn full mới, 11 mục, 17 cell mã, output full cũ đã bỏ. Chưa phải notebook đã Run all full sáu lượt.
- `ipynb/text/sentimentanalysis_eda.ipynb`: Raincloud mới và mô tả; metadata visualization_smoke ghi đúng phạm vi kiểm tra renderer CPU. Không gọi nó là Run all mới toàn bộ EDA. Cell thống kê nặng chứa outputs cũ có boxplot đã được xóa để tránh hình sai; các CSV/statistics gốc được giữ trong artifacts.
- `runs/raincloud-six-20261121/eda-artifacts/`: artifacts EDA gốc được sao chép sang thư mục mới, thay cbow-coverage.png bằng Raincloud, thêm cbow-raincloud-summary.csv, raincloud_verification.json và policy mới. Thống kê không tính lại; source.json ghi rõ nguồn tái sử dụng.
- `runs/raincloud-six-20261121/cpu-smoke/`: input/output notebook smoke CPU, execution.log, driver.json, artifacts.zip và artifacts/. CPU driver passed/vm_released=true. Kiểm tra số mẫu, quartile, zero fraction, sampling, nhóm không đổi và giá trị ngoài miền đã đạt.
- `runs/raincloud-six-20261121/t4-smoke-final/`: smoke sáu lượt đã đạt; input/output notebook, preflight, log, driver state và ZIP. Artifacts đã giải nén tại `artifacts/smoke-20261121T164408Z/`. Driver passed/vm_released=true. Nguồn smoke đã đối chiếu giống notebook root.

### Raincloud semantics
Hai ô OOV pretrained/UNK vocabulary, mỗi ô Base/Augmented, thang 0–100%. Nửa KDE Scott phản chiếu biên 0/1, box median/IQR dùng toàn bộ dữ liệu. Điểm jitter tối đa1.500/nhóm, seed42; ghi n và tỷ lệ bằng0. Nhóm không đổi không vẽ KDE giả. Dữ liệu gốc Base5.100/Augmented10.149; vocabulary chẩn đoán fit trên từng tập phát triển gốc, vocabulary train fit lại sau audit. Hình đã xem trực quan, không cắt nhãn.

### Fixes and scripts
- Hàm đánh giá GRU có @torch.inference_mode(); không bỏ decorator khi tái cấu trúc AST.
- VnCoreNLP tải trực tiếp ba file từ kho chính thức bằng urllib, retry3, kiểm tra file/JAR. Không quay lại download_model dùng wget không kiểm tra trạng thái.
- SVC giải thích bằng coef @ svd.components_, kiểm tra tổng đóng góp TF-IDF và intercept khớp margin. Không coi margin là xác suất.
- `scripts/validate_oxford_notebooks.py` hỗ trợ cả 12 lượt cũ và sáu lượt v3, policy và per-class/CM/ID/checkpoints.
- `scripts/validate_text_eda.py` hỗ trợ provenance Raincloud, CSV hash, hash hàm vẽ, quartile, zero và cỡ mẫu điểm.
- `scripts/sync_oxford_reports.py` đã chuẩn bị cho sáu lượt, SVD/GRU, Raincloud và metadata epoch đúng; so sánh lịch sử có dấu — khi không có đối ứng. Chưa chạy với kết quả full sáu lượt; cần kiểm tra idempotency và render sau full.

## Immediate Next Steps
1. Kiểm tra git status và đọc các file trên; không ghi đè công việc người khác. Xác nhận ba pipeline/sáu lượt trong source hiện tại. Không tái chạy smoke hoặc EDA nếu source không thay đổi và bằng chứng hiện tại vẫn hợp lệ.
2. Tạo thư mục run full mới, ví dụ `runs/raincloud-six-20261121/train-full/`; copy notebook root và preflight.py từ t4-smoke-final vào đó. Không dùng thư mục train-full v2 cũ. Lưu snapshot nguồn và hash.
3. Khởi chạy bằng launcher detached (subprocess.Popen với stdin DEVNULL, stdout/stderr vào driver.log, start_new_session=True), không phụ thuộc terminal:

```sh
python -u scripts/run_colab_notebook.py runs/raincloud-six-20261121/train-full/sentimentanalysis.ipynb --kind text --session raincloud-six-full-t4 --config /tmp/raincloud-six-full.json
```

Không truyền --smoke hoặc --existing cho full mới. Bắt đầu kernel sạch và pretrained/new weights; không resume smoke/weights cũ. Theo dõi log, thông báo tiến độ, chờ đến hoàn tất. Nếu lỗi, sửa và chạy lại snapshot mới theo phạm vi cần thiết; không dựng số liệu hoặc bỏ cấu hình yếu.
4. Launcher tự thu artifacts.zip, selected-checkpoints.zip và stop VM. Parse mọi output_type=error, verification.json và driver.json. CLI có thể trả0 dù cell lỗi; terminal đôi khi kết thúc143 nhưng VM còn chạy. Không khẳng định thành công chỉ từ exit code. Nếu launcher mất, xác minh đúng phiên sở hữu trước khi phục hồi; không stop phiên người khác.
5. Giải nén ZIP vào thư mục artifacts cạnh ZIP; lấy tên `full-<run-id>` thực từ run.json. Kiểm tra đủ6 lượt, test1.050, epochs4/3, policy, metrics/support/CM tính lại, reload và explanation unchanged. Kiểm tra ZIP weights bằng SHA-256.
6. Cài output full sau khi kiểm chứng:

```sh
python -B scripts/record_notebook_execution.py INPUT_NOTEBOOK OUTPUT_NOTEBOOK EXECUTION_LOG FULL_ARTIFACT_DIR ipynb/text/sentimentanalysis.ipynb --run-id ACTUAL_RUN_ID
```

Script giữ source guard; không sửa source sau dispatch. Nó chỉ bỏ progress tạm thời, giữ bằng chứng. execution_count null là đặc tính CLI, không tự bịa count.
7. Đồng bộ web:

```sh
python -B scripts/sync_oxford_reports.py --text-results FULL_ARTIFACT_DIR --eda-results runs/raincloud-six-20261121/eda-artifacts
```

Kiểm tra header/bảng/caption/conclusion đều sáu lượt, đúng SVD+SVC/GRU/PhoBERT và epochs4/3; Raincloud và diễn giải sampling/zero. Giữ các kết quả cũ có định danh nguồn để đối chiếu, không ghi đè lịch sử. Không gọi chênh lệch giữa hai pipeline là tác động nhân quả riêng của preprocessing.
8. Đồng bộ hai notebook download và Colab GitHub main. EDA mới có smoke renderer, không phải Run all toàn bộ EDA mới: ghi đúng phạm vi. Nếu cần xuất notebook EDA có toàn bộ output mới để bàn giao, chạy EDA từ kernel sạch trên CPU, thu ZIP và ghi provenance thật; copy policy đã chốt sau khi xác minh nguồn dữ liệu/mã, không tái chọn theo điểm test.
9. Chạy các kiểm tra bên dưới, kiểm tra sync idempotent, links/anchors/render desktop/mobile. Ghi README run và kết quả thật. Chưa commit/push/deploy.

## Validation
Đã đạt:
- CPU Raincloud smoke passed, rows15.249, groups4; vm_released=true.
- T4 smoke đủ6 lượt, 24 mẫu fit mỗi phiên bản, cùng6 ID test, 1 epoch neural; không có cell lỗi trong17 cell.
- CSV metrics/support/CM tính lại khớp; checkpoint reload và explanation weights unchanged đạt. SVD smoke thực tế23 chiều với24 mẫu fit.
- AST/nbformat, build_site --check, node --check navigation.js, git diff --check đạt. Website chưa đổi nội dung trong lượt này.

Lệnh nghiệm thu full:

```sh
python -B scripts/validate_oxford_notebooks.py --require-executed --verify-checkpoints --text-results FULL_ARTIFACT_DIR --eda-results runs/raincloud-six-20261121/eda-artifacts
python -B scripts/build_site.py --check
node --check pages/assets/navigation.js
git diff --check
```

Các notebook tải xuống chỉ được gọi là full mới sau khi byte-equal với nguồn có output full đã xác minh. Không đưa weights vào liên kết công khai. selected-checkpoints.zip nằm dưới runs được Git ignore.

## Environment State
Không còn phiên CPU/T4 của lượt smoke: cả hai driver.json xác nhận vm_released=true. Config /tmp chứa thông tin session/xác thực; không in hoặc đưa vào tài liệu/artifacts công khai. Colab CLI đã auth; chỉ escalation khi sandbox chặn log/network. `colab skill` là hướng dẫn operator. CLI venv Python có nbformat tại `/home/anhpd/.local/share/uv/tools/google-colab-cli/bin/python`.

Các lượt `t4-smoke/` và `t4-smoke-retry/` trong cùng thư mục run là bằng chứng lỗi cũ (tải JAR và mất inference decorator), đã giải phóng VM; không dùng làm smoke đạt.

## Blockers/Open Questions
Không cần quyết định thêm từ người dùng. Full sáu lượt và cập nhật website là công việc còn lại. Nếu T4 miễn phí không được cấp, báo tình trạng thật và không đổi gói.

## Related Resources
- Skill notebook: `/home/anhpd/.codex/skills/jupyter-notebook/SKILL.md`
- Skill bàn giao: `/home/anhpd/.codex/skills/session-handoff/SKILL.md`
- Lịch sử full12 trước đó: `runs/vlsp-eda-20261121/train-full/` và `pages/assets/vlsp-sentiment/eda-v2/20261121T123956Z/`.
