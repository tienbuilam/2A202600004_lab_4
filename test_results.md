## ✅ Kết quả kiểm thử (Test Cases)

### Test 1 — Direct Answer (Không cần tool)

**Input:**
> "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."

**Kỳ vọng:** Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool nào.

**Kết quả:** ✅ **PASS**
- Agent trả lời trực tiếp (💬), không gọi tool.
- Hỏi lại sở thích: biển, núi, hay thành phố nhộn nhịp.

---

### Test 2 — Single Tool Call

**Input:**
> "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"

**Kỳ vọng:** Gọi `search_flights("Hà Nội", "Đà Nẵng")`, liệt kê 4 chuyến bay.

**Kết quả:** ✅ **PASS**
- Gọi đúng tool: `🔧 search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})`
- Liệt kê đầy đủ 4 chuyến bay:
  1. Vietnam Airlines | 06:00 → 07:20 | 1.450.000đ | economy
  2. Vietnam Airlines | 14:00 → 15:20 | 2.800.000đ | business
  3. VietJet Air | 08:30 → 09:50 | 890.000đ | economy
  4. Bamboo Airways | 11:00 → 12:20 | 1.200.000đ | economy

---

### Test 3 — Multi-Step Tool Chaining

**Input:**
> "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"

**Kỳ vọng:** Agent phải tự chuỗi nhiều bước:
1. `search_flights("Hà Nội", "Phú Quốc")` → tìm vé rẻ nhất (1.100.000đ)
2. `search_hotels("Phú Quốc", max_price phù hợp)` → gợi ý trong tầm giá
3. `calculate_budget(5000000, "vé_bay:1100000,khách_sạn:...")` → tính còn lại

Rồi tổng hợp thành gợi ý hoàn chỉnh với bảng chi phí.

**Kết quả:** ✅ **PASS**
- Gọi đúng 3 tool theo thứ tự:
  - `🔧 search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})`
  - `🔧 search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1900000})`
  - `🔧 calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:3000000'})`
- Chọn vé rẻ nhất: VietJet Air 1.100.000đ
- Đề xuất khách sạn trong tầm giá: Lahana Resort ⭐⭐⭐ (800.000đ/đêm)
- Bảng tổng chi phí: 2.700.000đ / 5.000.000đ → Còn lại 2.300.000đ ✅

---

### Test 4 — Missing Info / Clarification

**Input:**
> "Tôi muốn đặt khách sạn"

**Kỳ vọng:** Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách bao nhiêu? Không gọi tool vội.

**Kết quả:** ✅ **PASS**
- Agent trả lời trực tiếp (💬), không gọi tool.
- Hỏi lại thông tin cần thiết: thành phố muốn đặt và ngân sách tối đa mỗi đêm.

---

### Test 5 — Guardrail / Refusal

**Input:**
> "Giải giúp tôi bài tập lập trình Python về linked list"

**Kỳ vọng:** Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.

**Kết quả:** ✅ **PASS**
- Agent từ chối lịch sự: *"Xin lỗi, nhưng tôi là trợ lý du lịch và không thể giúp bạn với bài tập lập trình."*
- Gợi ý quay lại chủ đề du lịch.

---

## 📊 Tổng kết kết quả

| # | Test Case | Loại | Kết quả |
|---|-----------|------|---------|
| 1 | Direct Answer — Chào hỏi | Không gọi tool | ✅ Pass |
| 2 | Single Tool — Tìm chuyến bay | 1 tool call | ✅ Pass |
| 3 | Multi-Step — Tư vấn chuyến đi trọn gói | 3 tool calls (chaining) | ✅ Pass |
| 4 | Missing Info — Thiếu thông tin | Hỏi lại, không gọi tool | ✅ Pass |
| 5 | Guardrail — Yêu cầu ngoài phạm vi | Từ chối lịch sự | ✅ Pass |

**Kết quả: 5/5 test cases PASSED ✅**