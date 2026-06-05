from openai import OpenAI

PROMPT = """你是一名专业智能助手。

下面是OCR识别到的内容：

====================
{OCR_TEXT}
====================

请根据内容进行分析。

要求：
1. 给出核心答案
2. 保持简洁
3. 不要复述题目
4. 如果内容不完整请指出"""

class DeepSeekClient:
    def __init__(self, api_key, base_url, model):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def ask(self, text):
        rsp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": PROMPT.replace("{OCR_TEXT}", text)}],
            stream=False,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}}
        )
        return rsp.choices[0].message.content
