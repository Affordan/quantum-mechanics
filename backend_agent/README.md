# backend_agent

最小可运行的量子力学学习助手后端原型。

## 功能

- `POST /chat`：返回结构化 JSON 响应
- `GET /health`：健康检查
- LangChain agent：通过 Kimi OpenAI-compatible API 处理通用问题
- 本地工具 1：输出项目最小开发计划与资料清单
- 本地工具 2：查询 `data/quantum_terms.json` 中的量子术语

## 目录结构

```text
backend_agent/
├─ app/
│  ├─ main.py
│  ├─ agent.py
│  ├─ tools.py
│  └─ prompts.py
├─ data/
│  └─ quantum_terms.json
├─ tests/
├─ requirements.txt
└─ .env
```

## 环境准备

1. 在项目根目录创建或更新 `.env`

```env
MOONSHOT_API_KEY=你的实际Kimi_API_Key
```

2. 安装依赖：

```powershell
python -m pip install -r requirements.txt
```

## 启动

```powershell
python -m uvicorn app.main:app --reload
```

启动后访问：

- Swagger: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

## 测试

```powershell
python -m pytest -q
```

## Swagger 演示

1. 打开 `http://127.0.0.1:8000/docs`
2. 找到 `POST /chat`
3. 点击 `Try it out`
4. 输入示例请求体后点击 `Execute`

## PowerShell 演示命令

健康检查：

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"
```

项目计划问答：

```powershell
$body = @{ message = "请给我这个项目的最小开发计划和需要补充的资料" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" -Method Post -ContentType "application/json; charset=utf-8" -Body $body | ConvertTo-Json -Depth 5
```

量子术语问答：

```powershell
$body = @{ message = "请解释一下叠加态" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" -Method Post -ContentType "application/json; charset=utf-8" -Body $body | ConvertTo-Json -Depth 5
```

## `/chat` 输入输出

请求体：

```json
{
  "message": "请给我这个物理小语言模型项目的最小开发计划和需要补充的资料"
}
```

响应体示例：

```json
{
  "intent": "project_plan",
  "answer": "最小开发计划已整理完成，可直接查看步骤和资料清单。",
  "data": {
    "project_name": "量子力学学习助手",
    "source": "local_plan",
    "steps": ["..."],
    "materials": ["..."]
  }
}
```

```json
{
  "message": "请解释一下叠加态"
}
```

响应体示例：

```json
{
  "intent": "quantum_term",
  "answer": "叠加态：......",
  "data": {
    "term": "叠加态",
    "source": "local_json",
    "found": true,
    "definition": "......",
    "developer_view": "......"
  }
}
```

## 本地术语数据

当前 `data/quantum_terms.json` 已包含至少 3 个可直接演示的术语：

- `波函数`
- `叠加态`
- `测不准原理`
