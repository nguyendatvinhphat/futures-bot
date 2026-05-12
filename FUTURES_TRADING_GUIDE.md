# HƯỚNG DẪN TOÀN DIỆN GIAO DỊCH CRYPTO FUTURES

---

## MỤC LỤC

1. [Kiến Thức Cơ Bản Về Futures](#1-kiến-thức-cơ-bản-về-futures)
2. [Đòn Bẩy (Leverage)](#2-đòn-bẩy-leverage)
3. [Chiến Lược Vào Lệnh (Entry Strategies)](#3-chiến-lược-vào-lệnh-entry-strategies)
4. [Stop Loss (SL)](#4-stop-loss-sl)
5. [Take Profit (TP)](#5-take-profit-tp)
6. [Tỷ Lệ Risk:Reward (R:R)](#6-tỷ-lệ-riskreward-rr)
7. [Quy Mô Vị Thế (Position Sizing)](#7-quy-mô-vị-thế-position-sizing)
8. [Ví Dụ Giao Dịch Thực Tế](#8-ví-dụ-giao-dịch-thực-tế)
9. [Sai Lầm Thường Gặp](#9-sai-lầm-thường-gặp)
10. [Mẫu Kế Hoạch Giao Dịch](#10-mẫu-kế-hoạch-giao-dịch)

---

## 1. KIẾN THỨC CƠ BẢN VỀ FUTURES

### 1.1 Hợp Đồng Futures Là Gì?

Hợp đồng Futures là thỏa thuận mua/bán một tài sản tại **giá xác định** vào **thời điểm trong tương lai**. Trong crypto, trader không sở hữu tài sản thực mà giao dịch dựa trên **biến động giá**.

**Hai loại hợp đồng chính:**

| Loại | Thời hạn | Đặc điểm | Phù hợp |
|------|----------|-----------|---------|
| **Perpetual (Vĩnh viễn)** | Không hết hạn | Có funding rate (phí duy trì) | Giao dịch ngắn hạn, scalping, day trading |
| **Quarterly (Quý)** | 3 tháng (hết hạn theo quý) | Không có funding rate | Giao dịch trung hạn, hedging |

### 1.2 Vị Thế Long vs Short

**LONG (Mua):**
- Dự đoán giá **TĂNG**
- Mua ở giá thấp → Bán ở giá cao
- Lợi nhuận = Giá bán - Giá mua
- Rủi ro: Giá giảm → Lỗ

**SHORT (Bán):**
- Dự đoán giá **GIẢM**
- Bán ở giá cao → Mua lại ở giá thấp
- Lợi nhuận = Giá bán - Giá mua lại
- Rủi ro: Giá tăng → Lỗ

```
LONG:  Entry $50,000 → Exit $52,000 = +$2,000/lệnh (Lãi)
LONG:  Entry $50,000 → Exit $48,000 = -$2,000/lệnh (Lỗ)

SHORT: Entry $50,000 → Exit $48,000 = +$2,000/lệnh (Lãi)
SHORT: Entry $50,000 → Exit $52,000 = -$2,000/lệnh (Lỗ)
```

### 1.3 Cách Tính Lợi Nhuận / Tổn Thất (PnL)

**Công thức:**

```
LONG:  PnL = (Giá thoát - Giá vào) × Số lượng
SHORT: PnL = (Giá vào - Giá thoát) × Số lượng

PnL % = (PnL / Margin) × 100
```

**Ví dụ LONG:**
- Entry: $50,000
- Exit: $52,000
- Quantity: 0.1 BTC
- PnL = ($52,000 - $50,000) × 0.1 = **$200**

**Ví dụ SHORT:**
- Entry: $50,000
- Exit: $48,000
- Quantity: 0.1 BTC
- PnL = ($50,000 - $48,000) × 0.1 = **$200**

### 1.4 Mark Price vs Last Price

| Khái niệm | Định nghĩa | Mục đích |
|------------|-------------|----------|
| **Last Price** | Giá giao dịch cuối cùng trên sàn | Hiển thị thị trường |
| **Mark Price** | Giá tham chiếu để tính liquidation | Tránh bị thanh lý sai do manipulation |

```
Mark Price = Index Price × (1 + Funding Basis)

Funding Basis = Funding Rate × (Time until next funding / Funding interval)
```

**Tại sao Mark Price quan trọng?**
- Liquidation dựa trên **Mark Price**, KHÔNG phải Last Price
- Ngăn ngừa sàn thao túng giá để thanh lý trader
- Last Price có thể bị manipulate ngắn hạn, Mark Price ổn định hơn

### 1.5 Loại Hợp Đồng

**USDT-Margined (Ký quỹ USDT):**
- Dùng USDT làm margin
- PnL tính bằng USDT
- Dễ tính toán, dễ hiểu
- Phù hợp người mới

**Coin-Margined (Ký quỹ coin):**
- Dùng BTC/ETH làm margin
- PnL tính bằng coin
- Phù hợp holder muốn tăng số coin
- Biến động kép (giá coin + giá position)

| Đặc điểm | USDT-Margined | Coin-Margined |
|-----------|---------------|---------------|
| Margin | USDT | BTC, ETH, etc. |
| PnL | USDT | Coin |
| Tính toán | Đơn giản | Phức tạp hơn |
| Funding | Bằng USDT | Bằng coin |
| Phù hợp | Mới bắt đầu | Holder, advanced |

---

## 2. ĐÒN BẨY (LEVERAGE)

### 2.1 Đòn Bẩy Hoạt Động Như Thế Nào?

Đòn bẩy cho phép kiểm soát vị thế **LỚN HƠN** số vốn thực có.

```
Vị thế thực = Margin × Leverage

Ví dụ:
- Margin: $1,000
- Leverage: 10x
- Vị thế thực: $1,000 × 10 = $10,000
```

**Bảng đòn bẩy phổ biến:**

| Leverage | Margin cần cho $10,000 position | % biến động để liquidation |
|----------|--------------------------------|---------------------------|
| 1x | $10,000 | 100% |
| 2x | $5,000 | 50% |
| 3x | $3,333 | 33% |
| 5x | $2,000 | 20% |
| 10x | $1,000 | 10% |
| 20x | $500 | 5% |
| 25x | $400 | 4% |
| 50x | $200 | 2% |
| 75x | $133 | 1.33% |
| 100x | $100 | 1% |
| 125x | $80 | 0.8% |

### 2.2 Initial Margin vs Maintenance Margin

**Initial Margin (Margin ban đầu):**
- Số tiền cần để MỞ vị thế
- Initial Margin = Position Value / Leverage

**Maintenance Margin (Margin duy trì):**
- Số tiền tối thiểu để GIỮ vị thế
- Nếu margin < Maintenance Margin → Bị thanh lý
- Thường = 50% Initial Margin

```
Ví dụ với $10,000 position, 10x leverage:
- Initial Margin = $10,000 / 10 = $1,000
- Maintenance Margin = $1,000 × 50% = $500
- Có thể lỗ tối đa $500 trước khi bị thanh lý
```

### 2.3 Cross Margin vs Isolated Margin

| Đặc điểm | Cross Margin | Isolated Margin |
|-----------|--------------|-----------------|
| Margin pool | Toàn bộ balance | Chỉ margin của position |
| Liquidation | Chậm hơn | Nhanh hơn |
| Risk | Có thể mất toàn bộ | Chỉ mất margin position |
| Phù hợp | Hedging, advanced | Mới bắt đầu, kiểm soát rủi ro |
| Khi lỗ | Lấy từ balance | Chỉ mất margin đã đặt |

**Cross Margin:**
```
Account Balance: $10,000
Position 1: Long BTC $5,000 margin
Position 2: Short ETH $3,000 margin
→ Tất cả $10,000 đều được dùng làm margin
→ Nếu Position 1 lỗ, lấy từ Position 2 hoặc balance
```

**Isolated Margin:**
```
Account Balance: $10,000
Position: Long BTC $1,000 margin (10x)
→ Chỉ $1,000 được dùng làm margin
→ Nếu lỗ > $1,000, bị thanh lý
→ Account vẫn còn $9,000
```

### 2.4 Cách Tính Giá Thanh Lý (Liquidation Price)

**LONG Liquidation Price:**

```
Liquidation Price = Entry Price × (1 - 1/Leverage + Maintenance Margin Rate)

Ví dụ: LONG BTC
- Entry: $50,000
- Leverage: 10x
- Maintenance Margin Rate: 0.5%

Liquidation Price = $50,000 × (1 - 1/10 + 0.005)
                  = $50,000 × (1 - 0.1 + 0.005)
                  = $50,000 × 0.905
                  = $45,250

→ Giá giảm 9.5% = bị thanh lý
```

**SHORT Liquidation Price:**

```
Liquidation Price = Entry Price × (1 + 1/Leverage - Maintenance Margin Rate)

Ví dụ: SHORT BTC
- Entry: $50,000
- Leverage: 10x
- Maintenance Margin Rate: 0.5%

Liquidation Price = $50,000 × (1 + 1/10 - 0.005)
                  = $50,000 × (1 + 0.1 - 0.005)
                  = $50,000 × 1.095
                  = $54,750

→ Giá tăng 9.5% = bị thanh lý
```

**Bảng Liquidation Price (LONG) - Entry $50,000:**

| Leverage | Liquidation Price | % giảm để thanh lý |
|----------|------------------|-------------------|
| 2x | $25,000 | 50% |
| 3x | $33,333 | 33% |
| 5x | $40,000 | 20% |
| 10x | $45,000 | 10% |
| 20x | $47,500 | 5% |
| 25x | $48,000 | 4% |
| 50x | $49,000 | 2% |
| 100x | $49,500 | 1% |
| 125x | $49,600 | 0.8% |

### 2.5 Effective Leverage vs Nominal Leverage

**Nominal Leverage:** Đòn bẩy bạn CHỌN (10x, 20x, etc.)

**Effective Leverage:** Đòn bẩy THỰC TẾ dựa trên vị thế và account

```
Effective Leverage = Position Value / Account Balance

Ví dụ:
- Account: $10,000
- Position: $50,000 (5x leverage)
- Effective Leverage = $50,000 / $10,000 = 5x

Nếu dùng 20x leverage với $500 margin:
- Position: $500 × 20 = $10,000
- Effective Leverage = $10,000 / $10,000 = 1x
```

### 2.6 Cách Chọn Đòn Bẩy Phù Hợp

| Loại giao dịch | Leverage khuyến nghị | Lý do |
|----------------|---------------------|-------|
| Scalping (1-5 phút) | 5x-20x | Cần nhanh, SL gần |
| Day Trading (1H-4H) | 3x-10x | Cân bằng risk/reward |
| Swing Trading (1D+) | 2x-5x | SL rộng hơn, ít bị thanh lý |
| Position Trading | 1x-3x | Dài hạn, biến động lớn |
| Hedging | 1x-5x | Ưu tiên bảo vệ vốn |

**Quy tắc vàng:**
```
1. Không bao giờ dùng > 10x nếu mới bắt đầu
2. Không bao giờ dùng > 20x ngay cả khi chuyên nghiệp
3. Chỉ dùng leverage cao khi SL rất gần (< 1% từ entry)
4. Luôn tính liquidation price TRƯỚC khi vào lệnh
```

### 2.7 Liquidation Formulas với Ví Dụ

**Liquidation Price (Isolated Margin):**

```
LONG:  Liq Price = Entry × (1 - 1/Lev + MaintRate)
SHORT: Liq Price = Entry × (1 + 1/Lev - MaintRate)

MaintRate thường = 0.5% (tùy sàn)
```

**Ví dụ chi tiết:**

```
LONG BTC với $500 margin, 20x leverage:
- Position = $500 × 20 = $10,000
- Entry = $50,000
- Quantity = $10,000 / $50,000 = 0.2 BTC

Liquidation Price = $50,000 × (1 - 1/20 + 0.005)
                  = $50,000 × (1 - 0.05 + 0.005)
                  = $50,000 × 0.955
                  = $47,750

→ Nếu BTC giảm xuống $47,750, bạn mất toàn bộ $500 margin
→ Giá chỉ cần giảm 4.5% để bị thanh lý
```

---

## 3. CHIẾN LƯỢC VÀO LỆNH (ENTRY STRATEGIES)

### 3.1 Market Order vs Limit Order

| Loại lệnh | Định nghĩa | Ưu điểm | Nhược điểm |
|-----------|------------|---------|------------|
| **Market Order** | Vào lệnh ngay giá thị trường | Nhanh, chắc chắn được khớp | Slippage, giá có thể khác预期 |
| **Limit Order** | Đặt giá cụ thể, chờ khớp | Giá chính xác, không slippage | Có thể không được khớp |

**Khi nào dùng Market Order:**
- Cần vào lệnh NGAY (breakout đang xảy ra)
- Thị trường thanh khoản cao (spread hẹp)
- Scalping, cần tốc độ

**Khi nào dùng Limit Order:**
- Chờ pullback về vùng giá cụ thể
- Swing trading, không cần vào ngay
- Thị trường biến động mạnh, tránh slippage

### 3.2 Tín Hiệu Xác Nhận Vào Lệnh

**A. Candlestick Patterns (Mô hình nến):**

| Mô hình | Tín hiệu | Độ tin cậy |
|---------|----------|-----------|
| **Bullish Engulfing** | Tăng | Cao |
| **Bearish Engulfing** | Giảm | Cao |
| **Hammer** | Tăng (sau downtrend) | Trung bình |
| **Shooting Star** | Giảm (sau uptrend) | Trung bình |
| **Doji** | Không chắc chắn | Cần xác nhận |
| **Morning Star** | Tăng | Cao |
| **Evening Star** | Giảm | Cao |
| **Three White Soldiers** | Tăng mạnh | Cao |
| **Three Black Crows** | Giảm mạnh | Cao |

**B. Indicator Confluence (Hội tụ chỉ báo):**

```
LONG setup mạnh khi có TẤT CẢ:
✓ RSI < 30 (quá bán) HOẶC RSI bullish divergence
✓ Giá chạm MA50/MA200 và bật lên
✓ Volume tăng khi giá bật
✓ MACD cross up
✓ Giá ở vùng Order Block / FVG

SHORT setup mạnh khi có TẤT CẢ:
✓ RSI > 70 (quá mua) HOẶC RSI bearish divergence
✓ Giá chạm MA50/MA200 và bị từ chối
✓ Volume tăng khi giá giảm
✓ MACD cross down
✓ Giá ở vùng Order Block / FVG
```

### 3.3 Entry on Pullback (Vào lệnh khi giá hồi về)

**Nguyên tắc:**
- Trong UPTEND → Chờ giá pullback về support (MA, trendline, order block)
- Trong DOWNTREND → Chờ giá bounce về resistance

**Quy trình:**
```
1. Xác định xu hướng chính (HTF)
2. Xác định vùng support/resistance
3. Chờ giá pullback về vùng đó
4. Tìm tín hiệu xác nhận (pin bar, engulfing, volume)
5. Vào lệnh với SL dưới/above vùng đó
```

**Ví dụ LONG pullback:**
```
- BTC uptrend trên Daily
- MA50 tại $48,000
- Giá pullback về $48,500
- Nến hammer tại MA50 + Volume spike
- Entry: $48,500
- SL: $47,500 (dưới MA50)
- TP1: $50,500 (R:R 1:2)
- TP2: $52,500 (R:R 1:4)
```

### 3.4 Entry on Breakout (Vào lệnh khi giá phá vỡ)

**Nguyên tắc:**
- Chờ giá phá vỡ resistance (LONG) hoặc support (SHORT)
- Xác nhận bằng volume (volume phải CAO HƠN trung bình)
- Retest sau breakout là entry tốt nhất

**Quy trình:**
```
1. Xác định vùng resistance/support mạnh
2. Chờ giá phá vỡ với volume cao
3. Chờ giá retest vùng vừa phá
4. Vào lệnh khi retest thành công
5. SL dưới/above vùng breakout
```

**Ví dụ SHORT breakdown:**
```
- ETH support tại $3,000
- Giá phá xuống $2,950 với volume cao
- Chờ retest $3,000 (giờ là resistance)
- Giá retest $3,000 và bị từ chối
- Entry: $2,980
- SL: $3,100 (trên resistance)
- TP1: $2,780 (R:R 1:1.7)
- TP2: $2,580 (R:R 1:3.3)
```

### 3.5 Entry on EMA Crossover với RSI Filter

**Setup:**
```
EMA 9 cắt lên EMA 21 (LONG signal)
+ RSI > 50 (xác nhận momentum)
+ Volume tăng
→ ENTRY LONG

EMA 9 cắt xuống EMA 21 (SHORT signal)
+ RSI < 50 (xác nhận momentum)
+ Volume tăng
→ ENTRY SHORT
```

**Ví dụ:**
```
- BTC 1H chart
- EMA 9 = $49,500, EMA 21 = $49,400
- EMA 9 cắt lên EMA 21
- RSI = 55 (trên 50)
- Volume = 1.5x trung bình
- Entry: $49,500
- SL: $49,000 (dưới EMA 21)
- TP: $51,000 (R:R 1:3)
```

### 3.6 Dollar Cost Averaging (DCA) trong Futures

**Cách hoạt động:**
- Chia vốn thành nhiều phần
- Vào lệnh dần dần theo khoảng cách giá xác định
- Giảm impact của biến động ngắn hạn

**Ví dụ DCA Long BTC:**
```
Tổng vốn: $5,000
Chia 5 phần: $1,000 mỗi phần

Entry 1: $50,000 - $1,000 (10x) = $10,000 position
Entry 2: $49,000 - $1,000 (10x) = $10,000 position
Entry 3: $48,000 - $1,000 (10x) = $10,000 position
Entry 4: $47,000 - $1,000 (10x) = $10,000 position
Entry 5: $46,000 - $1,000 (10x) = $10,000 position

Average Entry = ($50,000 + $49,000 + $48,000 + $47,000 + $46,000) / 5
              = $48,000

Total Position = $50,000
Total Margin = $5,000
```

**Ưu điểm:** Giá vào trung bình tốt hơn
**Nhược điểm:** Cần nhiều vốn, có thể over-exposed

### 3.7 Scaling In Technique (Kỹ thuật vào lệnh dần)

**Khác với DCA:**
- DCA: Vào theo lịch trình cố định
- Scaling In: Vào thêm khi có tín hiệu xác nhận

**Quy trình:**
```
1. Vào lệnh 50% position ban đầu
2. Chờ tín hiệu xác nhận (breakout, volume, etc.)
3. Vào thêm 30% nếu xác nhận
4. Vào thêm 20% nếu tiếp tục xác nhận
```

**Ví dụ:**
```
BTC breakout resistance $50,000:
- Entry 1: $50,000 - 50% position (khi breakout)
- Entry 2: $50,500 - 30% position (khi retest thành công)
- Entry 3: $51,000 - 20% position (khi tiếp tục tăng)

Average Entry ≈ $50,350
```

---

## 4. STOP LOSS (SL)

### 4.1 Fixed % SL (SL cố định theo %)

**Nguyên tắc:**
- Đặt SL ở một khoảng cách % cố định từ entry
- Phù hợp cho scalping và day trading

**Bảng SL theo %:**

| Loại giao dịch | SL % | Ví dụ Entry $50,000 |
|----------------|------|---------------------|
| Scalping | 0.3-0.5% | SL $49,850 - $49,750 |
| Day Trading | 0.5-1% | SL $49,750 - $49,500 |
| Swing Trading | 1-2% | SL $49,500 - $49,000 |
| Position Trading | 2-5% | SL $49,000 - $47,500 |

### 4.2 ATR-Based SL (SL dựa trên ATR)

**Công thức:**
```
SL = Entry - (ATR × Multiplier)   [LONG]
SL = Entry + (ATR × Multiplier)   [SHORT]

ATR = Average True Range (biến động trung bình)
Multiplier = 1.5 - 3x
```

**Ví dụ:**
```
BTC ATR (14 periods) = $500
Multiplier = 2x

LONG Entry: $50,000
SL = $50,000 - ($500 × 2) = $49,000

SHORT Entry: $50,000
SL = $50,000 + ($500 × 2) = $51,000
```

**Ưu điểm:** Tự động điều chỉnh theo biến động thị trường

### 4.3 Structure-Based SL (SL dựa trên cấu trúc)

**Nguyên tắc:**
- LONG: SL dưới swing low gần nhất
- SHORT: SL trên swing high gần nhất

**Ví dụ LONG:**
```
Swing low gần nhất: $48,500
Entry: $49,000
SL: $48,400 (dưới swing low một chút)

→ Nếu giá phá swing low, cấu trúc uptrend bị phá → Thoát lệnh
```

**Ví dụ SHORT:**
```
Swing high gần nhất: $51,500
Entry: $51,000
SL: $51,600 (trên swing high một chút)

→ Nếu giá phá swing high, cấu trúc downtrend bị phá → Thoát lệnh
```

### 4.4 Trailing Stop Loss (SL di động)

**Phương pháp 1: Trailing theo %**
```
Trailing Stop = Giá hiện tại × (1 - Trailing %)

Ví dụ: Trailing 2%
- Entry $50,000 → SL $49,000
- Giá lên $52,000 → SL $50,960 (2% dưới $52,000)
- Giá lên $54,000 → SL $52,920 (2% dưới $54,000)
```

**Phương pháp 2: Trailing theo ATR**
```
Trailing SL = Giá hiện tại - (ATR × Multiplier)

Điều chỉnh mỗi khi giá tạo swing low mới (LONG)
hoặc swing high mới (SHORT)
```

**Phương pháp 3: Trailing theo MA**
```
Dùng MA20 hoặc MA50 làm trailing stop
- LONG: Khi giá đóng cửa dưới MA → Đóng lệnh
- SHORT: Khi giá đóng cửa trên MA → Đóng lệnh
```

### 4.5 Break-Even SL (Dời SL về entry)

**Nguyên tắc:**
- Khi giá đạt TP1 (R:R 1:1)
- Dời SL về entry price
- Đảm bảo không lỗ trên phần còn lại

**Ví dụ:**
```
Entry LONG: $50,000
SL: $49,000 (risk $1,000)
TP1: $51,000 (R:R 1:1) → Close 50% position
→ Dời SL về $50,000 (entry)
→ Phần còn lại chạy risk-free
```

### 4.6 Time-Based SL (SL theo thời gian)

**Nguyên tắc:**
- Nếu giá không di chuyển theo hướng预期 trong X thời gian
- Đóng lệnh (dù lãi hay lỗ)

**Ví dụ:**
```
Scalping: Nếu sau 15 phút giá không đạt TP1 → Đóng lệnh
Day Trading: Nếu sau 2H giá không đạt TP1 → Đóng lệnh
Swing Trading: Nếu sau 2 ngày giá không đạt TP1 → Đóng lệnh
```

**Lý do:**
- Vốn bị "kẹt" trong position không hiệu quả
- Có thể miss cơ hội khác
- Thị trường sideway = rủi ro

### 4.7 SL Hunting Awareness (Nhận diện săn SL)

**Dấu hiệu bị săn SL:**
```
1. Giá phá SL rồi quay lại ngay (fake breakout)
2. Volume thấp khi phá SL
3. Phá SL vào thời điểm thanh khoản thấp (Cuối tuần, đêm)
4. Phá SL ở các vùng số tròn ($50,000, $49,000)
5. Nến có râu dài (wick) phá SL
```

**Cách chống bị săn SL:**
```
1. Đặt SL cách vùng số tròn $100-200
2. Không đặt SL ở swing low/high chính xác (đặt xa hơn 0.1-0.2%)
3. Dùng Mark Price thay vì Last Price
4. Tránh vào lệnh cuối tuần hoặc trước news lớn
5. Dùng SL rộng hơn nếu leverage thấp
```

---

## 5. TAKE PROFIT (TP)

### 5.1 Chiến Lược TP1, TP2, TP3, TP4, TP5

**Mục đích:** Chốt lời dần dần, tối ưu lợi nhuận theo trend

| TP | % Close | R:R | Mục đích |
|----|---------|-----|----------|
| TP1 | 25-30% | 1:1 | Cover risk, break-even |
| TP2 | 25-30% | 1:2 | Lấy lợi nhuận tốt |
| TP3 | 20-25% | 1:3 | Chạy theo trend |
| TP4 | 15-20% | 1:4 | Tối ưu trend mạnh |
| TP5 | 10% | Trailing | Chạy đến khi bị trail out |

### 5.2 Partial Take Profit (Chốt lời từng phần)

**Ví dụ cụ thể:**

```
LONG BTC - Entry: $50,000, SL: $49,000 (Risk: $1,000)

TP1: $51,000 (R:R 1:1) → Close 30% = $300 profit
TP2: $52,000 (R:R 1:2) → Close 25% = $500 profit
TP3: $53,000 (R:R 1:3) → Close 25% = $750 profit
TP4: $54,000 (R:R 1:4) → Close 10% = $400 profit
TP5: Trailing stop → Close 10% khi bị trail out

Tổng lợi nhuận (nếu đạt tất cả TP):
= $300 + $500 + $750 + $400 + ~$200 (trailing)
= ~$2,150 (trên $1,000 risk)
= R:R ~2.15:1
```

### 5.3 TP dựa trên R:R Ratio

**Bảng TP theo R:R:**

| Risk (SL distance) | TP1 (1:1) | TP2 (1:2) | TP3 (1:3) | TP4 (1:4) | TP5 (1:5) |
|--------------------|-----------|-----------|-----------|-----------|-----------|
| $100 (0.2%) | $100 | $200 | $300 | $400 | $500 |
| $200 (0.4%) | $200 | $400 | $600 | $800 | $1,000 |
| $500 (1%) | $500 | $1,000 | $1,500 | $2,000 | $2,500 |
| $1,000 (2%) | $1,000 | $2,000 | $3,000 | $4,000 | $5,000 |

### 5.4 TP dựa trên Structure (Cấu trúc)

**LONG:**
```
TP1: Resistance gần nhất
TP2: Resistance tiếp theo
TP3: Swing high trước đó
TP4: Fibonacci extension 1.272
TP5: Fibonacci extension 1.618
```

**SHORT:**
```
TP1: Support gần nhất
TP2: Support tiếp theo
TP3: Swing low trước đó
TP4: Fibonacci extension 1.272
TP5: Fibonacci extension 1.618
```

### 5.5 TP dựa trên Fibonacci Extensions

**Công thức:**
```
Fib Extension = Swing High + (Swing High - Swing Low) × Fib Level

Các mức Fib phổ biến:
- 1.272 (127.2%)
- 1.618 (161.8%)
- 2.618 (261.8%)
```

**Ví dụ LONG:**
```
Swing Low: $48,000
Swing High: $52,000
Range: $4,000

Fib 1.272 = $52,000 + ($4,000 × 1.272) = $57,088
Fib 1.618 = $52,000 + ($4,000 × 1.618) = $58,472
Fib 2.618 = $52,000 + ($4,000 × 2.618) = $62,472
```

### 5.6 TP dựa trên Order Blocks / FVG

**LONG TP:**
```
TP1: Bearish Order Block gần nhất
TP2: Bearish FVG chưa fill
TP3: Liquidity pool (swing high có nhiều stop loss)
```

**SHORT TP:**
```
TP1: Bullish Order Block gần nhất
TP2: Bullish FVG chưa fill
TP3: Liquidity pool (swing low có nhiều stop loss)
```

### 5.7 Trailing TP Method

**Phương pháp:**
```
1. Đặt TP ban đầu ở R:R 1:2
2. Khi giá đạt TP1, dời SL về entry
3. Cho phần còn lại chạy với trailing stop
4. Trailing stop = ATR × 2 hoặc MA20
5. Khi bị trail out → Đóng toàn bộ position
```

---

## 6. TỶ LỆ RISK:REWARD (R:R)

### 6.1 Cách Tính R:R

```
R:R = Potential Profit / Potential Loss

Ví dụ:
- Entry: $50,000
- SL: $49,000 (Risk: $1,000)
- TP: $53,000 (Reward: $3,000)
- R:R = $3,000 / $1,000 = 3:1 (hoặc 1:3 theo format Risk:Reward)
```

### 6.2 Bảng R:R Examples

| Entry | SL | TP | Risk | Reward | R:R |
|-------|----|----|------|--------|-----|
| $50,000 | $49,500 | $51,000 | $500 | $1,000 | 1:2 |
| $50,000 | $49,000 | $53,000 | $1,000 | $3,000 | 1:3 |
| $50,000 | $48,000 | $56,000 | $2,000 | $6,000 | 1:3 |
| $50,000 | $49,000 | $54,000 | $1,000 | $4,000 | 1:4 |
| $50,000 | $49,500 | $52,000 | $500 | $2,000 | 1:4 |

### 6.3 Win Rate Cần Thiết Cho Từng R:R

**Công thức Break-even Win Rate:**
```
Break-even Win Rate = 1 / (1 + R:R)

Ví dụ: R:R 1:3
Win Rate cần = 1 / (1 + 3) = 1/4 = 25%
```

| R:R | Break-even Win Rate | Ví dụ: 100 trades |
|-----|---------------------|-------------------|
| 1:1 | 50% | Thắng 50, thua 50 = $0 |
| 1:1.5 | 40% | Thắng 40 × $1.5, thua 60 × $1 = $0 |
| 1:2 | 33.3% | Thắng 33 × $2, thua 67 × $1 = -$1 |
| 1:3 | 25% | Thắng 25 × $3, thua 75 × $1 = $0 |
| 1:4 | 20% | Thắng 20 × $4, thua 80 × $1 = $0 |
| 1:5 | 16.7% | Thắng 17 × $5, thua 83 × $1 = $2 |

### 6.4 Kelly Criterion (Tiêu chí Kelly)

**Công thức:**
```
Kelly % = (W × R - L) / R

Trong đó:
- W = Win rate (tỷ lệ thắng)
- R = Average Win / Average Loss
- L = 1 - W (tỷ lệ thua)

Kelly % = (W × R - (1 - W)) / R
```

**Ví dụ:**
```
Win Rate = 40% (W = 0.4)
Average Win = $3,000
Average Loss = $1,000
R = $3,000 / $1,000 = 3

Kelly % = (0.4 × 3 - 0.6) / 3
         = (1.2 - 0.6) / 3
         = 0.6 / 3
         = 0.2 = 20%

→ Nên risk 20% mỗi trade (thường dùng Half Kelly = 10%)
```

### 6.5 Expected Value Calculation

**Công thức:**
```
EV = (Win Rate × Average Win) - (Loss Rate × Average Loss)

Ví dụ:
- Win Rate = 40%
- Average Win = $3,000
- Loss Rate = 60%
- Average Loss = $1,000

EV = (0.4 × $3,000) - (0.6 × $1,000)
   = $1,200 - $600
   = $600 per trade

→ Trung bình mỗi trade lãi $600
```

### 6.6 R:R Thực Tế Cho Các Chiến Lược

| Chiến lược | R:R khuyến nghị | Win Rate cần | Thời gian giữ lệnh |
|------------|----------------|--------------|-------------------|
| Scalping | 1:1 - 1:1.5 | 50-60% | 1-15 phút |
| Day Trading | 1:2 - 1:3 | 33-50% | 1-8 giờ |
| Swing Trading | 1:3 - 1:5 | 20-33% | 1-7 ngày |
| Position Trading | 1:5 - 1:10 | 10-20% | 1 tuần - 1 tháng |

### 6.7 Bảng R:R vs Win Rate vs Expected Profit

**Giả sử: 100 trades, Risk $1,000 mỗi trade**

| R:R | Win Rate | Wins | Losses | Gross Win | Gross Loss | Net Profit | ROI |
|-----|----------|------|--------|-----------|------------|------------|-----|
| 1:1 | 55% | 55 | 45 | $55,000 | $45,000 | $10,000 | 10% |
| 1:2 | 40% | 40 | 60 | $80,000 | $60,000 | $20,000 | 20% |
| 1:3 | 30% | 30 | 70 | $90,000 | $70,000 | $20,000 | 20% |
| 1:3 | 40% | 40 | 60 | $120,000 | $60,000 | $60,000 | 60% |
| 1:4 | 25% | 25 | 75 | $100,000 | $75,000 | $25,000 | 25% |
| 1:5 | 20% | 20 | 80 | $100,000 | $80,000 | $20,000 | 20% |
| 1:5 | 30% | 30 | 70 | $150,000 | $70,000 | $80,000 | 80% |

---

## 7. QUY MÔ VỊ THẾ (POSITION SIZING)

### 7.1 Fixed Risk Method (Phương pháp risk cố định)

**Công thức:**
```
Position Size = (Account × Risk%) / (Entry - SL)

Risk Amount = Account × Risk%
Position Value = Position Size × Entry Price
```

**Quy tắc:**
```
- Risk tối đa 1-2% mỗi trade
- Không bao giờ > 5% mỗi trade
- Tổng risk cùng lúc không > 6-10%
```

### 7.2 Ví Dụ với Các Account Khác Nhau

**Ví dụ 1: Account $1,000**
```
Risk: 2% = $20
Entry LONG: $50,000
SL: $49,000 (risk $1,000 per BTC)

Position Size = $20 / $1,000 = 0.02 BTC
Position Value = 0.02 × $50,000 = $1,000
Leverage cần = $1,000 / $20 = 50x

→ Mua 0.02 BTC với $20 margin, 50x leverage
→ Nếu bị thanh lý, mất $20 (2% account)
```

**Ví dụ 2: Account $5,000**
```
Risk: 2% = $100
Entry LONG: $50,000
SL: $49,000 (risk $1,000 per BTC)

Position Size = $100 / $1,000 = 0.1 BTC
Position Value = 0.1 × $50,000 = $5,000
Leverage cần = $5,000 / $100 = 50x

→ Mua 0.1 BTC với $100 margin, 50x leverage
→ Nếu bị thanh lý, mất $100 (2% account)
```

**Ví dụ 3: Account $10,000**
```
Risk: 2% = $200
Entry LONG: $50,000
SL: $49,000 (risk $1,000 per BTC)

Position Size = $200 / $1,000 = 0.2 BTC
Position Value = 0.2 × $50,000 = $10,000
Leverage cần = $10,000 / $200 = 50x

→ Mua 0.2 BTC với $200 margin, 50x leverage
→ Nếu bị thanh lý, mất $200 (2% account)
```

### 7.3 Cách Leverage Ảnh Hưởng Đến Position Size

**Cùng $100 margin, khác leverage:**

| Leverage | Position Value | SL cần để risk $100 |
|----------|---------------|---------------------|
| 5x | $500 | 20% |
| 10x | $1,000 | 10% |
| 20x | $2,000 | 5% |
| 50x | $5,000 | 2% |
| 100x | $10,000 | 1% |

**Cùng position $10,000, khác leverage:**

| Leverage | Margin cần | SL cần để risk $200 |
|----------|------------|---------------------|
| 5x | $2,000 | 10% |
| 10x | $1,000 | 10% |
| 20x | $500 | 10% |
| 50x | $200 | 10% |

→ Leverage không thay đổi risk nếu position size và SL như nhau!

### 7.4 Max Drawdown Calculation

**Công thức:**
```
Max Drawdown = (Peak Value - Trough Value) / Peak Value × 100%

Drawdown needed to recover:
- 10% drawdown → Cần 11.1% gain
- 20% drawdown → Cần 25% gain
- 30% drawdown → Cần 42.9% gain
- 40% drawdown → Cần 66.7% gain
- 50% drawdown → Cần 100% gain
- 75% drawdown → Cần 300% gain
- 90% drawdown → Cần 900% gain
```

**Bảng Drawdown Recovery:**

| Drawdown | Gain để recovery |
|----------|-----------------|
| 5% | 5.3% |
| 10% | 11.1% |
| 15% | 17.6% |
| 20% | 25% |
| 25% | 33.3% |
| 30% | 42.9% |
| 40% | 66.7% |
| 50% | 100% |

---

## 8. VÍ DỤ GIAO DỊCH THỰC TẾ

### 8.1 Ví Dụ LONG Chi Tiết

**Setup:**
```
Cặp: BTC/USDT
Khung thời gian: 4H (Swing Trading)
Account: $10,000
Risk: 2% = $200

Phân tích:
- Uptrend trên Daily (HH, HL)
- Giá pullback về MA50 ($48,000)
- Bullish engulfing tại MA50
- RSI = 42 (quá bán trong uptrend)
- Volume spike
```

**Entry & Exit:**
```
Entry: $48,000 (Limit order tại MA50)
SL: $47,000 (dưới swing low, risk $1,000/BTC)
TP1: $50,000 (R:R 1:2) - Close 30%
TP2: $52,000 (R:R 1:4) - Close 30%
TP3: $54,000 (R:R 1:6) - Close 25%
TP4: Trailing stop - Close 15%

Position Size = $200 / $1,000 = 0.2 BTC
Position Value = 0.2 × $48,000 = $9,600
Leverage = $9,600 / $200 = 48x (dùng 50x)
```

**PnL Calculation:**
```
TP1: $50,000 - $48,000 = $2,000 × 0.06 BTC = $120
TP2: $52,000 - $48,000 = $4,000 × 0.06 BTC = $240
TP3: $54,000 - $48,000 = $6,000 × 0.05 BTC = $300
TP4: Assume $55,000 - $48,000 = $7,000 × 0.03 BTC = $210

Total Gross Profit = $120 + $240 + $300 + $210 = $870
```

**Fee Calculation:**
```
Maker Fee: 0.02% (Binance)
Taker Fee: 0.04% (Binance)

Entry Fee (Limit): $9,600 × 0.02% = $1.92
Exit Fees (Market): 
- TP1: $3,000 × 0.04% = $1.20
- TP2: $3,120 × 0.04% = $1.25
- TP3: $2,700 × 0.04% = $1.08
- TP4: $1,650 × 0.04% = $0.66

Total Fees = $1.92 + $1.20 + $1.25 + $1.08 + $0.66 = $6.11

Net Profit = $870 - $6.11 = $863.89
ROI = $863.89 / $200 (margin) = 431.9%
```

### 8.2 Ví Dụ SHORT Chi Tiết

**Setup:**
```
Cặp: ETH/USDT
Khung thời gian: 1H (Day Trading)
Account: $5,000
Risk: 2% = $100

Phân tích:
- Downtrend trên 4H (LH, LL)
- Giá hồi về Bearish Order Block ($3,200)
- Bearish engulfing tại OB
- RSI = 68 (quá mua trong downtrend)
- Volume tăng khi reject
```

**Entry & Exit:**
```
Entry: $3,200 (Market order khi confirm)
SL: $3,300 (trên OB, risk $100/ETH)
TP1: $3,000 (R:R 1:2) - Close 40%
TP2: $2,800 (R:R 1:4) - Close 35%
TP3: Trailing stop - Close 25%

Position Size = $100 / $100 = 1 ETH
Position Value = 1 × $3,200 = $3,200
Leverage = $3,200 / $100 = 32x (dùng 30x)
```

**PnL Calculation:**
```
TP1: $3,200 - $3,000 = $200 × 0.4 ETH = $80
TP2: $3,200 - $2,800 = $400 × 0.35 ETH = $140
TP3: Assume $2,600 - $3,200 = $600 × 0.25 ETH = $150

Total Gross Profit = $80 + $140 + $150 = $370
```

**Fee Calculation:**
```
Entry Fee (Market): $3,200 × 0.04% = $1.28
Exit Fees:
- TP1: $1,200 × 0.04% = $0.48
- TP2: $980 × 0.04% = $0.39
- TP3: $650 × 0.04% = $0.26

Total Fees = $1.28 + $0.48 + $0.39 + $0.26 = $2.41

Net Profit = $370 - $2.41 = $367.59
ROI = $367.59 / $100 (margin) = 367.6%
```

### 8.3 Bảng So Sánh Phí Giao Dịch

| Sàn | Maker Fee | Taker Fee | Funding (8h) |
|-----|-----------|-----------|--------------|
| Binance | 0.02% | 0.04% | 0.01% (varies) |
| Bybit | 0.02% | 0.055% | 0.01% (varies) |
| OKX | 0.02% | 0.05% | 0.01% (varies) |
| Bitget | 0.02% | 0.06% | 0.01% (varies) |

---

## 9. SAI LẦM THƯỜNG GẶP

### 9.1 Over-Leveraging (Dùng đòn bẩy quá cao)

**Vấn đề:**
```
Account $1,000
Dùng 100x leverage
Position = $100,000
SL = 0.8% từ entry

→ Chỉ cần giá đi ngược 0.8% = mất $1,000 (toàn bộ account)
→ Không có room cho error
```

**Giải pháp:**
```
- Không bao giờ > 20x leverage
- Mới bắt đầu: 3-5x
- Tính liquidation price TRƯỚC khi vào lệnh
- Đảm bảo SL xa hơn liquidation price
```

### 9.2 Không Dùng Stop Loss

**Vấn đề:**
```
Long BTC $50,000 không có SL
Flash crash: BTC giảm 20% trong 1 phút
→ Account bị thanh lý toàn bộ

Nếu có SL $49,000:
→ Lỗ $1,000 thay vì mất toàn bộ
```

**Giải pháp:**
```
- LUÔN đặt SL ngay khi vào lệnh
- Không bao giờ "hold và hy vọng"
- SL là chi phí kinh doanh, không phải thất bại
```

### 9.3 Di Chuyển SL Xa Hơn (Averaging Down)

**Vấn đề:**
```
Long BTC $50,000, SL $49,000
Giá xuống $49,500 → Di chuyển SL xuống $48,000
Giá xuống $48,500 → Di chuyển SL xuống $47,000
→ Lỗ ngày càng lớn, cuối cùng thanh lý
```

**Giải pháp:**
```
- KHÔNG BAO GIỜ di chuyển SL xa hơn entry
- Chỉ di chuyển SL về entry (break-even) hoặc theo trailing
- Nếu SL bị hit → Chấp nhận lỗ, tìm setup mới
```

### 9.4 Revenge Trading (Giao dịch trả thù)

**Vấn đề:**
```
Thua 3 lệnh liên tiếp → Muốn gỡ lại ngay
Vào lệnh lớn hơn, leverage cao hơn
→ Thua thêm, lỗ chồng lỗ
```

**Giải pháp:**
```
- Giới hạn số lệnh thua liên tiếp (max 3)
- Nghỉ 30 phút - 1 giờ sau khi thua 3 lệnh
- Quay lại với position size nhỏ hơn
- Review lại lý do thua trước khi trade tiếp
```

### 9.5 Bỏ Qua Funding Rate

**Vấn đề:**
```
Funding rate 0.1% mỗi 8 giờ
Giữ position 3 ngày = 9 lần funding
= 0.9% chi phí

Nếu profit chỉ 2% → Funding ăn mất 45% profit
```

**Giải pháp:**
```
- Check funding rate TRƯỚC khi vào lệnh
- Funding > 0.05% → Cân nhắc chờ
- Funding > 0.1% → Tránh vào lệnh
- Có thể đóng position trước funding và mở lại sau
```

### 9.6 Position Quá Lớn

**Vấn đề:**
```
Account $10,000
Vào lệnh $50,000 (5x leverage)
SL 2% = risk $1,000 (10% account)

→ Thua 10 lệnh liên tiếp = cháy account
```

**Giải pháp:**
```
- Risk tối đa 2% mỗi trade
- Tổng risk cùng lúc < 10%
- Position size nhỏ hơn = ngủ ngon hơn
```

---

## 10. MẪU KẾ HOẠCH GIAO DỊCH

### 10.1 Entry Conditions Checklist

```
□ Xu hướng HTF (Daily/4H) rõ ràng?
□ Vùng entry là support/resistance mạnh?
□ Có tín hiệu xác nhận (candlestick pattern)?
□ Indicator confluence (RSI, MA, Volume)?
□ R:R tối thiểu 1:2?
□ Funding rate < 0.05%?
□ Không có news lớn sắp tới?
□ Đã tính position size?
□ Đã tính liquidation price?
□ Đã đặt SL?
```

### 10.2 SL Placement Rules

```
LONG:
□ SL dưới swing low gần nhất
□ SL dưới Order Block/FVG
□ SL dưới MA quan trọng (MA50, MA200)
□ SL cách entry tối thiểu 0.5% (scalping) hoặc 1% (swing)
□ SL phải xa hơn liquidation price

SHORT:
□ SL trên swing high gần nhất
□ SL trên Order Block/FVG
□ SL trên MA quan trọng
□ SL cách entry tối thiểu 0.5% (scalping) hoặc 1% (swing)
□ SL phải xa hơn liquidation price
```

### 10.3 TP Targets và Partial Close Rules

```
TP1 (R:R 1:1): Close 30% → Dời SL về entry
TP2 (R:R 1:2): Close 25%
TP3 (R:R 1:3): Close 25%
TP4 (R:R 1:4): Close 10%
TP5 (Trailing): Close 10% khi bị trail out

Quy tắc:
□ KHÔNG bao giờ close toàn bộ ở TP1
□ LUÔN để phần chạy theo trend
□ Trailing stop = ATR × 2 hoặc MA20
□ Nếu hit TP1 mà không hit TP2 trong 24h → Close 50% còn lại
```

### 10.4 Maximum Risk Per Trade

```
□ Risk tối đa: 2% account
□ Không vào lệnh nếu risk > 2%
□ Nếu account < $1,000 → Risk 1%
□ Nếu account > $50,000 → Risk 1% (absolute amount quá lớn)
□ Tổng risk cùng lúc: < 6% (3 lệnh max)
```

### 10.5 Maximum Daily Loss

```
□ Daily loss limit: 5% account
□ Nếu hit daily limit → NGỪNG giao dịch trong ngày
□ Số lệnh thua liên tiếp tối đa: 3
□ Sau 3 lệnh thua → Nghỉ ít nhất 1 giờ
□ Nếu thua 2 ngày liên tiếp → Nghỉ 1 ngày
```

### 10.6 Journaling Requirements

```
Ghi lại MỖI lệnh:
□ Thời gian vào/ra
□ Cặp giao dịch
□ Long/Short
□ Entry price
□ SL price
□ TP price(s)
□ Position size
□ Leverage
□ Lý do vào lệnh (setup gì?)
□ Lý do ra lệnh (hit TP/SL/manual?)
□ PnL (dollar và %)
□ Screenshot chart khi vào và ra
□ Cảm xúc khi trade
□ Bài học rút ra

Review hàng tuần:
□ Win rate tuần này?
□ R:R trung bình?
□ Có vi phạm rule nào không?
□ Cần cải thiện điều gì?
□ Có pattern nào lặp lại không?
```

---

## BẢNG TÓM TẮT CÔNG THỨC QUAN TRỌNG

### Position Sizing
```
Position Size = (Account × Risk%) / |Entry - SL|
Position Value = Position Size × Entry Price
Leverage = Position Value / Margin
```

### Liquidation Price
```
LONG:  Liq = Entry × (1 - 1/Lev + MaintRate)
SHORT: Liq = Entry × (1 + 1/Lev - MaintRate)
```

### PnL Calculation
```
LONG:  PnL = (Exit - Entry) × Quantity
SHORT: PnL = (Entry - Exit) × Quantity
PnL % = PnL / Margin × 100
```

### Risk:Reward
```
R:R = Reward / Risk
Break-even WR = 1 / (1 + R:R)
```

### Kelly Criterion
```
Kelly % = (W × R - L) / R
W = Win Rate, R = Avg Win / Avg Loss, L = 1 - W
```

### Expected Value
```
EV = (WR × Avg Win) - (LR × Avg Loss)
```

### Drawdown Recovery
```
Recovery % = 1 / (1 - Drawdown%) - 1
```

### Funding Rate
```
Annualized = Funding Rate × 3 × 365
```

---

## LƯU Ý CUỐI CÙNG

```
1. RISK MANAGEMENT là quan trọng nhất - Bảo vệ vốn trước, kiếm lời sau
2. Không có strategy nào thắng 100% - Chấp nhận thua là một phần
3. Tâm lý quyết định 80% kết quả - Kiểm soát cảm xúc
4. Backtest trước khi trade thật - Đừng trade bằng tiền thật ngay
5. Journal mọi lệnh - Học từ sai lầm
6. Bắt đầu với leverage thấp - Tăng dần khi có kinh nghiệm
7. Không trade khi mệt mỏi, stress, hoặc sau khi thua lớn
8. Thị trường luôn ở đó - Không cần trade mỗi ngày
9. Học hỏi liên tục - Thị trường luôn thay đổi
10. Không bao giờ invest nhiều hơn số tiền có thể mất
```
