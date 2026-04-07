from langchain_core.tools import tool

# ============================================================
# MOCK DATA
# ============================================================
FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air",       "departure": "08:30", "arrival": "09:50", "price":   890_000, "class": "economy"},
        {"airline": "Bamboo Airways",    "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "07:30", "arrival": "09:40", "price":   950_000, "class": "economy"},
        {"airline": "Bamboo Airways",    "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "13:00", "arrival": "14:20", "price":   780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "15:00", "arrival": "16:00", "price":   650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury",  "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê",    "rating": 4.5},
        {"name": "Sala Danang Beach",   "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê",    "rating": 4.3},
        {"name": "Fivitel Danang",      "stars": 3, "price_per_night":   650_000, "area": "Sơn Trà",   "rating": 4.1},
        {"name": "Memory Hostel",       "stars": 2, "price_per_night":   250_000, "area": "Hải Châu",  "rating": 4.6},
        {"name": "Christina's Homestay","stars": 2, "price_per_night":   350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort",  "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài",    "rating": 4.4},
        {"name": "Sol by Meliá",     "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort",    "stars": 3, "price_per_night":   800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel",  "stars": 2, "price_per_night":   200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel",          "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central",    "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel",   "stars": 3, "price_per_night":   550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room",    "stars": 2, "price_per_night":   180_000, "area": "Quận 1", "rating": 4.6},
    ],
}


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    try:
        # Thử tra xuôi chiều trước
        flights = FLIGHTS_DB.get((origin, destination))

        # Nếu không có, thử tra ngược chiều
        if not flights:
            flights = FLIGHTS_DB.get((destination, origin))
            if flights:
                # Hoán đổi origin/destination trong kết quả để đúng chiều
                origin, destination = destination, origin

        if not flights:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

        lines = [f"Chuyến bay từ {origin} → {destination}:\n"]
        for i, f in enumerate(flights, 1):
            price_fmt = f"{f['price']:,}đ".replace(",", ".")
            lines.append(
                f"{i}. {f['airline']} | {f['departure']} → {f['arrival']} | "
                f"{price_fmt} | Hạng: {f['class']}"
            )
        return "\n".join(lines)

    except Exception as e:
        return f"Lỗi khi tìm kiếm chuyến bay: {str(e)}"


@tool
def search_hotels(city: str, max_price_per_night: int = 99_999_999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    try:
        all_hotels = HOTELS_DB.get(city)
        if not all_hotels:
            return f"Không tìm thấy dữ liệu khách sạn tại {city}."

        # Lọc theo giá tối đa
        filtered = [h for h in all_hotels if h["price_per_night"] <= max_price_per_night]

        if not filtered:
            price_fmt = f"{max_price_per_night:,}đ".replace(",", ".")
            return (
                f"Không tìm thấy khách sạn tại {city} với giá dưới {price_fmt}/đêm. "
                f"Hãy thử tăng ngân sách."
            )

        # Sắp xếp theo rating giảm dần
        filtered.sort(key=lambda h: h["rating"], reverse=True)

        lines = [f"Khách sạn tại {city} (giá dưới {max_price_per_night:,}đ/đêm):\n".replace(",", ".")]
        for i, h in enumerate(filtered, 1):
            price_fmt = f"{h['price_per_night']:,}đ".replace(",", ".")
            stars = "⭐" * h["stars"]
            lines.append(
                f"{i}. {h['name']} {stars}\n"
                f"   Khu vực: {h['area']} | Giá: {price_fmt}/đêm | Rating: {h['rating']}/5"
            )
        return "\n".join(lines)

    except Exception as e:
        return f"Lỗi khi tìm kiếm khách sạn: {str(e)}"


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ), là số nguyên
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
      Số tiền là số nguyên, KHÔNG có dấu chấm phân cách.
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    """
    try:
        expense_dict: dict[str, int] = {}

        for item in expenses.split(","):
            item = item.strip()
            if ":" not in item:
                return f"Lỗi format: '{item}' không đúng dạng 'tên:số_tiền'."
            name, amount_str = item.split(":", 1)
            name = name.strip().replace("_", " ").title()
            try:
                amount = int(amount_str.strip())
            except ValueError:
                return f"Lỗi: '{amount_str.strip()}' không phải số nguyên hợp lệ."
            expense_dict[name] = amount

        total_expense = sum(expense_dict.values())
        remaining = total_budget - total_expense

        # Build bảng chi tiết
        lines = ["📊 Bảng chi phí:", ""]
        for name, amount in expense_dict.items():
            lines.append(f"  - {name}: {amount:,}đ".replace(",", "."))

        lines.append("")
        lines.append(f"  {'─' * 30}")
        lines.append(f"  Tổng chi:  {total_expense:,}đ".replace(",", "."))
        lines.append(f"  Ngân sách: {total_budget:,}đ".replace(",", "."))

        if remaining >= 0:
            lines.append(f"  Còn lại:   {remaining:,}đ ✅".replace(",", "."))
        else:
            lines.append(f"  Còn lại:   -{abs(remaining):,}đ ❌".replace(",", "."))
            lines.append(f"\n⚠️  Vượt ngân sách {abs(remaining):,}đ! Cần điều chỉnh.".replace(",", "."))

        return "\n".join(lines)

    except Exception as e:
        return f"Lỗi khi tính toán ngân sách: {str(e)}"