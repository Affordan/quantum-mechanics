# backend_agent

面向开发者的量子力学学习助手后端原型。

## 项目说明

这个项目是课程作业的后端部分，目标是为“不懂量子力学的开发者”提供一个最小可运行的量子力学学习助手。

- Sprint 1 基线：
  - FastAPI 服务
  - `GET /health`
  - `POST /chat`
  - LangChain Agent + Kimi API
  - 本地 `quantum_terms.json` 术语查询
- Sprint 2 改进：
  - 新增 `quantum_sources.jsonl` 轻量来源库
  - 新增来源检索工具，可回答“哪个 PDF/讲义适合看”
  - 保留术语查询能力
  - README 增加 Sprint 2 演示步骤

## 目录结构

```text
backend_agent/
├─ app/
│  ├─ main.py
│  ├─ agent.py
│  ├─ tools.py
│  └─ prompts.py
├─ data/
│  ├─ quantum_terms.json
│  ├─ quantum_sources.jsonl
│  └─ raw_pdfs/          # 本地 PDF 参考资料，不提交到 Git
├─ scripts/
│  └─ validate_sources.py
├─ tests/
├─ requirements.txt
└─ .env
```

## 安装依赖

在 `backend_agent` 目录下执行：

```powershell
python -m pip install -r requirements.txt
```

## 环境变量

在项目根目录创建或更新 `.env`：

```env
MOONSHOT_API_KEY=你的实际Kimi_API_Key
```

## 启动服务

```powershell
python -m uvicorn app.main:app --reload
```

启动后可访问：

- Swagger 文档：`http://127.0.0.1:8000/docs`
- 健康检查：`http://127.0.0.1:8000/health`

## 接口说明

### `GET /health`

返回：

```json
{"status": "ok"}
```

### `POST /chat`

请求体：

```json
{"message": "请解释一下叠加态"}
```

响应体：

```json
{"answer": "......"}
```

Sprint 2 中 `/chat` 对外统一保持简单格式，只返回一个 `answer` 字段。

## 如何测试 `/health`

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"
```

## 如何测试 `/chat`

### 1. 术语解释

```powershell
$body = @{ message = "请解释一下叠加态" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" -Method Post -ContentType "application/json; charset=utf-8" -Body $body | ConvertTo-Json -Depth 5
```

### 2. 来源资料查询

```powershell
$body = @{ message = "有什么资料可以帮助我理解波函数？" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" -Method Post -ContentType "application/json; charset=utf-8" -Body $body | ConvertTo-Json -Depth 5
```

### 3. 查询适合开发者的 PDF

```powershell
$body = @{ message = "哪个 PDF 适合开发者理解量子比特？" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" -Method Post -ContentType "application/json; charset=utf-8" -Body $body | ConvertTo-Json -Depth 5
```

### 4. 空输入处理

```powershell
$body = @{ message = "" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" -Method Post -ContentType "application/json; charset=utf-8" -Body $body | ConvertTo-Json -Depth 5
```

## 如何演示 Sprint 2

推荐按下面顺序演示：

1. 启动服务
2. 演示 `/health`
3. 演示本地术语解释：
   - `请解释一下叠加态`
4. 演示来源库检索：
   - `有什么资料可以帮助我理解波函数？`
   - `哪个 PDF 适合开发者理解量子比特？`
5. 演示空输入不会崩溃
6. 演示来源校验脚本

## 来源库校验脚本

```powershell
python scripts/validate_sources.py
```

脚本会：

- 读取 `data/quantum_sources.jsonl`
- 检查每一行是不是合法 JSON
- 输出来源总数
- 输出全部概念标签

## 本地 PDF 说明

- `data/raw_pdfs/` 中的 PDF 只作为**本地参考资料**
- **不要把 raw PDFs 提交到 Git**
- 仓库只保存：
  - 元数据
  - PDF 文件名
  - 来源链接
  - 自写摘要
  - 开发者视角说明

## 当前 Sprint 2 来源库内容

当前 `data/quantum_sources.jsonl` 已收录 8 条来源记录，来源于已成功下载的 PDF，包括：

- MIT OpenCourseWare 量子物理讲义
- David Tong 量子力学相关讲义
- Springer 的量子计算入门书
- UT Austin 量子力学课程资料
- 北京师范大学中文量子力学讲义
