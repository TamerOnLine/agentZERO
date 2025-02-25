from langchain.agents import initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from langchain.tools import Tool
import requests
from bs4 import BeautifulSoup

# 🔹 دالة استخراج البيانات من صفحة ويب معينة


def scrape_page(url: str, text_limit: int = 1000):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)[:text_limit]
    except requests.exceptions.RequestException as e:
        return f"Error retrieving content: {e}"




# 🔹 تعريف الأداة الوحيدة المتاحة (Web Scraper فقط)
tools = [
    Tool(
        name="Web Scraper",
        func=scrape_page,
        description="يستخدم لاستخراج النصوص من صفحة ويب معينة. يجب تمرير رابط الصفحة."
    )
]

# ✅ **إعداد المتغيرات الديناميكية للنموذج**
model_name = "mistral"
temperature = 0.7
top_p = 0.9

# 🔹 إعداد نموذج Ollama
llm = OllamaLLM(model=model_name, temperature=temperature, top_p=top_p)

# 🔹 تهيئة الوكيل مع Ollama (بدون Site Search)
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    return_intermediate_steps=False  # منع تنفيذ عمليات إضافية غير ضرورية
)

# 🔹 تجربة تشغيل الوكيل مع استخراج النصوص مباشرة من موقع معين
try:
    url_to_scrape = "https://link.springer.com/"  # ضع رابط الصفحة التي تريد استخراج البيانات منها
    response = agent_executor.invoke({"input": url_to_scrape})
    print(response)
except Exception as e:
    print(f"Error executing agent: {e}")
