# Đồ án cuối kỳ môn Nhập môn khoa học dữ liệu
## Thông tin nhóm
- STT: 12
- Thành viên:
  - Vũ Đăng Hoàng Long (18120203)
  - Nguyễn Huỳnh Đại Lợi (18120198)
  
---
# Giới thiệu đồ án

Chủ đề: Nhận diện chủ đề của một đoạn văn bản bất kỳ.

Input: một đoạn văn bản bất kỳ.

Output: một trong 18 phân lớp sau:

| | | |
| :- | :- | :- |
| 1. thời sự quốc tế | 2. thời sự trong nước | 3. du lịch |
| 4. kinh doanh | 5. giải trí | 6. công nghệ |
| 7. nhà đất | 8. sức khỏe | 9. giáo dục |
| 10. khoa học | 11. thể thao | 12. văn hóa |
| 13. pháp luật | 14. yêu | 15. xe |
| 16. thời trang | 17. nhịp sống trẻ | 18. ăn gì |

Nguồn dữ liệu: tất cả bài báo thu thập từ trang báo điện tử Tuổi trẻ Online (https://tuoitre.vn/).

Mục đích:
- Khách quan: phục vụ việc nhận diện chủ đề một cách tự động.
- Chủ quan: lọc các bài viết trên mạng xã hội theo chủ đề mà em quan tâm để tránh lãng phí thời gian lướt facebook chỉ để tìm chủ đề mà em quan tâm 🥴.

---
# Cấu trúc github
|----resources/ : thư mục chứa các file hình ảnh dùng trong notebook Final.ipynb.<br>
|----src/ : thư mục chứa các file data thu thập được, các notebook không dùng đến nhưng phát sinh trong quá trình làm việc nhóm để trao đổi, pickle của mô hình học được.<br>
|<br>
|--Final.ipynb : file notebook chính dùng để báo cáo, tất thảy mọi thứ đều ở đây <3.<br>
|--Demo_Model.ipynb : notebook này dự tính sẽ lấy các pickle của model đã train sẵn từ file final.ipynb để phục vụ dự đoán đoạn văn bản ngẫu nhiên. Tuy nhiên do một số trục trặc pickle nhóm vẫn chưa thể chạy được.<br>
|--Slide.pdf\/Slide.pptx : file powerpoint và bản pdf để coi tránh lỗi font, hình,...<br>
|--Teamwork.pdf : file báo cáo quá trình làm việc của nhóm<br>
