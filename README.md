# **Đồ Án CDIO (DS447A)**
### **Đề Tài**: ***Tìm Kiếm Bằng Hình Ảnh***
#### ***Giảng viên hướng dẫn: Mr. Đặng Việt Hùng***
#### ***Thành viên thanh gia:***
* Trương Minh Thống
* Nguyễn Trọng Hiếu
* Đặng Hữu Nam
* Thân Văn Việt

![markdown](https://i.postimg.cc/bv39RtcD/DS447.png)
***
### ***Giới thiệu về ý tưởng***:
1. Một giao diện để tương tác với người dùng.
2. Người dùng upload image cần thực hiện.
3. Model nhận biết được các đối tượng trong hình và tạo ra các ***button*** tìm kiếm ứng với mỗi đối tượng được detect.
4. Người dùng chọn vào 1 trong các ***button*** (ứng với đối tượng cần tìm kiếm hình liên quan).
5. Các hình ảnh gần giống nhất đối với đối tượng sẽ lần lượt xuất hiện theo tỉ lệ từ cao đến thấp.

### ***Các yêu cầu để chạy chương trình***:
> Cài đặt các thư viện cần thiết:

`pip install -r requirements.txt`

> Tải các file hỗ trợ, [**NeedToStart.zip**](https://drive.google.com/file/d/1Me_e4HlpkvaWwKhnUvrXti6UuMSkEyE5/view?usp=sharing) bao gồm:

* `yolov7.onnx`: Được thông qua bởi thư viện onnxruntime dùng để tăng tốc độ xử lý của mô hình Yolo khi sử dụng.
* `vectors.pkl`: File lưu trữ các vector của bộ dữ liệu sử dụng trong việc tìm kiếm. Cần đưa vào đúng vị trí `img_search\vectors.pkl`.

### ***Chạy thử chương trình***:
> Thực hiện lệnh:

`py GUI.py`

- Nhấn vào **Upload file** để tải ảnh muốn tìm kiếm
- Chọn **đối tượng** muốn tìm kiếm
- Xuất hiện **kết quả**
![markdown](https://i.postimg.cc/x8j8Rq28/image.png)

### ***Nhận diện đối tượng***:
- Sử dụng mô hình **Yolov7**:
```Shell
https://github.com/WongKinYiu/yolov7
```
- Dữ liệu: Coco Dataset
    - Đối tượng: `car, airplane, bus, truck, boat, bird, cat, dog, elephant, bear, zebra, backpack, kite, cup, banana, orange, broccoli, dining table, laptop`
- Mô hình: Yolov7
    | Model | Test Size | AP<sup>test</sup> | AP<sub>50</sub><sup>test</sup> | AP<sub>75</sub><sup>test</sup> | batch 1 fps | batch 32 average time |
    | :-- | :-: | :-: | :-: | :-: | :-: | :-: |
    | [**YOLOv7**](https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt) | 640 | **51.4%** | **69.7%** | **55.9%** | 161 *fps* | 2.8 *ms* |
- Để tăng tốc độ xử lý và nhận diện của mô hình, chuyển file weights sang dạng onnx
```Shell
https://github.com/WongKinYiu/yolov7#export
```
- Sử dụng file tracking.py để tiến hành load mô hình và các trọng số đã được lưu trong file yolov7.onnx
    - Với hàm predict() ta truyền đường dẫn tới hình ảnh muốn nhận diện vào, kết quả sẽ được lưu vào trong đường dẫn:
        ```Shell
        Dành cho hình ảnh
        Result/images/
        ```
        ```Shell
        Dành cho vị trí các đối tượng
        Result/labels/
        ```
### ***Tìm kiếm hình ảnh***:
1. *Trích xuất đặc trưng toàn bộ ảnh trong tập dữ liệu:*
* Trước khi thực hiện bước tìm kiếm ảnh, các hình ảnh trong bộ dữ liệu sẽ được trích xuất đặc trưng thông qua file `store_vectors.py` và sẽ được lưu dưới dạng mã nhị phân gồm 2 file: `paths.pkl(lưu đường dẫn đến hình ảnh)` và `vectors.pkl(lưu các vector đặc trưng của ảnh)`.
* Người dùng cũng có thể thêm data vào hoặc tạo mới 2 files pkl phía trên với kho dữ liệu mong muốn bằng cách chạy file `store_vectors` và thay đổi `data_folder="paths/to/folder_images"`
* Mô hình **VGG16** với tập weights (no-top) [**ImageNet**](https://storage.googleapis.com/tensorflow/keras-applications/vgg16/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5)  được sử dụng để trích xuất đặc trưng.
2. *Trích xuất ảnh muốn tìm kiếm:*
* Sau khi thông qua detect bởi yolov7 ở bước trước. Nếu người dùng chọn vào đối tượng muốn tìm kiếm hình liên quan. Hình ảnh được cắt từ bouding box của đối tượng được detect và thông qua mô hình VGG16 để trích xuất đặc trưng.
* Sau khi trích xuất đặc trưng ta có được vector đặc trưng của hình, ta sẽ tính khoảng cách euclid trên hệ trục tọa độ Oxy. Từ đó so sánh với các điểm hình ảnh đã trích xuất trước đó và lựa chọn ra K hình (ở đây là 6) gần giống nhất xuất hiện ra phía bên tay phải của giao diện.

### ***Giao diện***:
- Sau khi tải ảnh lên và cho mô hình yolov7 nhận diện đối tượng sẽ truy xuất vào hình ảnh thu được từ `Result/images/`, tải lên để người dùng có thể hình dung được
 
![markdown](https://i.postimg.cc/9F0xzp7R/cats-and-dogs-wallpapers.jpg)

- Dựa vào các tọa độ của các đối tượng được lưu ở `Result/labels/` để thực hiện cắt ảnh chỉ chứa đối tượng đó

![markdown](https://i.postimg.cc/kg61N6Sg/image.png)

- Tạo button cho hình ảnh đối tượng được tạo ra, để khi người dùng click vào thì sẽ truy xuất đến hàm predict ở trong `Image_Search/search_image.py` và tiến hành tìm kiếm các ảnh tương đồng
`Kết quả khi tìm kiếm đối tượng là con mèo ở hình dưới`

![markdown](https://i.postimg.cc/PxQpB4gr/image.png)

<!-- > Kho dữ liệu các hình ảnh được lưu dưới dạng nhị phân ở 2 files (***vectors.pkl*** và ***paths.pkl***) ứng với vector và đường dẫn của mỗi hình.
> Người dùng có thể tạo mới 2 files pkl phía trên bằng kho dữ liệu mới bằng cách chạy file `store_vectors` và thay đổi `data_folder="paths/to/folder_images"` -->
