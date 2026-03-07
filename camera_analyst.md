# PHẦN 1: TỔNG QUAN DỰ ÁN CAMERA ANALYST

## 1.1. Giới thiệu dự án (Introduction)

Trong bối cảnh ngành F&B cạnh tranh khốc liệt, việc quản lý nhà hàng không còn đơn thuần là giám sát qua màn hình camera truyền thống. Các hệ thống hiện tại thường chỉ đóng vai trò là "mắt ghi hình" thụ động, đòi hỏi con người phải trực tiếp quan sát và đánh giá, dẫn đến sai sót và lãng phí nguồn lực.

**Dự án Camera Analyst** là hệ thống Trí tuệ nhân tạo (AI) được thiết kế để chuyển đổi toàn bộ luồng dữ liệu hình ảnh từ 06 camera hiện có thành các  **chỉ số kinh doanh (Business Insights)** . Hệ thống không chỉ quan sát, mà còn hiểu, phân tích và đưa ra các quyết định quản trị về nhân sự, chất lượng món ăn và hành vi khách hàng một cách tự động theo thời gian thực (**$real-time$**).

## 1.2. Phân tích thực trạng & Nhu cầu cấp thiết (Problem Statement)

Từ yêu cầu thực tế của khách hàng, chúng tôi xác định 3 "nỗi đau" (Pain points) cốt lõi mà các nhà hàng đang gặp phải:

1. **Thất thoát chi phí nhân sự:** Chủ nhà hàng đang trả lương dựa trên "thời gian có mặt" (Attendance) chứ không phải "thời gian lao động thực tế" (Active Work). Việc nhân viên ngồi chơi, sử dụng điện thoại trong giờ làm việc là một lãng phí lớn nhưng rất khó định lượng.
2. **Sự thiếu đồng nhất về chất lượng (QC):** Mỗi đầu bếp, mỗi ca làm việc lại có sự sai lệch nhỏ trong cách trình bày và định lượng món ăn. Việc kiểm soát thủ công tại quầy ra đồ thường bị bỏ qua khi nhà hàng đông khách.
3. **Dữ liệu khách hàng rời rạc:** Việc đếm khách bằng tay hoặc ước tính qua hóa đơn không phản ánh đúng lưu lượng thực tế (conversion rate) và thời gian khách phải chờ đợi để được phục vụ.

## 1.3. Mục tiêu chiến lược (Strategic Objectives)

Hệ thống Camera Analyst được triển khai với 4 mục tiêu chính:

* **Số hóa quản trị nhân sự:** Tự động hóa hoàn toàn việc chấm công bằng khuôn mặt và đo lường chính xác hiệu suất làm việc của từng cá nhân trong khu vực bếp và quầy.
* **Chuẩn hóa quy trình QC:** Thiết lập một "hàng rào AI" tại khu vực ra đồ để đảm bảo mọi món ăn đều đạt chuẩn hình ảnh mẫu trước khi đến tay khách hàng.
* **Tối ưu hóa dòng tiền:** Cung cấp báo cáo về **"Tổng tiền thực tế"** (chi phí chi trả cho năng suất thực sự) để giúp chủ nhà hàng điều chỉnh định biên nhân sự phù hợp theo từng khung giờ.
* **Nâng cao trải nghiệm khách hàng:** Theo dõi thời gian chờ và lưu lượng khách để tối ưu tốc độ phục vụ.

## 1.4. Giá trị cốt lõi mang lại (Value Proposition)

Hệ thống của **DSC-Labs** mang lại giá trị vượt trội thông qua 3 yếu tố:

* **Tầm nhìn máy tính tiên tiến:** Áp dụng các kỹ thuật **$SOTA$** (State-of-the-art) như Pose Estimation, Action Recognition và Deep Metric Learning để giải quyết các bài toán phức tạp mà camera thường không làm được.
* **ROI rõ ràng (Return on Investment):** Bằng việc phát hiện và cắt giảm thời gian "ngồi chơi" của nhân sự, hệ thống giúp khách hàng thu hồi vốn đầu tư chỉ sau 3-6 tháng vận hành thông qua việc tối ưu quỹ lương.
* **Tính bảo mật & Riêng tư:** Giải pháp xử lý dữ liệu tại biên (Edge Computing), đảm bảo hình ảnh nhạy cảm không bị rò rỉ và tuân thủ các quy định về quyền riêng tư của nhân viên và khách hàng.

# PHẦN 2: CÁC MODULE AI CỐT LÕI VÀ PHÂN TÍCH KỸ THUẬT CHI TIẾT

Phần này mô tả chi tiết 4 module AI chính, cách chúng vận hành và các thuật toán **$State-of-the-art$** được áp dụng để đảm bảo độ chính xác tối ưu trong môi trường nhà hàng phức tạp (ánh sáng thay đổi, khói bếp, mật độ người cao).

### 2.1. Module 1: AI Biometric Attendance & Evolution (Chấm công & Theo dõi biến dạng)

Khác với các máy chấm công tĩnh, module này sử dụng camera động tại quầy để nhận diện nhân sự một cách tự nhiên (passive identification).

* **Mục tiêu:** Chấm công chính xác, tự động cập nhật cơ sở dữ liệu khi nhân sự có sự thay đổi về ngoại hình (tăng/giảm cân, thay đổi kiểu tóc, đeo khẩu trang).
* **Kỹ thuật áp dụng:**
  * **Backbone:** Sử dụng kiến trúc **ArcFace** hoặc **MagFace** để trích xuất Vector đặc trưng (Embedding) có độ phân biệt cao.
  * **Liveness Detection:** Thuật toán rà soát các đặc điểm sinh học (chớp mắt, cử động môi) để loại bỏ rủi ro gian lận bằng ảnh chụp hoặc video từ điện thoại.
* **Sơ đồ luồng (Logic Flow):**
  > `Camera Stream` ➔ `MTCNN/YOLO-Face Detection` ➔ `Face Alignment` (Căn chỉnh trục mắt/mũi) ➔ `Feature Extraction` (Chuyển ảnh thành vector 512 chiều) ➔ `Cosine Similarity Comparison`.
  >
* **Cơ chế "Học máy liên tục" (Self-Evolution):** Nếu một nhân viên có độ khớp (Similarity Score) **$S$** thỏa mãn **$0.85 < S < 0.95$**, hệ thống sẽ tự động coi đây là một biến thể diện mạo mới và cập nhật vector này vào bộ nhớ đệm. Điều này giúp hệ thống "thuộc mặt" nhân viên ngay cả khi họ thay đổi phong cách hoặc lão hóa tự nhiên, giảm thiểu sai số xuống dưới  **0.1%** .

### 2.2. Module 2: Human Action Recognition - HAR (Phân tích hiệu suất lao động)

Đây là module quan trọng nhất để tính toán chi phí nhân sự thực tế. Nó chuyển đổi hình ảnh di chuyển thành các nhãn hành động cụ thể.

* **Mục tiêu:** Phân loại chính xác thời gian **Active** (Làm việc) và **Idle** (Ngồi chơi/Sử dụng điện thoại).
* **Kỹ thuật áp dụng:**
  * **Tracking:** Sử dụng **ByteTrack** để duy trì ID nhân viên xuyên suốt các khung hình, ngay cả khi họ bị che khuất tạm thời bởi đồ vật hoặc người khác.
  * **Pose Estimation:** Trích xuất 17-25 điểm chốt trên cơ thể (khớp tay, vai, lưng) để hiểu tư thế.
  * **Temporal Classification:** Sử dụng mô hình **SlowFast** hoặc **Video Swin Transformer** để phân tích chuỗi hành động trong khoảng thời gian **$T$**.
* **Sơ đồ luồng (Logic Flow):**
  > `Object Detection` ➔ `Multi-Object Tracking (MOT)` ➔ `Pose Estimation` ➔ `Spatio-Temporal Feature Extraction` ➔ `Softmax Classifier (Nấu ăn/Rửa bát/Dọn dẹp/Bấm điện thoại)`.
  >
* **Chỉ số đầu ra:** Hệ thống sẽ xuất ra một biểu đồ thời gian (**$Timeline$**) của từng nhân viên. Ví dụ: *Nguyễn Văn A: 8h làm việc - 1.5h Idle (45p bấm điện thoại, 45p ngồi không tại khu vực kho).*

### 2.3. Module 3: Food Quality Matching (Kiểm soát chất lượng món ăn)

Module này đóng vai trò là một chuyên gia kiểm định hình ảnh tại khu vực ra đồ.

* **Mục tiêu:** So khớp món ăn thực tế với "Master Image" (Ảnh chuẩn do đầu bếp trưởng thiết lập).
* **Kỹ thuật áp dụng:**

  * **Geometric Correction:** Sử dụng **Spatial Transformer Networks (STN)** để hiệu chỉnh góc nhìn từ camera (thường bị nghiêng hoặc méo) về góc nhìn chuẩn từ trên xuống (Top-down view).
  * **Image Understanding:** Phân tích các thành phần màu sắc, bố cục (Symmetry) và sự hiện diện của các thành phần bắt buộc (topping, nước sốt).
* **Sơ đồ luồng (Logic Flow):**

  > `Trigger (Nhân viên giơ món)` ➔ `Image Alignment` ➔ `Feature Matching` ➔ `Confidence Score Calculation` ➔ `Pass/Fail Alert`.
  >
* **Logic chấm điểm:** Nếu món ăn có độ tương đồng

  $$
  Similarity(I_{real}, I_{master}) < 0.90
  $$

  , hệ thống sẽ ngay lập tức kích hoạt đèn cảnh báo tại bếp và gửi ảnh lỗi về điện thoại quản lý.

### 2.4. Module 4: Customer Flow Analytics (Phân tích khách hàng)

Phân tích lưu lượng khách để tối ưu hóa quy trình phục vụ.

* **Mục tiêu:** Đếm khách, phân tích thời gian chờ (Dwell time) và nhận diện khách quen.
* **Kỹ thuật áp dụng:** **Re-Identification (Re-ID)** để nhận diện khách hàng xuyên suốt 2 camera mà không cần lưu trữ dữ liệu khuôn mặt (để bảo mật).
* **Sơ đồ luồng (Logic Flow):**

  > `Human Detection` ➔ `Staff Filtering` (Loại bỏ người có trong DB nhân sự) ➔ `Entry/Exit Tracking` ➔ `Dwell Time Monitoring`.
  >
* **Logic lọc nhiễu:** Để được coi là khách hàng hiệu dụng, người đó phải thỏa mãn điều kiện:

  $$
  \text{Status} = (\text{ID} \notin \text{Staff\_DB}) \land (\text{Time\_in\_Store} > 10\text{s})
  $$

  *(Điều này loại bỏ hoàn toàn việc đếm nhầm người đi ngang qua cửa hoặc shipper chỉ vào lấy đồ rồi đi ngay).*

### 2.5. Module 5: Automated Reporting Integration (Tích hợp báo cáo)

Module này là nơi tổng hợp dữ liệu từ 4 module trên để tạo ra giá trị kinh doanh.

* **Logic vận hành:** Dữ liệu từ các Module 1, 2, 3, 4 sẽ được đẩy vào một cơ sở dữ liệu trung tâm (**$Data\ Warehouse$**). Tại đây, các thuật toán phân tích tài chính sẽ tính toán:
  * **Labor Efficiency:** Tỷ lệ giữa thời gian tạo ra giá trị và thời gian có mặt.
  * **Loss Prevention:** Số tiền thất thoát do nhân viên lơ là hoặc làm sai món.
* **Đầu ra:** Báo cáo tổng hợp tự động dưới dạng Dashboard trực quan và thông báo Telegram vào cuối mỗi ca làm việc.


# PHẦN 3: MÔ HÌNH TOÁN HỌC & CÔNG THỨC QUẢN TRỊ TÀI CHÍNH

Hệ thống Camera Analyst của **DSC-Labs** chuyển đổi các hành vi định tính của nhân viên thành các con số định lượng để tính toán giá trị kinh tế thực tế.

### 3.1. Công thức tính toán Chi phí nhân sự thực tế (Actual Labor Cost - ALC)

Thông thường, nhà hàng trả lương theo thời gian chấm công (**$T_{attendance}$**). Hệ thống của chúng tôi bóc tách thời gian này để tìm ra con số thực tế mà chủ nhà hàng nên chi trả.

$$
ALC = \sum_{i=1}^{n} \left[ (T_{active, i} + T_{prep, i}) \times R_{h, i} \right]
$$

**Trong đó:**

* **$T_{active, i}$**: Tổng thời gian nhân viên **$i$** thực hiện các hành động tạo ra giá trị (nấu nướng, phục vụ, ra đồ) được AI ghi nhận.
* **$T_{prep, i}$**: Thời gian chuẩn bị hợp lệ (không phải ngồi chơi).
* **$R_{h, i}$**: Mức lương mỗi giờ của nhân viên **$i$**.

### 3.2. Chỉ số hiệu quả vận hành (Operation Efficiency Index - OEI)

Đây là chỉ số "sức khỏe" của đội ngũ nhân sự trong ca làm việc.

$$
OEI = \left( \frac{\sum T_{active}}{\sum T_{attendance}} \right) \times 100\%
$$

* **OEI > 85%:** Hệ thống vận hành tối ưu.
* **OEI < 70%:** Cảnh báo dư thừa nhân sự hoặc quy trình làm việc đang có "nút thắt cổ chai" (bottleneck).

### 3.3. Định lượng thất thoát do chất lượng món ăn (Quality Loss Estimation)

AI ghi nhận các món lỗi không đạt chuẩn và quy đổi ra số tiền lãng phí nguyên liệu (**$Wasted\ Food\ Cost$**):

$$
L_{quality} = \sum (N_{fail} \times C_{unit})
$$

* **$N_{fail}$**: Số lượng món bị AI đánh giá lỗi.
* **$C_{unit}$**: Chi phí nguyên liệu trung bình cho mỗi món.

# PHẦN 4: TIÊU CHUẨN BẢO MẬT & QUYỀN RIÊNG TƯ (SECURITY & PRIVACY)

Để đảm bảo niềm tin tuyệt đối từ phía khách hàng và tuân thủ các quy định về pháp lý, hệ thống Camera Analyst được xây dựng trên nền tảng bảo mật đa lớp:

### 4.1. Xử lý dữ liệu tại biên (Edge Computing Architecture)

* **Cơ chế:** Toàn bộ luồng dữ liệu Video nặng từ 6 camera sẽ được xử lý trực tiếp trên **Edge Server** (NVIDIA Jetson hoặc Workstation) đặt tại chính nhà hàng.
* **Lợi ích:** Hình ảnh nhạy cảm của khách hàng và nhân viên  **không bao giờ rời khỏi mạng nội bộ** . Chỉ có các Metadata (dữ liệu số như: "Nhân viên A - Active - 10:00") được mã hóa và gửi lên Cloud để tạo báo cáo. Điều này loại bỏ hoàn toàn rủi ro bị hacker can thiệp vào luồng video từ bên ngoài.

### 4.2. Công nghệ Vector hóa khuôn mặt (Face Vectorization)

* Hệ thống không lưu trữ ảnh gốc của nhân viên trong cơ sở dữ liệu dài hạn.
* Sau khi nhận diện, khuôn mặt được mã hóa thành một chuỗi số thực 512 chiều (Embedding Vector). Chuỗi số này là một chiều, không thể dịch ngược lại thành hình ảnh người thật nếu bị đánh cắp dữ liệu.

### 4.3. Quyền riêng tư của khách hàng (Privacy-by-Design)

* **Face Masking:** Đối với khách hàng, hệ thống có tùy chọn tự động làm mờ khuôn mặt ngay khi phát hiện (**$Real-time\ Blurring$**). Chúng tôi chỉ sử dụng các đặc điểm dáng người (Re-ID) để đếm lượt và tính thời gian chờ mà không thu thập đặc điểm định danh khuôn mặt của khách.
* **Data Retention Policy:** Dữ liệu video thô được ghi đè sau 7-14 ngày tùy theo dung lượng ổ cứng, chỉ các báo cáo thống kê dạng text được lưu trữ lâu dài.

### 4.4. Phân quyền truy cập đa cấp (RBAC - Role-based Access Control)

* **Level 1 (Chủ đầu tư):** Truy cập toàn bộ báo cáo tài chính, hiệu suất và video minh chứng lỗi.
* **Level 2 (Quản lý cửa hàng):** Xem báo cáo nhân sự trong ca, nhận cảnh báo lỗi món ăn real-time.
* **Level 3 (Nhân viên):** Chỉ xem được kết quả chấm công và bảng lương cá nhân qua App

# PHẦN 5: HỆ THỐNG BÁO CÁO & LỘ TRÌNH TRIỂN KHAI

### 5.1. Cấu trúc báo cáo Daily (Gửi qua Telegram/App lúc 22h00 hàng ngày)

1. **Chỉ số nhân sự:** Danh sách nhân viên đi muộn/về sớm; Tổng giờ làm thực tế.
2. **Chỉ số tài chính:** So sánh Quỹ lương lý thuyết vs Quỹ lương thực tế (giảm thiểu chi phí cho thời gian Idle).
3. **Chỉ số chất lượng:** Tỷ lệ món đạt chuẩn; Top 3 món hay bị lỗi nhất để cải thiện đầu bếp.
4. **Chỉ số khách hàng:** Tổng lượt khách; Khung giờ cao điểm; Thời gian chờ trung bình của khách trước khi có món.

### 5.2. Lộ trình triển khai (Roadmap)

* **Giai đoạn 1 (7 ngày):** Khảo sát hạ tầng mạng/điện, lắp đặt  Edge Server.
* **Giai đoạn 2 (10 ngày):** Thu thập dữ liệu Master (Ảnh món ăn mẫu, Face ID nhân viên) và huấn luyện mô hình Action Recognition theo không gian bếp thực tế.
* **Giai đoạn 3 (40 ngày):** Chạy thử nghiệm (Pilot), tinh chỉnh ngưỡng (threshold) cho việc nhận diện món ăn và hành động.
* **Giai đoạn 4:** Bàn giao, đào tạo quản lý và chính thức vận hành.

# PHẦN 6: ĐỀ XUẤT PHẦN CỨNG & PHÂN TÍCH HIỆU QUẢ KIẾN TRÚC

## 6.1. Danh mục thiết bị đề xuất (Hardware Components)

Để hệ thống vận hành ổn định cho 06 camera/nhà hàng, chúng ta sẽ kết hợp thiết bị chuyên dụng của Hikvision và bộ xử lý AI của DSC-Labs:

1. **Thiết bị nhận diện khuôn mặt (Face Recognition):** Sử dụng dòng  **Hikvision MinMoe (DS-K1T series)** .
   * *Hiệu quả:* Tự động xử lý nhận diện khuôn mặt và chống giả mạo ngay tại phần cứng, giảm tải 100% việc xử lý Face ID cho Server trung tâm. Dữ liệu trả về chỉ là ID và Timestamp (dạng text cực nhẹ).
2. **Hệ thống Camera giám sát:** Tận dụng camera IP có sẵn hoặc lắp mới dòng Hikvision 4MP/4K để đảm bảo độ nét cho module soi món ăn (Food Matching).
3. **Bộ xử lý AI (AI Inference Server):** Tùy thuộc vào phương án lựa chọn dưới đây.

## 6.2. So sánh hai phương án kiến trúc hệ thống

### Option 1: Xử lý phân tán (Distributed Processing - Edge Server tại mỗi nhà hàng)

Mỗi nhà hàng sẽ lắp đặt 01 bộ xử lý AI tại chỗ (ví dụ: NVIDIA Jetson Orin Nano hoặc Mini PC có GPU).

* **Ưu điểm:**
  * **Băng thông:** Video 4K từ 6 camera chỉ chạy trong mạng nội bộ, không tốn băng thông internet để đẩy lên Cloud.
  * **Tốc độ (Latency):** Cảnh báo món ăn lỗi hoặc hành động "ngồi chơi" gần như tức thì (**$<1s$**).
  * **Tính ổn định:** Nếu mất internet, hệ thống vẫn ghi nhận hành động và chấm công bình thường, dữ liệu sẽ đồng bộ lại khi có mạng.
  * **Bảo mật:** Hình ảnh khách hàng không bao giờ rời khỏi nhà hàng.
* **Nhược điểm:**
  * Chi phí đầu tư ban đầu (CAPEX) cao do mỗi nhà hàng cần 1 Server riêng.
  * Khó bảo trì, cập nhật Model AI đồng loạt khi có hàng trăm nhà hàng.
* **Chi phí vận hành (OPEX):** Thấp. Chủ yếu là tiền điện cho Server tại chỗ.

### Option 2: Xử lý tập trung (Centralized Processing - Một Server mạnh cho tất cả nhà hàng)

Tất cả 6 luồng camera từ mỗi nhà hàng sẽ được Stream qua internet về một Data Center trung tâm của DSC-Labs (sử dụng GPU mạnh như RTX 4090 hoặc A100).

* **Ưu điểm:**
  * **Quản lý tập trung:** Dễ dàng cập nhật, tinh chỉnh Model AI cho toàn bộ hệ thống chỉ tại 1 nơi.
  * **Chi phí phần cứng tại chỗ thấp:** Nhà hàng không cần lắp Server AI, chỉ cần Camera và thiết bị mạng.
  * **Khai thác dữ liệu:** Dễ dàng phân tích so sánh chéo hiệu quả giữa các chi nhánh ngay lập tức.
* **Nhược điểm:**
  * **Chi phí đường truyền cực cao:** Upload 6 luồng video 4K liên tục 24/7 yêu cầu gói internet doanh nghiệp cực mạnh và ổn định.
  * **Rủi ro hệ thống:** Nếu Server trung tâm hoặc đường truyền internet gặp sự cố, toàn bộ chuỗi nhà hàng sẽ mất khả năng giám sát AI.
* **Chi phí vận hành (OPEX):** Rất cao (Tiền thuê Cloud, băng thông internet, bảo trì Server tập trung).

## 6.3. Bảng phân tích chi tiết & Dự toán hiệu quả

| **Tiêu chí**                   | **Option 1: Xử lý Phân tán (Khuyên dùng)** | **Option 2: Xử lý Tập trung**          |
| -------------------------------------- | ------------------------------------------------------ | ----------------------------------------------- |
| **Thiết bị tại mỗi điểm**  | 1 Edge AI Box (NVIDIA Jetson) + Hikvision MinMoe       | Router chịu tải mạnh + Hikvision MinMoe      |
| **Xử lý Face Recognition**     | Offload qua thiết bị Hikvision                       | Offload qua thiết bị Hikvision                |
| **Xử lý Action & Food QC**     | Xử lý tại chỗ (Real-time)                          | Xử lý tại Cloud (Độ trễ cao)              |
| **Yêu cầu Internet**           | Gói cơ bản (chỉ gửi báo cáo text)               | Gói cao cấp (Upload video 24/7)               |
| **Chi phí đầu tư (CAPEX)**   | **Cao**(~15-25 triệu/điểm)                    | **Thấp**(~5-7 triệu/điểm)             |
| **Chi phí hàng tháng (OPEX)** | **Thấp**(Gần như bằng 0)                     | **Rất cao**(Thuê server & băng thông) |
| **Tính bảo mật riêng tư**   | Tuyệt đối (Local Only)                              | Thấp (Video chạy trên internet)              |
