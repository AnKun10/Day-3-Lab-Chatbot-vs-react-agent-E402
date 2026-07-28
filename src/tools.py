"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Chủ đề: Trợ Lý Nắm Bắt Tính Cách & Chọn Quà Tặng Phù Hợp (Trọn bộ 10 Core Tools)
"""

import json

# ==========================================
# CƠ SỞ DỮ LIỆU SẢN PHẨM MẪU (MOCK CATALOG)
# ==========================================
MOCK_GIFT_CATALOG = [
    {
        "id": "GIFT001",
        "name": "Nến thơm tinh dầu Lavender & Gỗ Thông (Vintage Box)",
        "category": "Chill & Decor",
        "price": 350000,
        "suitable_age": "18-35",
        "gender": "Nữ",
        "personality": "Hướng nội, lãng mạn, chu đáo",
        "interests": ["đọc sách", "cà phê", "chill", "decor", "thư giãn"],
        "rating": 4.9,
        "reviews_count": 128,
        "review_summary": "Thơm dịu nhẹ, hũ thủy tinh vintage rất đẹp, đóng gói cẩn thận.",
        "in_stock": True
    },
    {
        "id": "GIFT002",
        "name": "Bộ lắp ráp Lego Architecture Thành phố Tokyo",
        "category": "Đồ chơi & Sáng tạo",
        "price": 1450000,
        "suitable_age": "15-40",
        "gender": "Tất cả",
        "personality": "Sáng tạo, tỉ mỉ, kiên nhẫn",
        "interests": ["lego", "kiến trúc", "du lịch", "mô hình", "sáng tạo"],
        "rating": 4.8,
        "reviews_count": 95,
        "review_summary": "Chi tiết siêu nét, thích hợp làm quà tặng bạn nam hoặc người thích sưu tầm.",
        "in_stock": True
    },
    {
        "id": "GIFT003",
        "name": "Tai nghe Bluetooth chống ồn Sony WH-1000XM4",
        "category": "Công nghệ & Âm thanh",
        "price": 4500000,
        "suitable_age": "20-45",
        "gender": "Tất cả",
        "personality": "Hướng ngoại, đam mê trải nghiệm, tập trung",
        "interests": ["công nghệ", "âm nhạc", "game", "du lịch", "tai nghe"],
        "rating": 5.0,
        "reviews_count": 310,
        "review_summary": "Chống ồn đỉnh cao, đeo êm tai, pin dùng 30 tiếng.",
        "in_stock": True
    },
    {
        "id": "GIFT004",
        "name": "Bình giữ nhiệt Hydro Flask Sport 750ml (Limited Edition)",
        "category": "Thể thao & Phụ kiện",
        "price": 420000,
        "suitable_age": "16-35",
        "gender": "Tất cả",
        "personality": "Năng động, thích vận động, chu đáo",
        "interests": ["du lịch", "thể thao", "gym", "phượt", "dã ngoại"],
        "rating": 4.7,
        "reviews_count": 84,
        "review_summary": "Giữ lạnh cực tốt 24h, màu sơn nhám chống trầy.",
        "in_stock": False  # Đã hết hàng để test Similar Gift Finder
    },
    {
        "id": "GIFT005",
        "name": "Bộ tách pha cà phê Pour Over bằng gốm Bát Tràng",
        "category": "Cà phê & Đồ dùng",
        "price": 550000,
        "suitable_age": "22-50",
        "gender": "Tất cả",
        "personality": "Tỉ mỉ, tinh tế, thích sự lắng đọng",
        "interests": ["cà phê", "đọc sách", "gốm sứ", "thư giãn"],
        "rating": 4.9,
        "reviews_count": 67,
        "review_summary": "Men gốm mỏng đẹp, pha cà phê vị đậm đà thanh thoát.",
        "in_stock": True
    },
    {
        "id": "GIFT006",
        "name": "Đèn đọc sách chống mỏi mắt nhãn hiệu Baseus LED",
        "category": "Học tập & Decor",
        "price": 280000,
        "suitable_age": "18-30",
        "gender": "Tất cả",
        "personality": "Hướng nội, chăm chỉ, tinh tế",
        "interests": ["đọc sách", "học tập", "công nghệ"],
        "rating": 4.6,
        "reviews_count": 42,
        "review_summary": "Ánh sáng dịu không đau mắt, kẹp sách tiện lợi.",
        "in_stock": True
    }
]

# CƠ SỞ DỮ LIỆU CỬA HÀNG MẪU (MOCK STORES)
MOCK_STORES = [
    {
        "name": "GiftShop Premium Hà Nội",
        "address": "Số 45 Phố Tràng Tiền, Quận Hoàn Kiếm, Hà Nội",
        "phone": "0988.123.456",
        "hours": "08:30 - 21:30"
    },
    {
        "name": "World Gift Center TP.HCM",
        "address": "128 Nguyễn Trãi, Quận 1, TP. Hồ Chí Minh",
        "phone": "0909.888.999",
        "hours": "09:00 - 22:00"
    },
    {
        "name": "Đà Nẵng Craft & Gift",
        "address": "76 Bạch Đằng, Quận Hải Châu, Đà Nẵng",
        "phone": "0914.555.666",
        "hours": "08:00 - 21:00"
    }
]


# ==========================================
# TRỌN BỘ 10 CORE TOOLS (GIFT ASSISTANT)
# ==========================================

def analyze_personality(text: str) -> str:
    """
    Tool 1: 🎭 Personality Analyzer
    Phân tích đặc điểm tính cách (hướng nội, hướng ngoại, tỉ mỉ, lãng mạn, chu đáo...) từ câu trả lời hoặc đoạn hội thoại.
    
    Args:
        text (str): Văn bản mô tả hoặc đoạn chat của người dùng
        
    Returns:
        str: Kết quả phân tích tính cách chi tiết
    """
    if not text or not isinstance(text, str):
        return "LỖI: Nội dung văn bản không hợp lệ."
        
    t_lower = text.lower()
    traits = []
    
    if any(k in t_lower for k in ["sách", "yên tĩnh", "chill", "một mình", "sâu lắng"]):
        traits.append("Hướng nội (Introvert) - Yêu thích không gian riêng tư, sâu sắc")
    if any(k in t_lower for k in ["bạn bè", "tiệc tùng", "du lịch", "năng động", "hoạt bát"]):
        traits.append("Hướng ngoại (Extrovert) - Thích kết nối, năng động, hào hứng với trải nghiệm mới")
    if any(k in t_lower for k in ["hoa", "thơ", "nến", "kỷ niệm", "ngọt ngào"]):
        traits.append("Lãng mạn & Chu đáo - Nhạy cảm với các giá trị tinh thần")
    if any(k in t_lower for k in ["công nghệ", "game", "lego", "mô hình", "lập trình"]):
        traits.append("Sáng tạo & Logic - Thích sự tỉ mỉ, khám phá tính năng và cấu trúc")

    if not traits:
        traits.append("Linh hoạt & Tinh tế - Tính cách hài hòa, dễ thích nghi")

    return "🎭 KẾT QUẢ PHÂN TÍCH TÍNH CÁCH (PERSONALITY ANALYZER):\n- " + "\n- ".join(traits)


def recommend_gifts(personality: str, age: int = 22, gender: str = "Tất cả", interests: str = "") -> str:
    """
    Tool 2: 💝 Gift Recommendation
    Gợi ý quà tặng dựa trên tính cách, độ tuổi, giới tính và sở thích của người nhận.
    
    Args:
        personality (str): Tính cách người nhận (Ví dụ: 'Hướng nội, chu đáo')
        age (int): Độ tuổi (Ví dụ: 22)
        gender (str): Giới tính ('Nam', 'Nữ', hoặc 'Tất cả')
        interests (str): Từ khóa sở thích (Ví dụ: 'đọc sách, cà phê')
        
    Returns:
        str: Danh sách món quà được đề xuất phù hợp nhất
    """
    try:
        age_num = int(age)
    except ValueError:
        age_num = 22
        
    p_lower = personality.lower()
    i_lower = interests.lower()
    g_lower = gender.lower()
    
    matches = []
    for item in MOCK_GIFT_CATALOG:
        score = 0
        if any(w in item["personality"].lower() for w in p_lower.split()):
            score += 3
        if any(tag in i_lower for tag in item["interests"]):
            score += 3
        if g_lower == "tất cả" or g_lower in item["gender"].lower() or item["gender"].lower() == "tất cả":
            score += 2
            
        if score > 0:
            matches.append((score, item))
            
    matches.sort(key=lambda x: x[0], reverse=True)
    if not matches:
        matches = [(1, item) for item in MOCK_GIFT_CATALOG[:3]]

    results = [
        f"- [{item['id']}] {item['name']} | Giá: {item['price']:,} VNĐ | Phù hợp: {item['personality']}"
        for _, item in matches
    ]
    return f"💝 KẾT QUẢ GỢI Ý QUÀ TẶNG (GIFT RECOMMENDATION) (Tuổi: {age_num}, Giới tính: {gender}):\n" + "\n".join(results)


def filter_by_budget(max_budget: int, min_budget: int = 0) -> str:
    """
    Tool 3: 💰 Budget Filter
    Lọc danh sách món quà trong khoảng ngân sách cho phép (VNĐ).
    
    Args:
        max_budget (int): Ngân sách tối đa (Ví dụ: 500000)
        min_budget (int): Ngân sách tối thiểu (Mặc định: 0)
        
    Returns:
        str: Danh sách món quà thỏa mãn ngân sách
    """
    try:
        max_b = int(max_budget)
        min_b = int(min_budget)
    except ValueError:
        return "LỖI: Ngân sách phải là số nguyên (VNĐ)."

    filtered = [
        f"- [{item['id']}] {item['name']} | Giá: {item['price']:,} VNĐ | Trạng thái: {'Còn hàng' if item['in_stock'] else '❌ Hết hàng'}"
        for item in MOCK_GIFT_CATALOG
        if min_b <= item["price"] <= max_b
    ]
    
    if not filtered:
        return f"⚠️ Không có món quà nào trong khoảng ngân sách từ {min_b:,}đ đến {max_b:,}đ."
        
    return f"💰 KẾT QUẢ LỌC THEO NGÂN SÁCH ({min_b:,}đ - {max_b:,}đ):\n" + "\n".join(filtered)


def detect_occasion(text: str) -> str:
    """
    Tool 4: 🎂 Occasion Detector
    Xác định dịp tặng quà từ mô tả của người dùng (Sinh nhật, Valentine, Noel, Kỷ niệm ngày cưới, Tết...).
    
    Args:
        text (str): Câu hỏi hoặc thông cảnh người dùng (Ví dụ: 'Sắp đến sinh nhật 22 tuổi bạn gái tôi')
        
    Returns:
        str: Dịp tặng quà đã xác định và gợi ý chủ đạo
    """
    if not text:
        return "LỖI: Chưa nhập thông tin dịp tặng."
        
    t_lower = text.lower()
    
    if "sinh nhật" in t_lower or "birthday" in t_lower:
        return "🎂 DỊP TẶNG QUÀ: Sinh nhật (Birthday)\n- Gợi ý chủ đạo: Món quà mang tính cá nhân hóa, thiệp chúc mừng tuổi mới."
    elif any(k in t_lower for k in ["valentine", "lễ tình nhân", "14/2"]):
        return "❤️ DỊP TẶNG QUÀ: Lễ Tình Nhân (Valentine)\n- Gợi ý chủ đạo: Món quà lãng mạn, socola, nến thơm, hoa tươi."
    elif any(k in t_lower for k in ["noel", "giáng sinh", "christmas"]):
        return "🎄 DỊP TẶNG QUÀ: Giáng Sinh (Noel)\n- Gợi ý chủ đạo: Món quà ấm áp, tông màu đỏ/xanh lá, đồ decor mùa đông."
    elif any(k in t_lower for k in ["kỷ niệm", "anniversary", "ngày cưới"]):
        return "🥂 DỊP TẶNG QUÀ: Kỷ Niệm (Anniversary)\n- Gợi ý chủ đạo: Quà tặng sang trọng, đồ đôi, trải nghiệm gắn kết."
    elif any(k in t_lower for k in ["tết", "năm mới", "new year"]):
        return "🧧 DỊP TẶNG QUÀ: Tết Nguyên Đán / Năm Mới\n- Gợi ý chủ đạo: Hộp quà sức khỏe, trà cao cấp, gốm sứ sang trọng."
    else:
        return "🎁 DỊP TẶNG QUÀ: Quà tặng bất ngờ / Ngày thường (Just Because)\n- Gợi ý chủ đạo: Món quà thiết thực, nhỏ nhắn mang niềm vui hàng ngày."


def extract_interests(text: str) -> str:
    """
    Tool 5: ❤️ Interest Extractor
    Trích xuất các từ khóa sở thích, đam mê từ hội thoại người dùng (cà phê, du lịch, công nghệ, đọc sách...).
    
    Args:
        text (str): Văn bản hội thoại
        
    Returns:
        str: Danh sách các từ khóa sở thích trích xuất
    """
    if not text:
        return "LỖI: Văn bản trống."
        
    interests_keywords = ["đọc sách", "cà phê", "công nghệ", "du lịch", "lego", "âm nhạc", "thể thao", "decor", "nến thơm", "game", "gốm sứ"]
    t_lower = text.lower()
    
    found = [kw for kw in interests_keywords if kw in t_lower]
    if not found:
        found = [w.strip() for w in text.split() if len(w.strip()) > 3][:3]
        
    return f"❤️ SỞ THÍCH TRÍCH XUẤT (INTEREST EXTRACTOR): {', '.join(found)}"


def search_products(keyword: str, category: str = "") -> str:
    """
    Tool 6: 🛒 Product Search
    Tìm kiếm sản phẩm phù hợp theo tên từ khóa hoặc danh mục trong hệ thống.
    
    Args:
        keyword (str): Từ khóa tìm kiếm (Ví dụ: 'Sony', 'Lego', 'Sách')
        category (str): Danh mục lọc bổ sung (Ví dụ: 'Công nghệ', 'Đồ chơi')
        
    Returns:
        str: Danh sách các sản phẩm tìm thấy
    """
    kw_lower = keyword.lower()
    cat_lower = category.lower()
    
    results = []
    for item in MOCK_GIFT_CATALOG:
        kw_match = not keyword or (kw_lower in item["name"].lower() or any(kw_lower in tag for tag in item["interests"]))
        cat_match = not category or (cat_lower in item["category"].lower())
        
        if kw_match and cat_match:
            status = "Còn hàng" if item["in_stock"] else "❌ Hết hàng"
            results.append(f"- [{item['id']}] {item['name']} | Giá: {item['price']:,} VNĐ | {status}")
            
    if not results:
        return f"🛒 KHÔNG TÌM THẤY sản phẩm khớp với từ khóa '{keyword}' trong danh mục '{category}'."
        
    return f"🛒 KẾT QUẢ TÌM KIẾM SẢN PHẨM ({len(results)} kết quả):\n" + "\n".join(results)


def check_reviews(product_name_or_id: str) -> str:
    """
    Tool 7: ⭐ Review Checker
    Kiểm tra điểm đánh giá ⭐, số lượng lượt review và tổng hợp đánh giá chất lượng sản phẩm.
    
    Args:
        product_name_or_id (str): Mã sản phẩm (Ví dụ: 'GIFT001') hoặc tên món quà
        
    Returns:
        str: Thông tin chi tiết đánh giá review
    """
    query = product_name_or_id.strip().upper()
    item = next((g for g in MOCK_GIFT_CATALOG if g["id"] == query or query.lower() in g["name"].lower()), None)
    
    if not item:
        return f"⚠️ Không tìm thấy dữ liệu đánh giá cho sản phẩm '{product_name_or_id}'."
        
    return (
        f"⭐ ĐÁNH GIÁ CHẤT LƯỢNG SẢN PHẨM [{item['id']}] '{item['name']}':\n"
        f"- Điểm đánh giá trung bình: ⭐ {item['rating']} / 5.0\n"
        f"- Tổng số lượt đánh giá: {item['reviews_count']} lượt mua\n"
        f"- Tổng hợp phản hồi thực tế: \"{item['review_summary']}\""
    )


def find_nearby_stores(city: str, district: str = "") -> str:
    """
    Tool 8: 📍 Store Finder
    Tìm danh sách cửa hàng quà tặng bán trực tiếp gần nhất dựa trên Thành phố / Quận huyện.
    
    Args:
        city (str): Tên Thành phố (Ví dụ: 'Hà Nội', 'TP.HCM', 'Đà Nẵng')
        district (str): Tên Quận/Huyện (Không bắt buộc)
        
    Returns:
        str: Danh sách địa chỉ cửa hàng gần nhất
    """
    c_lower = city.lower()
    matched_stores = [
        f"- 📍 {s['name']}\n  Địa chỉ: {s['address']}\n  Điện thoại: {s['phone']} | Giờ mở cửa: {s['hours']}"
        for s in MOCK_STORES
        if any(w in s["address"].lower() for w in c_lower.split())
    ]
    
    if not matched_stores:
        # Tra về toàn bộ danh sách cửa hàng
        matched_stores = [
            f"- 📍 {s['name']}\n  Địa chỉ: {s['address']}\n  Điện thoại: {s['phone']} | Giờ mở cửa: {s['hours']}"
            for s in MOCK_STORES
        ]
        
    return f"📍 DẠNG CỬA HÀNG QUÀ TẶNG GẦN BẠN ({city}):\n" + "\n\n".join(matched_stores)


def find_similar_gifts(product_id: str) -> str:
    """
    Tool 9: 🔄 Similar Gift Finder
    Tìm đề xuất các món quà tương tự (dùng khi món chính hết hàng hoặc muốn có lựa chọn thay thế cùng phân khúc).
    
    Args:
        product_id (str): Mã sản phẩm gốc (Ví dụ: 'GIFT004')
        
    Returns:
        str: Danh sách sản phẩm tương tự thay thế
    """
    p_id = product_id.strip().upper()
    target = next((g for g in MOCK_GIFT_CATALOG if g["id"] == p_id), None)
    
    if not target:
        return f"⚠️ Không tìm thấy sản phẩm gốc mã '{product_id}' để tìm món tương tự."
        
    similars = []
    for item in MOCK_GIFT_CATALOG:
        if item["id"] != p_id and item["in_stock"]:
            cat_match = item["category"] == target["category"]
            tag_match = any(t in target["interests"] for t in item["interests"])
            if cat_match or tag_match:
                similars.append(f"- [{item['id']}] {item['name']} | Giá: {item['price']:,} VNĐ | Danh mục: {item['category']}")
                
    if not similars:
        similars = [f"- [{item['id']}] {item['name']} | Giá: {item['price']:,} VNĐ" for item in MOCK_GIFT_CATALOG if item["id"] != p_id and item["in_stock"]][:2]

    return (
        f"🔄 MÓN QUÀ TƯƠNG TỰ THAY THẾ CHO [{target['id']}] '{target['name']}':\n"
        + "\n".join(similars)
    )


def suggest_gift_wrapping(occasion: str, recipient_relationship: str = "bạn gái") -> str:
    """
    Tool 10: 🎁 Wrapping Suggestion
    Gợi ý phong cách gói quà, tone màu giấy gói, kiểu nơ và mẫu thiệp chúc mừng phù hợp.
    
    Args:
        occasion (str): Dịp tặng quà (Ví dụ: 'Sinh nhật', 'Valentine', 'Noel')
        recipient_relationship (str): Mối quan hệ (Ví dụ: 'bạn gái', 'bạn trai', 'sếp')
        
    Returns:
        str: Gợi ý gói quà & mẫu thiệp chi tiết
    """
    occ_lower = occasion.lower()
    rel_lower = recipient_relationship.lower()
    
    if "valentine" in occ_lower or "người yêu" in rel_lower or "bạn gái" in rel_lower:
        style = "Gói quà Romantic Vintage: Giấy Kraft nâu nhạt, dây thừng cói thắt nơ kèm nhành hoa khô Lavender."
        color_tone = "Tone Hồng Đất & Pastel / Đỏ Vang"
        card_sample = f"\"Chúc {recipient_relationship} một ngày {occasion} rực rỡ và luôn nở nụ cười rạng rỡ trên môi! ❤️\""
    elif "sếp" in rel_lower or "đối tác" in rel_lower:
        style = "Gói quà Executive Luxury: Hộp bìa cứng màu xanh navy/đen, nơ lụa mạ kim sang trọng."
        color_tone = "Tone Xanh Navy / Đen Tuyền & Vàng Ánh Kim"
        card_sample = f"\"Kính chúc {recipient_relationship.title()} luôn dồi dào sức khỏe, thành công và gặt hái thêm nhiều thắng lợi mới! 🥂\""
    else:
        style = "Gói quà Warm Pastel: Giấy gói màu kem/pastel, nơ ruy băng lụa mềm mại."
        color_tone = "Tone Kem & Pastel Hài Hòa"
        card_sample = f"\"Chúc {recipient_relationship} một mùa {occasion} an lành, tràn ngập niềm vui và may mắn! 🎁\""

    return (
        f"🎁 GỢI Ý PHONG CÁCH GÓI QUÀ & THIỆP ({occasion.title()} - {recipient_relationship.title()}):\n"
        f"- Phong cách gói: {style}\n"
        f"- Tông màu chủ đạo: {color_tone}\n"
        f"- Mẫu thiệp gợi ý: {card_sample}"
    )


# ==========================================
# TRỌN BỘ 10 CORE TOOLS ĐƯỢC ĐĂNG KÝ
# ==========================================
AVAILABLE_TOOLS = {
    "analyze_personality": analyze_personality,
    "recommend_gifts": recommend_gifts,
    "filter_by_budget": filter_by_budget,
    "detect_occasion": detect_occasion,
    "extract_interests": extract_interests,
    "search_products": search_products,
    "check_reviews": check_reviews,
    "find_nearby_stores": find_nearby_stores,
    "find_similar_gifts": find_similar_gifts,
    "suggest_gift_wrapping": suggest_gift_wrapping,
}
