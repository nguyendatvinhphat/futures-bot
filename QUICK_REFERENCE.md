# QUICK REFERENCE - GIAO DỊCH FUTURES

## CÔNG THỨC QUAN TRỌNG

### Position Sizing
```
Position Size = (Account × Risk%) / |Entry - SL|
```

### Liquidation Price
```
LONG:  Liq = Entry × (1 - 1/Lev + 0.005)
SHORT: Liq = Entry × (1 + 1/Lev - 0.005)
```

### PnL
```
LONG:  PnL = (Exit - Entry) × Qty
SHORT: PnL = (Entry - Exit) × Qty
```

### Risk:Reward
```
R:R = TP distance / SL distance
Break-even Win Rate = 1 / (1 + R:R)
```

### Kelly Criterion
```
Kelly % = (W × R - L) / R
```

---

## BẢNG LIQUIDATION (LONG, Entry $50,000)

| Leverage | Liq Price | % giảm |
|----------|-----------|--------|
| 5x | $40,000 | 20% |
| 10x | $45,000 | 10% |
| 20x | $47,500 | 5% |
| 50x | $49,000 | 2% |
| 100x | $49,500 | 1% |

---

## BẢNG R:R vs WIN RATE

| R:R | Break-even WR |
|-----|---------------|
| 1:1 | 50% |
| 1:2 | 33% |
| 1:3 | 25% |
| 1:4 | 20% |
| 1:5 | 17% |

---

## QUY TẮC VÀNG

```
1. Risk tối đa 2% mỗi trade
2. R:R tối thiểu 1:2
3. Không > 20x leverage
4. LUÔN đặt SL
5. Không di chuyển SL xa hơn entry
6. Max 3 lệnh thua liên tiếp
7. Daily loss limit: 5%
8. Tổng risk cùng lúc: < 6%
```

---

## CHECKLIST TRƯỚC KHI VÀO LỆNH

```
□ Xu hướng HTF rõ ràng?
□ Vùng entry là S/R mạnh?
□ Có tín hiệu xác nhận?
□ R:R ≥ 1:2?
□ Funding rate OK?
□ Đã tính position size?
□ Đã tính liquidation price?
□ Đã đặt SL?
□ Risk ≤ 2%?
□ Daily loss limit chưa hit?
```

---

## PHÍ GIAO DỊCH

| Sàn | Maker | Taker |
|-----|-------|-------|
| Binance | 0.02% | 0.04% |
| Bybit | 0.02% | 0.055% |
| OKX | 0.02% | 0.05% |
