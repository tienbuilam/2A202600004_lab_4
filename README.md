# 🧳 TravelBuddy — Trợ lý Du lịch Thông minh

**MSSV:** 2A202600004 | **Lab 4** — Xây dựng AI Agent với Tool-Calling

## 📖 Giới thiệu

TravelBuddy là một AI Agent trợ lý du lịch được xây dựng bằng **LangGraph** và **GPT-4o-mini**, có khả năng tự động gọi các công cụ (tool-calling) để tìm kiếm chuyến bay, khách sạn và tính toán ngân sách cho chuyến đi trong nước Việt Nam.

Agent sử dụng kiến trúc **ReAct** (Reasoning + Acting) với vòng lặp Agent → Tool → Agent, cho phép tự động chuỗi nhiều bước xử lý liên tiếp để tư vấn chuyến đi hoàn chỉnh.

## 🏗️ Kiến trúc hệ thống

```
User Input
    ↓
┌─────────┐     ┌───────────┐
│  Agent  │────▶│   Tools   │
│ (LLM)  │◀────│  (Mock)   │
└─────────┘     └───────────┘
    ↓
Agent Response
```

- **Agent** (`agent.py`): Node chính sử dụng GPT-4o-mini với system prompt, quyết định khi nào cần gọi tool và khi nào trả lời trực tiếp.
- **Tools** (`tools.py`): 3 công cụ mock data — `search_flights`, `search_hotels`, `calculate_budget`.
- **System Prompt** (`system_prompt.txt`): Định nghĩa persona, quy tắc, hướng dẫn sử dụng tool, và các ràng buộc.

## 🛠️ Các công cụ (Tools)

| Tool | Mô tả | Tham số |
|------|--------|---------|
| `search_flights` | Tìm chuyến bay giữa 2 thành phố | `origin`, `destination` |
| `search_hotels` | Tìm khách sạn tại thành phố, lọc theo giá | `city`, `max_price_per_night` (tùy chọn) |
| `calculate_budget` | Tính ngân sách còn lại sau các khoản chi | `total_budget`, `expenses` |

**Dữ liệu hỗ trợ:** Hà Nội, Đà Nẵng, Phú Quốc, Hồ Chí Minh (chuyến bay + khách sạn mock).

## 🚀 Cài đặt & Chạy

```bash
# 1. Cài đặt dependencies
pip install langgraph langchain-openai python-dotenv

# 2. Tạo file .env với API key
echo OPENAI_API_KEY=sk-your-key > .env

# 3. Chạy agent
python agent.py
```

## 📁 Cấu trúc dự án

```
2A202600004_lab_4/
├── agent.py            # Agent chính (LangGraph + GPT-4o-mini)
├── tools.py            # 3 tools: flights, hotels, budget
├── system_prompt.txt   # System prompt với persona & rules
├── test_results.md     # Kết quả chạy thực tế
├── .env                # API key (không commit)
└── README.md           # readme
└── test_result.md      # chạy thử testcases
```
