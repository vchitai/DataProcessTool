# Website Data Process Tool

Công cụ xử lý dữ liệu trên Website xxx.org

## Grade Data Process

Các bước sử dụng: 

- Đổi tên file điểm thành **Grade.csv**

- Đổi tên file thời gian làm bài thành **Result.csv**

- Chạy chương trình, nhập các tham số: "Thời gian làm bài tối đa", số thứ tự của bài kiểm tra

**Setting**

Các thiết đặt nên thay đổi với mỗi lần sử dụng:

- Cột điểm đầu tiên (-1): **firstGradeColumn** = {int} (Mỗi khóa mỗi khác)

- Số lượng highlight: **top** = {int} (Optional)

- Tên staff (Để lọc ra): **staffName** = Array{String} (Optional)

## Forum Data Process

Các bước sử dụng:

- Download Phantomjs: https://goo.gl/1JN7FN

- Đặt file ngang hàng crawler

- Chạy file forumProcess

- Nhập email và password

- Chờ kết quả...