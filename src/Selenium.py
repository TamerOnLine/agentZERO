from langchain.agents import initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from langchain.tools import Tool
from bs4 import BeautifulSoup

# 🔹 دالة استخراج البيانات من صفحة ويب معينة
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def scrape_page(url: str, text_limit: int = 1000):
    options = Options()
    options.add_argument("--headless")  # تشغيل بدون واجهة رسومية
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')
        return soup.get_text(separator=' ', strip=True)[:text_limit]
    finally:
        driver.quit()




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
# تجربة الكود
url = "https://link.springer.com/"
content = scrape_page(url)
print(content)
