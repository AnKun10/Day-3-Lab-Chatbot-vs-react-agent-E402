"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Test Cases + Multi-Provider.
Chủ đề: Trợ Lý Nắm Bắt Tính Cách & Chọn Quà Tặng Phù Hợp (Trọn bộ 10 Tools)
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
from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, AUTONOMOUS_PLANNING_PROMPT, MAX_ITERATIONS
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
        if provider.__class__.__name__ in ["OfflineMockProvider", "MockProvider"] or not getattr(provider, "api_key", True):
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


def run_autonomous_agent(user_query: str, provider):
    """
    🎁 BONUS CẤP 4: AUTONOMOUS AGENT (Planning + Execution + Memory + Goal Evaluation)
    Tự động chia nhỏ mục tiêu phức tạp, thực thi từng bước bằng Tools và lưu vết vào Memory.
    """
    print(f"\n🚀 [AUTONOMOUS AGENT - CẤP 4] Mục tiêu lớn (Goal): {user_query}")
    memory = []
    
    is_mock = provider.__class__.__name__ in ["OfflineMockProvider", "MockProvider"] or not getattr(provider, "api_key", True)
    
    if is_mock:
        print("\n📋 [PHASE 1: PLANNING - TỰ RÃ MỤC TIÊU]")
        plans = [
            {"step": 1, "task": "Phân tích đặc điểm tính cách & trích xuất sở thích người nhận"},
            {"step": 2, "task": "Lọc danh sách quà tặng trong kho phù hợp ngân sách & kiểm tra đánh giá (Reviews)"},
            {"step": 3, "task": "Tìm vị trí cửa hàng quà tặng gần nhất & đề xuất phong cách gói quà phù hợp"},
            {"step": 4, "task": "Tổng hợp kết quả cuối cùng và tự đánh giá hoàn thành mục tiêu (Goal Evaluation)"}
        ]
        for p in plans:
            print(f"  📌 Bước {p['step']}: {p['task']}")
            
        print("\n⚙️ [PHASE 2: EXECUTION & MEMORY TRACKING]")
        
        # Step 1
        print(f"\n--- 🔄 Step 1: {plans[0]['task']} ---")
        print("🧠 Thought/Planning: Phân tích đặc điểm đối tượng tặng quà.")
        print(f"🛠️ Action: analyze_personality['{user_query}']")
        obs1 = AVAILABLE_TOOLS["analyze_personality"](user_query)
        print(f"👁️ Observation:\n{obs1}")
        memory.append({"step": 1, "plan": plans[0]['task'], "action": f"analyze_personality['{user_query}']", "result": obs1})
        print("💾 [Memory Saved]: Đã lưu thông tin tính cách vào bộ nhớ (Memory).")
        
        # Step 2
        print(f"\n--- 🔄 Step 2: {plans[1]['task']} ---")
        print("🧠 Thought/Planning: Lọc danh sách món quà dưới 500k VNĐ và xem đánh giá chất lượng sản phẩm.")
        print("🛠️ Action: filter_by_budget[500000, 0]")
        obs2_1 = AVAILABLE_TOOLS["filter_by_budget"](500000, 0)
        print(f"👁️ Observation 1:\n{obs2_1}")
        print("🛠️ Action: check_reviews['GIFT001']")
        obs2_2 = AVAILABLE_TOOLS["check_reviews"]("GIFT001")
        print(f"👁️ Observation 2:\n{obs2_2}")
        step2_res = f"Filter:\n{obs2_1}\nReview:\n{obs2_2}"
        memory.append({"step": 2, "plan": plans[1]['task'], "action": "filter_by_budget + check_reviews", "result": step2_res})
        print("💾 [Memory Saved]: Đã lưu danh sách quà & đánh giá vào bộ nhớ (Memory).")
        
        # Step 3
        print(f"\n--- 🔄 Step 3: {plans[2]['task']} ---")
        print("🧠 Thought/Planning: Tra cứu cửa hàng bán quà gần nhất ở Hà Nội và phong cách gói quà sinh nhật.")
        print("🛠️ Action: find_nearby_stores['Hà Nội', 'Cầu Giấy']")
        obs3_1 = AVAILABLE_TOOLS["find_nearby_stores"]("Hà Nội", "Cầu Giấy")
        print(f"👁️ Observation 1:\n{obs3_1}")
        print("🛠️ Action: suggest_gift_wrapping['Sinh nhật', 'bạn gái']")
        obs3_2 = AVAILABLE_TOOLS["suggest_gift_wrapping"]("Sinh nhật", "bạn gái")
        print(f"👁️ Observation 2:\n{obs3_2}")
        step3_res = f"Stores:\n{obs3_1}\nWrapping:\n{obs3_2}"
        memory.append({"step": 3, "plan": plans[2]['task'], "action": "find_nearby_stores + suggest_gift_wrapping", "result": step3_res})
        print("💾 [Memory Saved]: Đã lưu vị trí cửa hàng & style gói quà vào bộ nhớ (Memory).")
        
        # Step 4: Evaluation
        print(f"\n--- 🎯 Step 4: [GOAL EVALUATION & FINAL SYNTHESIS] ---")
        print(f"📊 Tổng số bản ghi trong Memory: {len(memory)} bước thực thi thành công.")
        final_ans = (
            "BÁO CÁO TƯ VẤN HOÀN CHỈNH TỪ AUTONOMOUS AGENT (CẤP 4):\n"
            "1. Tính cách: Bạn gái 22t hướng nội, thích không gian yên tĩnh đọc sách và thưởng thức cà phê.\n"
            "2. Quà tặng đề xuất (Dưới 500k): [GIFT001] Nến thơm Lavender (350,000 VNĐ - ⭐ 4.8/5) hoặc [GIFT006] Đèn đọc sách chống mỏi mắt Baseus (280,000 VNĐ).\n"
            "3. Địa chỉ mua trực tiếp: Gift Studio Cầu Giấy (123 Xuân Thủy, Cầu Giấy, Hà Nội).\n"
            "4. Phong cách gói quà: Romantic Vintage với giấy Kraft nâu, nơ cói thắt hoa khô kèm thiệp chúc mừng sinh nhật ngọt ngào."
        )
        print(f"🏁 Final Answer:\n{final_ans}")
    else:
        # Online LLM Mode
        print("\n📋 [PHASE 1: PLANNING - TỰ RÃ MỤC TIÊU BẰNG LLM]")
        planning_prompt = AUTONOMOUS_PLANNING_PROMPT + f"\nGoal: {user_query}"
        plan_res = provider.generate(planning_prompt)
        print(f"📝 Kế hoạch thực thi (Plan):\n{plan_res}")

        print("\n⚙️ [PHASE 2: EXECUTION WITH REACT LOOP & MEMORY TRACKING]")
        conversation_history = f"Goal: {user_query}\nPlan:\n{plan_res}\n"
        
        step = 0
        while step < MAX_ITERATIONS:
            step += 1
            print(f"\n--- 🔄 Autonomous Step {step}/{MAX_ITERATIONS} ---")
            
            memory_str = ""
            if memory:
                memory_str = "\n[MEMORY LOG - BỘ NHỚ LƯU VẾT]:\n" + "\n".join(
                    [f"- Step {m['step']}: Action `{m['action']}` -> Observation: {m['result'][:150]}" for m in memory]
                ) + "\n"
                
            prompt = REACT_SYSTEM_PROMPT + memory_str + "\n" + conversation_history
            response = provider.generate(prompt)
            print(f"🤖 LLM suy luận:\n{response}")
            
            if "[Gemini Exception]" in response or "RESOURCE_EXHAUSTED" in response:
                print("⚠️ Gặp lỗi API Rate Limit trong quá trình lặp. Dừng và sử dụng dữ liệu trong Memory.")
                print(f"🏁 Final Answer: Đã hoàn tất {len(memory)} bước suy luận tự chủ trước khi đạt giới hạn API.")
                break

            if "Final Answer:" in response:
                final_ans = response.split("Final Answer:")[-1].strip()
                print(f"\n🏁 Final Answer: {final_ans}")
                print(f"💾 Tổng số bước lưu vết trong Memory: {len(memory)}")
                print("🎯 [Goal Evaluation]: Mục tiêu đã hoàn thành 100%!")
                break
                
            match = re.search(r"Action:\s*(\w+)\[(.*?)\]", response)
            if match:
                t_name, t_args = match.group(1), match.group(2)
                print(f"🛠️ Thực thi Action: {t_name}[{t_args}]")
                obs = execute_tool_call(t_name, t_args)
                print(f"👁️ Observation:\n{obs}")
                memory.append({"step": step, "action": f"{t_name}[{t_args}]", "result": obs})
                print(f"💾 [Memory Saved]: Logged step {step} to memory.")
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

    print("\n--- DEMO 3: 🎁 BONUS - AUTONOMOUS AGENT (CẤP 4: PLANNING & MEMORY) ---")
    run_autonomous_agent(sample_query, provider)

