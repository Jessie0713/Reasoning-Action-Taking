# ReAct Agent 專案

## 專案描述

這是一個基於 Reasoning and Action Taking (ReAct) 框架的 AI 代理專案。代理使用 OpenAI 的 GPT 模型來進行推理，並結合 Tavily 搜索工具來獲取外部資訊，以回答用戶的問題。

## 功能特色

- **ReAct 框架**: 結合推理 (Reasoning) 和行動 (Action) 的代理架構
- **OpenAI GPT 整合**: 使用 GPT-4o-mini 模型進行推理
- **Tavily 搜索**: 整合外部搜索功能以獲取最新資訊
- **步驟限制**: 可設定最大推理步驟數以控制計算成本
- **錯誤處理**: 包含 API 錯誤處理和異常情況處理

## 安裝步驟

### 1. 克隆專案

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. 建立虛擬環境

```bash
python -m venv venv
source venv/bin/activate  # 在 macOS/Linux 上
# 或在 Windows 上: venv\Scripts\activate
```

### 3. 安裝依賴

```bash
pip install -r requirements.txt
```

### 4. 設定環境變數

建立 `.env` 檔案並設定以下變數：

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## 使用方法

### 基本使用

```python
from agent import ReActAgent

# 建立代理實例
agent = ReActAgent(model="gpt-4o-mini", max_steps=5)

# 執行任務
question = "What fraction of Japan's population is Taiwan's population as of 2025?"
answer = agent.execute(question)
print(answer)
```

### 執行範例任務

運行 `main.py` 來測試預設的範例任務：

```bash
python main.py
```

目前包含的三個範例任務：
1. 日本人口佔台灣人口的比例 (2025年)
2. iPhone 15 和 Samsung S24 的主要螢幕規格比較
3. Morphic AI 搜尋創業公司的 CEO 是誰

## 專案結構

```
.
├── agent.py          # ReActAgent 類別實作
├── tools.py          # SearchTool 類別實作
├── main.py           # 主程式和範例任務
├── requirements.txt  # Python 依賴套件
└── README.md         # 專案說明文件
```

## API 金鑰取得

### OpenAI API Key
1. 前往 [OpenAI 平台](https://platform.openai.com/)
2. 註冊或登入帳戶
3. 在 API Keys 區塊建立新的金鑰
4. 複製金鑰並貼到 `.env` 檔案中

### Tavily API Key
1. 前往 [Tavily 網站](https://tavily.com/)
2. 註冊帳戶
3. 取得 API 金鑰
4. 複製金鑰並貼到 `.env` 檔案中

## 自訂設定

### 模型選擇
可以在建立 `ReActAgent` 時指定不同的 GPT 模型：

```python
agent = ReActAgent(model="gpt-4", max_steps=10)
```

### 最大步驟數
調整 `max_steps` 參數來控制代理的最大推理步驟：

```python
agent = ReActAgent(model="gpt-4o-mini", max_steps=3)  # 減少步驟以節省成本
```

## 注意事項

- 確保 API 金鑰安全，不要將 `.env` 檔案提交到版本控制系統
- Tavily 搜索可能會有使用限制，請參考其官方文件
- OpenAI API 呼叫會產生費用，請注意使用量

## 授權

此專案僅供學習和研究用途。