# backend_agent

最小可运行的量子力学学习助手后端原型。

## 功能

- `POST /chat`：返回结构化 JSON 响应
- `GET /health`：健康检查
- 本地工具 1：输出项目最小开发计划与资料清单
- 本地工具 2：查询 `data/quantum_terms.json` 中的量子术语

## 环境准备

1. 更新 `.env` 中的 `MOONSHOT_API_KEY`
2. 安装依赖：

```powershell
& 'C:\Users\Affordan\miniconda3\python.exe' -m pip install -r requirements.txt
```

## 启动

```powershell
& 'C:\Users\Affordan\miniconda3\python.exe' -m uvicorn app.main:app --reload
```

启动后访问：

- Swagger: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

## 测试

```powershell
& 'C:\Users\Affordan\miniconda3\python.exe' -m pytest -q
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
    "definition": "......",
    "developer_view": "......"
  }
}
```
