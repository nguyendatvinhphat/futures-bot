# BỘ KIẾN THỨC GIAO DỊCH CRYPTO FUTURES

---

## 1. RSI (RELATIVE STRENGTH INDEX)

### 1.1 Công thức tính

```
RS = Average Gain / Average Loss (trong n kỳ)

RSI = 100 - (100 / (1 + RS))

- Kỳ mặc định: 14 (14 nến)
- RSI dao động từ 0 đến 100
```

**Cách tính chi tiết:**
- Lấy giá đóng cửa của mỗi nến, tính sự thay đổi so với nến trước
- Tách thành 2 nhóm: lợi nhuận (gain) và tổn thất (loss)
- Tính trung bình động của gain và loss trong n kỳ
- RS = Average Gain / Average Loss
- RSI = 100 - (100 / (1 + RS))

### 1.2 Cách diễn giải

| Vùng RSI | Ý nghĩa | Hành động |
|-----------|----------|-----------|
| RSI > 70 | Quá mua (Overbought) | Cân nhắc bán/chốt lời |
| RSI < 30 | Quá bán (Oversold) | Cân nhắc mua |
| RSI = 50 | Trung tính | Không có xu hướng rõ |
| RSI > 50 | Phe mua đang kiểm soát | Ưu tiên lệnh LONG |
| RSI < 50 | Phe bán đang kiểm soát | Ưu tiên lệnh SHORT |

### 1.3 Phân kỳ RSI (Divergence)

**Phân kỳ dương (Bullish Divergence):**
- Giá tạo đáy thấp hơn (Lower Low) nhưng RSI tạo đáy cao hơn (Higher Low)
- Tín hiệu: Xu hướng giảm có thể kết thúc, chuẩn bị đảo chiều tăng
- Độ tin cậy cao khi xuất hiện ở vùng RSI < 30

**Phân kỳ âm (Bearish Divergence):**
- Giá tạo đỉnh cao hơn (Higher High) nhưng RSI tạo đỉnh thấp hơn (Lower High)
- Tín hiệu: Xu hướng tăng có thể kết thúc, chuẩn bị đảo chiều giảm
- Độ tin cậy cao khi xuất hiện ở vùng RSI > 70

**Phân kỳ ẩn (Hidden Divergence):**
- **Hidden Bullish**: Giá tạo đáy cao hơn nhưng RSI tạo đáy thấp hơn → Xu hướng tiếp tục tăng
- **Hidden Bearish**: Giá tạo đỉnh thấp hơn nhưng RSI tạo đỉnh cao hơn → Xu hướng tiếp tục giảm

### 1.4 Failure Swings (Thất bại dao động)

**Bullish Failure Swing:**
1. RSI giảm xuống dưới 30 (quá bán)
2. RSI hồi phục lên trên 30
3. RSI pullback nhưng KHÔNG giảm xuống dưới đáy trước đó
4. RSI phá vỡ đỉnh hồi phục trước đó → TÍN HIỆU MUA

**Bearish Failure Swing:**
1. RSI tăng lên trên 70 (quá mua)
2. RSI giảm xuống dưới 70
3. RSI hồi phục nhưng KHÔNG vượt lên đỉnh trước đó
4. RSI phá vỡ đáy hồi phục trước đó → TÍN HIỆU BÁN

### 1.5 Tùy chỉnh theo khung thời gian

| Khung thời gian | Kỳ RSI | Vùng quá mua | Vùng quá bán |
|-----------------|--------|---------------|---------------|
| Scalping (1m-5m) | 7-9 | 80 | 20 |
| Intraday (15m-1h) | 14 | 70 | 30 |
| Swing (4h-1D) | 14 | 70 | 30 |
| Position (1W) | 21 | 65 | 35 |

**Lưu ý quan trọng cho Crypto:**
- Trong thị trường crypto mạnh (bull run), RSI có thể duy trì > 70 trong thời gian dài
- Trong bear market, RSI có thể duy trì < 30 lâu hơn bình thường
- Không nên dùng RSI đơn lẻ, cần kết hợp với volume và MA

---

## 2. MOVING AVERAGES (TRUNG BÌNH ĐỘNG)

### 2.1 Các loại Moving Average

**SMA (Simple Moving Average):**
```
SMA = (Giá1 + Giá2 + ... + GiáN) / N
```
- Mỗi nến có trọng số bằng nhau
- Chậm hơn, ít nhiễu hơn
- Phù hợp xác định xu hướng dài hạn

**EMA (Exponential Moving Average):**
```
Multiplier (Hệ số) = 2 / (N + 1)
EMA = Giá hiện tại × Multiplier + EMA trước × (1 - Multiplier)
```
- Trọng số cao hơn cho giá gần đây
- Nhanh hơn SMA, phản ứng nhanh hơn
- Phù hợp cho entry/exit ngắn hạn

**WMA (Weighted Moving Average):**
```
WMA = (Giá1×1 + Giá2×2 + ... + GiáN×N) / (1+2+...+N)
```
- Trọng số tuyến tính, nến mới nhất có trọng số cao nhất
- Nhanh hơn SMA nhưng chậm hơn EMA

### 2.2 Các đường MA quan trọng

| Đường MA | Kỳ | Ứng dụng chính |
|----------|-----|----------------|
| MA7 | 7 | Xu hướng rất ngắn hạn, scalping |
| MA20 | 20 | Xu hướng ngắn hạn (vùng hỗ trợ/kháng cự động) |
| MA50 | 50 | Xu hướng trung hạn |
| MA100 | 100 | Xu hướng dài hạn |
| MA200 | 200 | Xu hướng rất dài hạn, xác định bull/bear market |

### 2.3 Golden Cross và Death Cross

**Golden Cross (Chữ thập vàng):**
- MA ngắn hạn cắt lên MA dài hạn (ví dụ: MA50 cắt lên MA200)
- Tín hiệu: Xu hướng TĂNG mạnh sắp đến
- Độ tin cậy cao hơn khi có volume tăng đột biến
- Thường dùng để xác nhận bắt đầu bull market

**Death Cross (Chữ thập tử thần):**
- MA ngắn hạn cắt xuống MA dài hạn (ví dụ: MA50 cắt xuống MA200)
- Tín hiệu: Xu hướng GIẢM mạnh sắp đến
- Thường dùng để xác nhận bắt đầu bear market

**Lưu ý:** Trong crypto, Golden/Death Cross có thể bị fake (tín hiệu giả) do biến động mạnh. Cần xác nhận thêm bằng volume và các indicator khác.

### 2.4 MA Ribbon (Dải ruy-băng MA)

Bao gồm nhiều đường MA (thường 8-10 đường) với các kỳ khác nhau:
- MA20, MA30, MA40, MA50, MA60, MA70, MA80, MA90, MA100

**Cách đọc:**
- Tất cả MA hướng lên và xếp theo thứ tự (ngắn lên trên dài) → Xu hướng TĂNG mạnh
- Tất cả MA hướng xuống và xếp theo thứ tự (ngắn ở dưới dài) → Xu hướng GIẢM mạnh
- Các MA đan xen nhau → Thị trường sideway, không rõ xu hướng
- Ribbon mở rộng → Momentum mạnh
- Ribbon co lại → Momentum yếu, có thể sắp đảo chiều

### 2.5 Dynamic Support/Resistance (Hỗ trợ/Kháng cự động)

- **Uptrend**: MA đóng vai trò HỖ TRỢ ĐỘNG → Giá pullback về MA rồi bật lên
- **Downtrend**: MA đóng vai trò KHÁNG CỰ ĐỘNG → Giá hồi phục đến MA rồi bị từ chối

**Cách giao dịch:**
- Trong uptrend: Chờ giá pullback về MA20/MA50 → Buy
- Trong downtrend: Chờ giá hồi phục đến MA20/MA50 → Sell
- Stop loss đặt dưới MA (cho lệnh Buy) hoặc trên MA (cho lệnh Sell)

### 2.6 Timeframe Confluence (Hội tụ đa khung thời gian)

Khi cùng một đường MA đóng vai trò hỗ trợ/kháng cự trên NHIỀU khung thời gian:
- Ví dụ: MA50 trên khung 4H trùng với MA50 trên khung 1D
- Độ tin cậy GẤP ĐÔI so với chỉ 1 khung thời gian
- Đây là vùng giá quan trọng, thường tạo phản ứng mạnh

---

## 3. PHÂN TÍCH VOLUME

### 3.1 Volume Profile (Hồ sơ khối lượng)

Volume Profile hiển thị khối lượng giao dịch tại MỨC GIÁ CỤ THỂ (không phải theo thời gian).

**Các thành phần quan trọng:**
- **POC (Point of Control)**: Mức giá có volume giao dịch nhiều nhất → Vùng cân bằng
- **Value Area (VA)**: Khu vực chứa 70% volume (1 độ lệch chuẩn)
- **VAH (Value Area High)**: Giới hạn trên của vùng giá trị
- **VAL (Value Area Low)**: Giới hạn dưới của vùng giá trị
- **HVN (High Volume Node)**: Mức giá có volume cao → Vùng giá mạnh, khó phá vỡ
- **LVN (Low Volume Node)**: Mức giá có volume thấp → Vùng giá yếu, giá di chuyển nhanh qua

**Ứng dụng:**
- Giá có xu hướng quay lại POC sau khi breakout
- HVN = Hỗ trợ/Kháng cự mạnh
- LVN = Giá di chuyển nhanh, có thể dùng để xác định target
- Giá ở trên VAH → Bullish bias
- Giá ở dưới VAL → Bearish bias

### 3.2 OBV (On-Balance Volume)

```
Nếu giá đóng cửa > giá đóng cửa trước: OBV = OBV trước + Volume hiện tại
Nếu giá đóng cửa < giá đóng cửa trước: OBV = OBV trước - Volume hiện tại
Nếu giá đóng cửa = giá đóng cửa trước: OBV = OBV trước
```

**Cách sử dụng:**
- OBV tăng → Áp lực mua đang tăng (accumulation)
- OBV giảm → Áp lực bán đang tăng (distribution)
- **Phân kỳ Bullish**: Giá giảm nhưng OBV tăng → Sắp đảo chiều tăng
- **Phân kỳ Bearish**: Giá tăng nhưng OBV giảm → Sắp đảo chiều giảm
- OBV phá vỡ đỉnh trước → Giá có thể cũng sẽ phá vỡ đỉnh

### 3.3 VWAP (Volume Weighted Average Price)

```
VWAP = Σ(Price × Volume) / Σ(Volume)

Price = (High + Low + Close) / 3 (Typical Price)
```

**Cách sử dụng:**
- Giá > VWAP → Bullish trong ngày (session)
- Giá < VWAP → Bearish trong ngày
- VWAP đóng vai trò hỗ trợ/kháng cự động quan trọng
- **VWAP Bands** (dải VWAP): Giống Bollinger Bands nhưng dùng VWAP thay vì SMA

**Ứng dụng trong Futures:**
- Giá test VWAP từ trên xuống → Vùng Buy tiềm năng
- Giá test VWAP từ dưới lên → Vùng Sell tiềm năng
- Giá cách xa VWAP → Có khả năng quay lại VWAP (mean reversion)

### 3.4 Climax Volume (Volume cao trào)

**Buying Climax:**
- Volume cực cao + Giá tăng mạnh + Nến thân dài
- Thường đánh dấu đỉnh ngắn hạn
- Sau đó giá thường giảm hoặc sideway

**Selling Climax:**
- Volume cực cao + Giá giảm mạnh + Nến thân dài
- Thường đánh dấu đáy ngắn hạn
- Sau đó giá thường hồi phục hoặc sideway

**Dấu hiệu nhận biết:**
- Volume gấp 2-3 lần trung bình 20 phiên
- Giá di chuyển mạnh trong 1-2 nến
- Thường xuất hiện ở cuối xu hướng

### 3.5 Accumulation/Distribution (A/D Line)

```
Money Flow Multiplier = ((Close - Low) - (High - Close)) / (High - Low)
Money Flow Volume = Money Flow Multiplier × Volume
A/D = A/D trước + Money Flow Volume
```

**Cách diễn giải:**
- A/D tăng → Đang tích lũy (accumulation), phe mua kiểm soát
- A/D giảm → Đang phân phối (distribution), phe bán kiểm soát
- Phân kỳ giữa A/D và giá → Tín hiệu đảo chiều tiềm năng

---

## 4. XU HƯỚNG THỊ TRƯỜNG (MARKET TREND)

### 4.1 Phương pháp xác định xu hướng

**Phương pháp 1: Higher Highs / Higher Lows (HH/HL)**
- **Uptrend**: Đỉnh sau cao hơn đỉnh trước (HH) + Đáy sau cao hơn đáy trước (HL)
- **Downtrend**: Đỉnh sau thấp hơn đỉnh trước (LH) + Đáy sau thấp hơn đáy trước (LL)
- **Sideway**: Không có HH/HL hoặc LH/LL rõ ràng

**Phương pháp 2: Moving Averages**
- Giá trên MA200 → Uptrend dài hạn
- Giá dưới MA200 → Downtrend dài hạn
- MA20 > MA50 > MA200 → Uptrend mạnh

**Phương pháp 3: Trendlines**
- Vẽ đường nối các đáy trong uptrend (trendline hỗ trợ)
- Vẽ đường nối các đỉnh trong downtrend (trendline kháng cự)
- Phá vỡ trendline → Có thể đảo chiều

**Phương pháp 4: Swing Highs/Lows**
- Phân tích cấu trúc swing để xác định xu hướng
- Swing high/low cao hơn → Uptrend
- Swing high/low thấp hơn → Downtrend

### 4.2 ADX (Average Directional Index) - Đo lường sức mạnh xu hướng

```
+DI = Directional Indicator dương
-DI = Directional Indicator âm
ADX = EMA của |+DI - -DI| / |+DI + -DI| × 100 (trong 14 kỳ)
```

**Cách diễn giải:**

| ADX | Sức mạnh xu hướng | Hành động |
|-----|-------------------|-----------|
| 0-15 | Không có xu hướng | Sideway, dùng range trading |
| 15-25 | Xu hướng yếu | Chờ xác nhận |
| 25-50 | Xu hướng mạnh | Giao dịch theo xu hướng |
| 50-75 | Xu hướng rất mạnh | Trend following tích cực |
| 75-100 | Xu hướng cực mạnh | Cẩn thận, có thể sắp đảo chiều |

**Kết hợp +DI và -DI:**
- +DI > -DI → Uptrend
- -DI > +DI → Downtrend
- +DI cắt lên -DI → Tín hiệu Buy
- -DI cắt lên +DI → Tín hiệu Sell

### 4.3 Các mô hình đảo chiều xu hướng

**Reversal Patterns (Mô hình đảo chiều):**
- **Head & Shoulders**: Đỉnh 3 phần (Left Shoulder - Head - Right Shoulder) → Đảo chiều từ TĂNG sang GIẢM
- **Inverse Head & Shoulders**: Ngược lại → Đảo chiều từ GIẢM sang TĂNG
- **Double Top**: 2 đỉnh bằng nhau → Bearish reversal
- **Double Bottom**: 2 đáy bằng nhau → Bullish reversal
- **Triple Top/Bottom**: 3 đỉnh/đáy → Mạnh hơn Double
- **Rounding Top/Bottom**: Đỉnh/đáy tròn → Đảo chiều từ từ

**Continuation Patterns (Mô hình tiếp diễn):**
- **Bull Flag**: Giá tăng mạnh → Sideway/consolidation → Tăng tiếp
- **Bear Flag**: Giá giảm mạnh → Sideway/consolidation → Giảm tiếp
- **Pennant**: Tam giác nhỏ sau move mạnh → Tiếp diễn
- **Ascending/Descending Triangle**: Tam giác → Breakout theo hướng của tam giác

---

## 5. ÁP LỰC MUA/BÁN (BUY/SELL PRESSURE)

### 5.1 Order Flow (Dòng lệnh)

**Khái niệm:**
- Phân tích từng lệnh giao dịch để hiểu hành vi của market participants
- Distinguish giữa aggressive buyers (market buy) và aggressive sellers (market sell)

**Các thành phần:**
- **Market Buy**: Lệnh mua chủ động (trả giá cao hơn) → Áp lực mua
- **Market Sell**: Lệnh bán chủ động (chấp nhận giá thấp hơn) → Áp lực bán
- **Limit Buy**: Lệnh mua chờ (đặt giá thấp hơn) → Hỗ trợ
- **Limit Sell**: Lệnh bán chờ (đặt giá cao hơn) → Kháng cự

### 5.2 Bid-Ask Spread

- **Spread hẹp**: Thanh khoản cao, thị trường ổn định
- **Spread rộng**: Thanh khoản thấp, thị trường biến động
- **Spread mở rộng đột ngột**: Có thể sắp có biến động lớn

**Ứng dụng:**
- Spread rất hẹp + Volume cao → Thị trường khỏe, xu hướng đáng tin cậy
- Spread rộng + Volume thấp → Cẩn thận, có thể fake breakout

### 5.3 Funding Rate (Tỷ lệ tài trợ)

**Khái niệm:**
- Phí định kỳ giữa LONG và SHORT để giữ giá futures gần giá spot
- Funding > 0: Long trả cho Short (thị trường bullish, nhiều người long)
- Funding < 0: Short trả cho Long (thị trường bearish, nhiều người short)

**Tần suất:**
- Binance: Mỗi 8 giờ (00:00, 08:00, 16:00 UTC)
- Bybit: Mỗi 8 giờ
- Một số sàn: Mỗi 1 giờ

**Cách sử dụng:**

| Funding Rate | Ý nghĩa | Hành động |
|--------------|----------|-----------|
| > 0.1% (cao) | Long quá đông | Cẩn thận, có thể bị long squeeze |
| > 0.3% (rất cao) | Long cực kỳ đông | Tín hiệu Short tiềm năng |
| < -0.1% (âm) | Short quá đông | Cẩn thận, có thể bị short squeeze |
| < -0.3% (rất âm) | Short cực kỳ đông | Tín hiệu Long tiềm năng |
| ~0% (trung tính) | Cân bằng | Không có bias rõ ràng |

### 5.4 Open Interest (OI) - Hợp đồng mở

**Khái niệm:**
- Tổng số hợp đồng futures đang được giữ (chưa đóng)
- OI tăng → Tiền mới đang chảy vào thị trường
- OI giảm → Tiền đang rút khỏi thị trường

**Phân tích kết hợp:**

| Giá | OI | Volume | Ý nghĩa |
|-----|-----|--------|----------|
| Tăng | Tăng | Tăng | Uptrend mạnh (new longs entering) |
| Tăng | Giảm | Tăng | Short covering (weak uptrend) |
| Giảm | Tăng | Tăng | Downtrend mạnh (new shorts entering) |
| Giảm | Giảm | Tăng | Long liquidation (weak downtrend) |
| Sideway | Tăng | Tăng | Tích lũy, chuẩn bị breakout |
| Sideway | Giảm | Giảm | Thiếu quan tâm, chờ catalyst |

### 5.5 Long/Short Ratio

**Khái niệm:**
- Tỷ lệ giữa số lượng lệnh Long và Short trên thị trường
- Dữ liệu từ các sàn như Binance, Bybit, OKX

**Cách sử dụng:**
- Long/Short > 1.5: Long quá đông → Contrarian: Cân nhắc Short
- Long/Short < 0.67: Short quá đông → Contrarian: Cân nhắc Long
- Tỷ lệ thay đổi đột ngột → Có thể sắp có biến động lớn

**Lưu ý:** Long/Short ratio là indicator CONTRARIAN (giao dịch ngược đám đông) trong thị trường phái sinh.

---

## 6. TÂM LÝ THỊ TRƯỜNG (MARKET SENTIMENT)

### 6.1 Fear & Greed Index

**Thang đo (0-100):**
- 0-25: Extreme Fear → Thường là đáy (cơ hội mua)
- 25-45: Fear
- 45-55: Neutral
- 55-75: Greed
- 75-100: Extreme Greed → Thường là đỉnh (cơ hội bán)

**Các thành phần:**
- Volatility (25%): Biến động giá
- Market Momentum/Volume (25%): Momentum và volume so với trung bình
- Social Media (15%): Tâm lý trên mạng xã hội
- Surveys (15%): Khảo sát nhà đầu tư
- Dominance (10%): Tỷ lệ thống trị của Bitcoin
- Trends (10%): Xu hướng tìm kiếm Google

**Ứng dụng:**
- Extreme Fear + Giá ở vùng hỗ trợ mạnh → Cơ hội MUA tốt
- Extreme Greed + Giá ở vùng kháng cự mạnh → Cơ hội BÁN tốt
- Không dùng đơn lẻ, cần kết hợp với phân tích kỹ thuật

### 6.2 Social Sentiment (Tâm lý mạng xã hội)

**Nguồn dữ liệu:**
- Twitter/X: Số lượng mention, hashtag, sentiment
- Reddit: Số bài post, comment, upvote
- Telegram: Số thành viên, tin nhắn, sentiment
- Discord: Tương tự Telegram

**Cách sử dụng:**
- Social volume tăng đột biến + Giá tăng → FOMO, có thể gần đỉnh
- Social volume tăng đột biến + Giá giảm → Panic selling, có thể gần đáy
- Social volume thấp → Thị trường ít quan tâm, có thể tích lũy

### 6.3 Whale Movements (Di chuyển của cá voi)

**Dấu hiệu whale activity:**
- Transfer lớn từ ví cá nhân → Sàn giao dịch: Có thể chuẩn bị BÁN
- Transfer lớn từ sàn giao dịch → Ví cá nhân: Có thể chuẩn bị HOLD (bullish)
- Transfer lớn giữa các sàn: Có thể arbitrage hoặc di chuyển thanh khoản
- OTC deals: Giao dịch khối lượng lớn ngoài sàn

**Công cụ theo dõi:**
- Whale Alert (Twitter)
- Blockchain explorers (Etherscan, Blockchain.com)
- Glassnode, CryptoQuant
- Coinglass (cho futures)

### 6.4 Liquidation Data (Dữ liệu thanh lý)

**Khái niệm:**
- Khi giá di chuyển ngược hướng vị thế, trader bị thanh lý (liquidation)
- Liquidation cascade: Nhiều vị thế bị thanh lý liên tiếp → Giá di chuyển mạnh hơn

**Cách sử dụng:**
- Liquidation lớn ở mức giá cụ thể → Vùng giá quan trọng
- Long liquidation cluster → Vùng hỗ trợ yếu (nếu bị phá, giá giảm mạnh)
- Short liquidation cluster → Vùng kháng cự yếu (nếu bị phá, giá tăng mạnh)
- Tổng liquidation cao → Thị trường biến động mạnh

### 6.5 CVD (Cumulative Volume Delta)

```
CVD = Σ(Volume Delta)
Volume Delta = Volume Buy - Volume Sell (tính theo từng nến)
```

**Cách diễn giải:**
- CVD tăng → Áp lực mua ròng đang tăng (bullish)
- CVD giảm → Áp lực bán ròng đang tăng (bearish)
- **Phân kỳ Bullish**: Giá giảm nhưng CVD tăng → Sắp đảo chiều tăng
- **Phân kỳ Bearish**: Giá tăng nhưng CVD giảm → Sắp đảo chiều giảm
- CVD phá vỡ đỉnh/đáy trước giá → Leading indicator

---

## 7. SMART MONEY CONCEPTS (SMC)

### 7.1 Order Blocks (Khối lệnh)

**Định nghĩa:**
- Vùng giá nơi Smart Money (tổ chức, ngân hàng) đặt lệnh lớn
- Là nến cuối cùng trước khi giá di chuyển mạnh (breakout/breakdown)

**Bullish Order Block:**
- Nến giảm cuối cùng trước khi giá tăng mạnh
- Vùng này sẽ đóng vai trò HỖ TRỢ khi giá quay lại
- Entry: Khi giá pullback về vùng OB

**Bearish Order Block:**
- Nến tăng cuối cùng trước khi giá giảm mạnh
- Vùng này sẽ đóng vai trò KHÁNG CỰ khi giá quay lại
- Entry: Khi giá hồi phục về vùng OB

**Đặc điểm OB chất lượng:**
- Có displacement (di chuyển mạnh) sau OB
- Có volume cao tại OB
- Chưa bị "mitigated" (giá chưa quay lại test)
- Ở vùng swing high/low quan trọng

### 7.2 Fair Value Gaps (FVG) - Khoảng trống giá trị hợp lý

**Định nghĩa:**
- Khoảng trống giữa 3 nến liên tiếp, nơi giá di chuyển quá nhanh
- Bullish FVG: Đáy nến 3 > Đỉnh nến 1 (khoảng trống hướng lên)
- Bearish FVG: Đỉnh nến 3 < Đáy nến 1 (khoảng trống hướng xuống)

**Cách sử dụng:**
- Giá có xu hướng quay lại FVG để "lấp đầy" (fill the gap)
- Bullish FVG → Vùng Buy khi giá pullback
- Bearish FVG → Vùng Sell khi giá hồi phục
- FVG chưa bị fill → Mục tiêu giá tiềm năng

**FVG + Order Block:**
- Khi FVG trùng với Order Block → Vùng entry CỰC MẠNH
- Đây là vùng Smart Money sẽ defend (bảo vệ)

### 7.3 Liquidity Sweeps (Quét thanh khoản)

**Khái niệm:**
- Smart Money cần thanh khoản để fill lệnh lớn
- Họ sẽ "quét" qua các vùng có nhiều stop loss để lấy thanh khoản
- Thường xảy ra ở swing high/low, round numbers

**Các loại liquidity:**
- **Buy-side Liquidity (BSL)**: Stop loss của SHORT traders (ở trên swing high)
- **Sell-side Liquidity (SSL)**: Stop loss của LONG traders (ở dưới swing low)
- **Equal Highs/Lows (EQH/EQL)**: Nhiều đỉnh/đáy bằng nhau → Nhiều stop loss tập trung

**Cách giao dịch:**
1. Xác định vùng liquidity (swing high/low, EQH/EQL)
2. Chờ giá sweep qua vùng đó (breakout giả)
3. Xác nhận reversal (pin bar, engulfing, order block)
4. Entry theo hướng ngược lại sweep

### 7.4 Breaker Blocks (Khối phá vỡ)

**Định nghĩa:**
- Order Block thất bại (failed order block) được chuyển đổi vai trò
- Bullish OB bị phá vỡ → Trở thành Bearish Breaker (kháng cự)
- Bearish OB bị phá vỡ → Trở thành Bullish Breaker (hỗ trợ)

**Đặc điểm:**
- Breaker phải có FVG bên trong hoặc liền kề
- Phải có displacement khi phá vỡ
- Độ tin cậy cao hơn OB thường vì đã được "confirm" bởi market

### 7.5 Mitigation Blocks (Khối giảm thiểu)

**Định nghĩa:**
- Order Block đã được "mitigated" (giá đã quay lại test)
- Không còn hiệu lực như Order Block nữa
- Nhưng có thể trở thành vùng consolidation

**Cách sử dụng:**
- Mitigation block → Vùng giá có thể sideway
- Không nên dùng làm entry point
- Dùng để xác định vùng giá đã được "xử lý"

### 7.6 SMC Trading Framework

**Bước 1: Xác định xu hướng**
- Higher Highs/Higher Lows → Uptrend
- Lower Highs/Lower Lows → Downtrend

**Bước 2: Tìm vùng interest**
- Order Blocks
- Fair Value Gaps
- Liquidity pools

**Bước 3: Chờ liquidity sweep**
- Giá sweep qua swing high/low
- Lấy stop loss của retail traders

**Bước 4: Xác nhận entry**
- Giá về Order Block/FVG
- Có rejection candle (pin bar, engulfing)
- Volume xác nhận

**Bước 5: Quản lý rủi ro**
- Stop loss dưới/above Order Block
- Take profit ở liquidity pool đối diện

---

## 8. QUẢN LÝ RỦI RO (RISK MANAGEMENT)

### 8.1 Position Sizing (Quy mô vị thế)

**Phương pháp 1: Fixed Percentage (Phần trăm cố định)**
```
Risk Amount = Account Balance × Risk Percentage (1-2%)
Position Size = Risk Amount / (Entry Price - Stop Loss Price)
```

**Ví dụ:**
- Account: $10,000
- Risk: 2% = $200
- Entry: $50,000 (BTC)
- Stop Loss: $49,000
- Risk per unit: $1,000
- Position Size: $200 / $1,000 = 0.2 BTC

**Phương pháp 2: Kelly Criterion**
```
Kelly % = (W × R - L) / R
W = Win rate
R = Average Win / Average Loss
L = 1 - W
```

**Lưu ý:** Nửa Kelly (Kelly / 2) thường được sử dụng để giảm rủi ro.

**Phương pháp 3: Volatility-based (Dựa trên biến động)**
```
Position Size = (Account × Risk%) / (ATR × Multiplier)
ATR = Average True Range (biến động trung bình)
```

### 8.2 Risk:Reward Ratio (Tỷ lệ R:R)

**Khái niệm:**
- R:R = Potential Profit / Potential Loss
- R:R 1:2 = Lỗ $1 khi sai, Lãi $2 khi đúng

**R:R tối thiểu khuyến nghị:**
- Scalping: 1:1.5 đến 1:2
- Intraday: 1:2 đến 1:3
- Swing: 1:3 trở lên
- Position: 1:5 trở lên

**Công thức tính break-even win rate:**
```
Break-even Win Rate = 1 / (1 + R:R)
Ví dụ: R:R 1:2 → Break-even = 1/3 = 33.3%
```

| R:R | Break-even Win Rate | Cần win bao nhiêu? |
|-----|---------------------|---------------------|
| 1:1 | 50% | 50% |
| 1:2 | 33.3% | 33.3% |
| 1:3 | 25% | 25% |
| 1:4 | 20% | 20% |
| 1:5 | 16.7% | 16.7% |

### 8.3 Trailing Stop (Dừng lỗ di động)

**Phương pháp 1: Trailing Stop theo %**
- Di chuyển stop loss theo phần trăm cố định từ giá hiện tại
- Ví dụ: Trailing 2% → Stop loss luôn cách giá hiện tại 2%

**Phương pháp 2: Trailing Stop theo ATR**
- Stop loss = Giá hiện tại - (ATR × Multiplier)
- Điều chỉnh theo biến động thực tế của thị trường
- Multiplier phổ biến: 1.5-3x ATR

**Phương pháp 3: Trailing Stop theo MA**
- Dùng MA (MA20, MA50) làm trailing stop
- Khi giá đóng cửa dưới MA → Đóng lệnh

**Phương pháp 4: Trailing Stop theo swing points**
- Di chuyển stop loss theo swing low mới (cho lệnh Long)
- Di chuyển stop loss theo swing high mới (cho lệnh Short)

### 8.4 Partial Take Profit (Chốt lời từng phần)

**Chiến lược:**
1. **TP1** (25-30% vị thế): Tại R:R 1:1 → Đảm bảo không lỗ
2. **TP2** (30-40% vị thế): Tại R:R 1:2 → Lấy lợi nhuận tốt
3. **TP3** (30-40% vị thế): Tại R:R 1:3+ hoặc trailing stop → Chạy theo trend

**Khi nào dùng:**
- Thị trường biến động mạnh
- Không chắc chắn về target
- Muốn tối ưu lợi nhuận theo trend

### 8.5 Hedging (Bảo hiểm)

**Phương pháp 1: Hedge với Futures**
- Giữ Long spot + Short futures (hoặc ngược lại)
- Giảm rủi ro khi thị trường biến động mạnh
- Tốn phí funding rate

**Phương pháp 2: Hedge với Options**
- Mua Put option để bảo vệ Long position
- Mua Call option để bảo vệ Short position
- Tốn premium nhưng giới hạn lỗ

**Phương pháp 3: Hedge với correlation**
- Long BTC + Short altcoin (hoặc ngược lại)
- Dựa trên correlation giữa các crypto

**Phương pháp 4: Delta Neutral**
- Vị thế không bị ảnh hưởng bởi biến động giá nhỏ
- Thường dùng trong DeFi yield farming

---

## 9. ĐẶC THÙ CRYPTO

### 9.1 Tác động của Funding Rate

**Funding Rate cao (dương):**
- Long đang trả phí cho Short
- Chi phí giữ vị thế Long tăng
- Có thể dẫn đến Long squeeze nếu giá giảm nhẹ
- Trader có thể đóng Long → Giá giảm thêm

**Funding Rate âm (cao):**
- Short đang trả phí cho Long
- Chi phí giữ vị thế Short tăng
- Có thể dẫn đến Short squeeze nếu giá tăng nhẹ
- Trader có thể đóng Short → Giá tăng thêm

**Funding Rate Arbitrage:**
- Mua spot + Short futures khi funding cao
- Thu funding rate mà không có rủi ro giá
- Lợi nhuận: Funding rate - Phí giao dịch

### 9.2 Liquidation Heatmaps (Bản đồ thanh lý)

**Khái niệm:**
- Hiển thị vùng giá có nhiều vị thế sẽ bị thanh lý
- Màu nóng (đỏ): Nhiều liquidation tập trung
- Màu lạnh (xanh): Ít liquidation

**Cách sử dụng:**
- Vùng liquidation lớn → Vùng giá quan trọng (magnet)
- Giá có xu hướng di chuyển đến vùng liquidation để "quét"
- Long liquidation cluster → Vùng hỗ trợ yếu (nếu bị phá → giảm mạnh)
- Short liquidation cluster → Vùng kháng cự yếu (nếu bị phá → tăng mạnh)

### 9.3 Exchange Flow (Dòng tiền ra vào sàn)

**Inflow (Dòng tiền vào sàn):**
- Crypto chuyển từ ví cá nhân → Sàn giao dịch
- Có thể chuẩn bị BÁN
- Bearish signal

**Outflow (Dòng tiền ra khỏi sàn):**
- Crypto chuyển từ sàn giao dịch → Ví cá nhân
- Có thể chuẩn bị HOLD dài hạn
- Bullish signal

**Netflow:**
- Netflow dương → Nhiều inflow hơn outflow → Bearish
- Netflow âm → Nhiều outflow hơn inflow → Bullish

### 9.4 Whale Alerts (Cảnh báo cá voi)

**Dấu hiệu whale activity:**
- Transfer > $1M từ ví → Sàn: Chuẩn bị bán
- Transfer > $1M từ sàn → Ví: Chuẩn bị hold
- Transfer > $10M: Whale accumulation/distribution
- Stablecoin inflow lớn: Chuẩn bị mua crypto

**Công cụ:**
- Whale Alert (Twitter bot)
- CryptoQuant
- Glassnode
- Nansen

---

## 10. PHÂN TÍCH ĐA KHUNG THỜI GIAN (MULTI-TIMEFRAME ANALYSIS)

### 10.1 Nguyên tắc cơ bản

**Khung thời gian cao hơn = Ưu tiên cao hơn**
- Xu hướng trên khung cao hơn sẽ chi phối
- Tín hiệu trên khung thấp hơn phải phù hợp với khung cao hơn

**Cấu trúc khuyến nghị:**

| Phong cách | Khung chính | Khung phụ | Khung vào lệnh |
|------------|-------------|-----------|----------------|
| Scalping | 1H | 15M | 1M-5M |
| Intraday | 4H | 1H | 15M |
| Swing | 1D | 4H | 1H |
| Position | 1W | 1D | 4H |

### 10.2 Quy trình phân tích đa khung

**Bước 1: Xác định xu hướng khung cao (HTF)**
- Xác định trend chính (uptrend/downtrend/sideway)
- Xác định vùng S/R quan trọng
- Xác định Order Blocks, FVG trên HTF

**Bước 2: Phân tích khung trung (MTF)**
- Xác định swing structure
- Tìm vùng interest trong xu hướng HTF
- Xác định momentum

**Bước 3: Tìm entry trên khung thấp (LTF)**
- Chờ giá về vùng interest từ HTF/MTF
- Tìm tín hiệu entry trên LTF
- Xác nhận với volume, RSI, divergence

### 10.3 Timeframe Confluence (Hội tụ đa khung)

**Ví dụ confluence mạnh:**
- MA50 trên khung 4H = $50,000
- Order Block trên khung 1H = $49,800-$50,200
- FVG trên khung 15M = $49,900-$50,100
→ Vùng $49,800-$50,200 là VÙNG CONFLUENCE MẠNH

**Các yếu tố confluence:**
- MA trên nhiều khung
- Order Block + FVG
- Fibonacci levels + S/R
- Volume Profile POC + MA
- Funding rate extremes + Technical levels

### 10.4 Cách kết hợp signals

**LONG setup mẫu (Swing trading):**

1. **HTF (Daily):**
   - Uptrend (HH/HL)
   - Giá pullback về MA50
   - RSI ~40 (oversold trong uptrend)

2. **MTF (4H):**
   - Bullish Order Block tại vùng MA50
   - FVG chưa fill
   - Volume giảm dần (accumulation)

3. **LTF (1H):**
   - Giá sweep liquidity dưới swing low
   - Bullish engulfing tại Order Block
   - RSI bullish divergence
   - Volume spike

4. **Entry:**
   - Vào lệnh Long tại Order Block
   - Stop Loss dưới swing low
   - TP1: R:R 1:1
   - TP2: R:R 1:2
   - TP3: Trailing theo swing low

**SHORT setup mẫu (Swing trading):**

1. **HTF (Daily):**
   - Downtrend (LH/LL)
   - Giá hồi phục về MA50
   - RSI ~60 (overbought trong downtrend)

2. **MTF (4H):**
   - Bearish Order Block tại vùng MA50
   - FVG chưa fill
   - Volume tăng dần (distribution)

3. **LTF (1H):**
   - Giá sweep liquidity trên swing high
   - Bearish engulfing tại Order Block
   - RSI bearish divergence
   - Volume spike

4. **Entry:**
   - Vào lệnh Short tại Order Block
   - Stop Loss trên swing high
   - TP1: R:R 1:1
   - TP2: R:R 1:2
   - TP3: Trailing theo swing high

---

## TÓM TẮT CÔNG THỨC QUAN TRỌNG

### RSI
```
RSI = 100 - (100 / (1 + RS))
RS = Average Gain / Average Loss (14 kỳ)
```

### Moving Averages
```
SMA = Σ(Price) / N
EMA = Price × (2/(N+1)) + EMA_prev × (1 - 2/(N+1))
```

### VWAP
```
VWAP = Σ(Typical Price × Volume) / Σ(Volume)
Typical Price = (High + Low + Close) / 3
```

### OBV
```
If Close > Close_prev: OBV = OBV_prev + Volume
If Close < Close_prev: OBV = OBV_prev - Volume
```

### A/D Line
```
MFM = ((Close - Low) - (High - Close)) / (High - Low)
MFV = MFM × Volume
A/D = A/D_prev + MFV
```

### Position Sizing
```
Position Size = (Account × Risk%) / |Entry - StopLoss|
```

### Break-even Win Rate
```
Break-even WR = 1 / (1 + R:R)
```

### Funding Rate Impact
```
Annualized Funding = Funding Rate × 3 × 365
```

---

## LƯU Ý QUAN TRỌNG

1. **Không indicator nào đúng 100%** - Luôn kết hợp nhiều tín hiệu
2. **Risk management là quan trọng nhất** - Bảo vệ vốn trước, kiếm lời sau
3. **Crypto biến động mạnh hơn forex/stock** - Cần stop loss rộng hơn
4. **Funding rate là chi phí thực** - Tính vào P&L
5. **Thanh lý là rủi ro lớn nhất** - Không over-leverage
6. **Tâm lý là yếu tố quyết định** - Không FOMO, không panic sell
7. **Backtest trước khi trade thật** - Kiểm tra chiến lược với dữ liệu lịch sử
8. **Journal giao dịch** - Ghi lại mọi lệnh để học hỏi
