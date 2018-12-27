# Tool sinh services

Đây là một tool được viết bằng python giúp sinh tự động các services lên Kong API Gateway từ một file dữ liệu json.

## Tóm tắt

Tài liệu này sẽ giải thích chi tiết về cách thức hoạt động của tool cũng như ý nghĩa của các trường dữ liệu đầu vào ứng với các thông tin của services trong Kong. 

## Các tính năng của tool

- Tự động sinh ra các services, các routes tương ứng với mỗi service, thêm các plugins như ip-restriction, redirect http to https, certificates từ file dữ liệu đầu vào định dạng .json theo chuẩn.
- Tự động xóa các services, routes, certificates, plugins.
  

## Cách thức hoạt động của tool
### Input của tool
Tool nhận ba tham số dữ liệu đầu vào:
   - Đường dẫn đến tệp json (__-file__) 
   - Host của Kong API Gateway (__-host__), ví dụ: http://192.168.26.220:8001
   - Một option để xác định tác vụ muốn thực hiện (__-option__), nhận hai giá trị là __delete__ hoặc __create__ tương ứng với tác vụ sinh hoặc xóa service.

### Chi tiết tệp dữ liệu đầu vào
__Định dạng chuẩn của một tệp json:__

![](https://raw.githubusercontent.com/PinoNTK/MyViettelTest/master/jsonsample.PNG)


__Ý nghĩa của các trường__
 - __name__:  
 - __server_name__:  là __hosts__ của route của service được tạo ra.
 - __listen__: __port__ mặc định của service nếu __host__ trong __locations__ không chứa __port__.
 - __locations__: Một danh sách chứa các cặp __path__ : __url__, ứng với mỗi cặp ta sẽ tạo một route tương ứng cho service có tên là __name__ + __path__. __url__ chứa các thông tin về __host__ và __port__ của service này. __path__ chính là  __paths__ của route ứng với service này.
 - __ip-restriction__:
   - blacklist: chứa danh sách các IP bị chặn truy cập
   - whitelist: chứa danh sách các IP được phép truy cập
 - __ssl__: 
   - Nhận hai giá trị __true__ hoặc __false__.
   - Xác định xem các routes tương ứng với service đó có hỗ trợ giao thức https không. Nếu có ta sẽ thêm certificates cho nó và đặt __protocol__ tương ứng của route là __https__. Mặc định __protocols__ hỗ trợ cả __http__ và __https__.
 - __cert__: chứa đường dẫn đến file pem chứa ssl certificate.
 - __private_key__: chứa đường dẫn đến file pem chứa khóa RSA không công khai.
 - ****is_redirected****: nhận hai giá trị __true__ hoặc __false__, xác định xem có điều hướng các http request thành https request hay không.
 
 ![](https://raw.githubusercontent.com/PinoNTK/MyViettelTest/master/Drawing1.png)
## Cách thức triển khai
### Sinh service, routes, certificates, ...:
		python auto_config_apigateway.py --host your_host --file file_name --action create
### Xóa tất cả services, routes, certificates, ...:
		python auto_config_apigateway.py --host your_host --file file_name --action delete
