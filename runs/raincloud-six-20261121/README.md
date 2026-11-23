# Raincloud và smoke sáu lượt — 21/11/2026

Đã thay boxplot CBOW bằng Raincloud trong notebook EDA. Đã kiểm tra renderer trên Colab CPU bằng toàn bộ 15.249 mẫu của CSV cũ, không tính lại các thống kê EDA không đổi. Các nguồn/artifacts cũ được giữ nguyên; `eda-artifacts/source.json` ghi nguồn tái sử dụng. Notebook EDA ghi rõ phạm vi visualization_smoke, không tự nhận Run all toàn bộ mã mới.

Đã chuyển notebook full về ba pipeline × Base/Augmented = sáu lượt: TF-IDF → TruncatedSVD → LinearSVC; CBOW → GRU; PhoBERT-base-v2. Full mặc định GRU4 epoch, PhoBERT3 epoch khi thiếu lineage; SVD tối đa300 thành phần, GRUhidden64/batch64. Tiền xử lý EDA và seed42 được giữ.

- [CPU smoke](cpu-smoke/): input/output/log/driver và artifacts; passed, vm_released=true.
- [Raincloud](cpu-smoke/artifacts/cbow-coverage.png): nửa KDE, median/IQR và điểm jitter; dữ liệu/thống kê đầy đủ, điểm tối đa1.500/nhóm, seed42. Nhóm bằng0/không đổi được ghi rõ.
- [EDA artifacts dùng cho web mới](eda-artifacts/): giữ thống kê, thêm Raincloud, summary, verification và policyv3.
- [T4 smoke đạt](t4-smoke-final/): 17 cell mã không lỗi, sáu lượt, 24 mẫu fit mỗi phiên bản và cùng6 mẫu test; epoch1 cho neural.
- [Kết quả smoke đã giải nén](t4-smoke-final/artifacts/smoke-20261121T164408Z/): metrics/support/confusion matrix được tính lại từ CSV; checkpoint reload/explanation unchanged đạt. SVD thực tế23 chiều vì smoke có24 mẫu fit.

Hai lượt T4 trước đó là bằng chứng lỗi, không phải smoke đạt: lỗi tải VnCoreNLP JAR và lỗi decorator inference bị mất khi tái cấu trúc. Cả hai đã giải phóng phiên; mã hiện tại sửa cả hai lỗi.

Đã đạt: AST, nbformat, validate_text_eda, validate_oxford_notebooks với artifacts smoke, build_site --check, node --check navigation.js và git diff --check. Đã xem hình Raincloud xuất thực tế.

Chưa chạy full sáu lượt, chưa thay số liệu và bản tải xuống trên website; website vẫn phản ánh full12 trước đó. Agent tiếp theo dùng tài liệu bàn giao `.claude/handoffs/2026-11-21-234749-raincloud-six-full-and-web.md` từ thư mục gốc để hoàn tất full và đồng bộ web. Script sync đã chuẩn bị cho sáu lượt nhưng cần kiểm tra với artifacts full thật, idempotency và render.

Không commit/push/deploy. Image/Tabular không thay đổi.
