"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Test Cases + Multi-Provider.
Chủ đề: Trợ Lý Nắm Bắt Tính Cách & Chọn Quà Tặng Phù Hợp (Trọn bộ 10 Tools)
Developer: Nguyễn Trần Nghĩa (01664)
"""

import ast
import json
import os
import re
import sys
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/ hoạt động mượt mà
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import các thành phần từ file của Role 2, Role 3 & Multi-Provider Adapter
from tools import AVAILABLE_TOOLS
from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider

load_dotenv()

def load_test_cases():
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    
    # Fallback kiểm tra nếu file ở thư mục hiện tại
    if not os.path.exists(config_path):
        config_path = "test_cases.json"
        
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_baseline_chatbot(user_query: str, provider):
    """
    Dựng Chatbot gốc (Baseline) không có công cụ.
    """
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    print(f"⚙️ System Prompt: {CHATBOT_BASELINE_PROMPT.strip()}")
    
    # Gọi LLM Provider thực hiện sinh câu trả lời
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Chatbot trả lời:\n{response}")


def parse_tool_args(raw_args: str):
    """Phân tích cú pháp tham số linh hoạt cho Tool call (hỗ trợ cả positional và kwargs)"""
    raw_args = raw_args.strip()
    if not raw_args:
        return [], {}

    kwargs = {}
    pos_args = []
    
    # Kiểm tra nếu tham số truyền dạng key=value (kwargs)
    if "=" in raw_args:
        matches = re.findall(r'(\w+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s,]+))', raw_args)
        if matches:
            for k, val_d, val_s, val_raw in matches:
                val = val_d or val_s or val_raw
                if val.isdigit():
                    val = int(val)
                kwargs[k] = val
            return pos_args, kwargs

    # Thử parse tham số bằng ast.literal_eval để giữ nguyên string chứa dấu phẩy
    try:
        parsed = ast.literal_eval(f"({raw_args})")
        if isinstance(parsed, tuple):
            pos_args = list(parsed)
        else:
            pos_args = [parsed]
        return pos_args, kwargs
    except Exception:
        # Fallback tách phẩy nếu không parse được
        args = [a.strip().strip("'\"") for a in raw_args.split(",") if a.strip()]
        return args, kwargs


def execute_tool_call(tool_name: str, raw_args: str) -> str:
    """Hàm bổ trợ thực thi Tool động từ tên tool và tham số được LLM yêu cầu"""
    tool_func = AVAILABLE_TOOLS.get(tool_name.strip())
    if not tool_func:
        return f"LỖI: Không tìm thấy công cụ '{tool_name}' trong AVAILABLE_TOOLS."
        
    pos_args, kwargs = parse_tool_args(raw_args)
    try:
        if kwargs:
            return tool_func(**kwargs)
        else:
            return tool_func(*pos_args)
    except Exception as e:
        return f"LỖI THỰC THI TOOL '{tool_name}': {str(e)}"


def run_react_agent(user_query: str, provider):
    """
    Dựng vòng lặp ReAct Agent (Thought -> Action -> Observation) có Guardrails.
    """
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    step = 0
    conversation_history = f"User Request: {user_query}\n"
    
    while step < MAX_ITERATIONS:
        step += 1
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")
        
        # Nếu đang ở Offline Mock Mode (không kết nối API key)
        if provider.__class__.__name__ == "OfflineMockProvider" or not getattr(provider, "api_key", True):
            if step == 1:
                print("🧠 Thought: Cần phân tích đặc điểm tính cách và sở thích người nhận.")
                print("🛠️ Action: analyze_personality['Nữ 22 tuổi thích đọc sách và cà phê']")
                obs = AVAILABLE_TOOLS["analyze_personality"]("Nữ 22 tuổi thích đọc sách và cà phê")
                print(f"👁️ Observation:\n{obs}")
                conversation_history += f"Step 1 Obs: {obs}\n"
                
            elif step == 2:
                print("🧠 Thought: Cần lọc món quà phù hợp với ngân sách dưới 500.000 VNĐ.")
                print("🛠️ Action: filter_by_budget[500000, 0]")
                obs = AVAILABLE_TOOLS["filter_by_budget"](500000, 0)
                print(f"👁️ Observation:\n{obs}")
                conversation_history += f"Step 2 Obs: {obs}\n"
                
            elif step == 3:
                print("🧠 Thought: Cần gợi ý gói quà và mẫu thiệp sinh nhật tinh tế.")
                print("🛠️ Action: suggest_gift_wrapping['Sinh nhật', 'bạn gái']")
                obs = AVAILABLE_TOOLS["suggest_gift_wrapping"]("Sinh nhật", "bạn gái")
                print(f"👁️ Observation:\n{obs}")
                
                print("\n🏁 Final Answer: Đề xuất tuyệt vời nhất cho bạn gái 22 tuổi hướng nội là [GIFT001] Nến thơm tinh dầu Lavender (350,000 VNĐ) hoặc [GIFT006] Đèn đọc sách chống mỏi mắt Baseus LED (280,000 VNĐ). Đi kèm phong cách gói quà Romantic Vintage với giấy Kraft nâu và nơ cói thắt cùng nhành hoa khô!")
                break
        else:
            # Chạy thực tế với Online LLM Provider (Gemini / OpenAI / OpenRouter)
            prompt = REACT_SYSTEM_PROMPT + "\n" + conversation_history
            response = provider.generate(prompt)
            print(f"🤖 LLM suy luận:\n{response}")
            
            if "Final Answer:" in response:
                final_ans = response.split("Final Answer:")[-1].strip()
                print(f"\n🏁 Final Answer: {final_ans}")
                break
                
            match = re.search(r"Action:\s*(\w+)\[(.*?)\]", response)
            if match:
                t_name, t_args = match.group(1), match.group(2)
                print(f"🛠️ Thực thi Action: {t_name}[{t_args}]")
                obs = execute_tool_call(t_name, t_args)
                print(f"👁️ Observation:\n{obs}")
                conversation_history += f"\n{response}\nObservation: {obs}\n"
            else:
                conversation_history += f"\n{response}\n"

    if step >= MAX_ITERATIONS:
        print(f"\n🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn tối đa {MAX_ITERATIONS} bước. Ngắt lặp an toàn!")


if __name__ == "__main__":
    print("==================================================")
    print("🏫 BÀI LAB 3: CHATBOT VS REACT AGENT (10 CORE TOOLS)")
    print("==================================================")
    
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")
    
    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json\n")
    
    # Chạy câu test case số 3 (Index 2)
    sample_query = tests[2]["question"]
    
    print("--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE ---")
    run_baseline_chatbot(sample_query, provider)
    
    print("\n--- DEMO 2: CHẠY TRÊN REACT AGENT (10 CORE TOOLS) ---")
    run_react_agent(sample_query, provider)
