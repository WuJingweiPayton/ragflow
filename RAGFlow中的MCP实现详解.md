# RAGFlow中的MCP实现详解

## 1. MCP架构概览

RAGFlow实现了完整的MCP（Model Context Protocol）生态系统，包括：

### 1.1 双重角色

- **MCP服务器**：对外提供RAGFlow的检索能力
- **MCP客户端**：集成外部MCP工具到AI对话中

### 1.2 核心组件

```
RAGFlow MCP架构
├── MCP Server (mcp/server/)
│   ├── server.py - MCP服务器实现
│   └── RAGFlowConnector - RAGFlow API连接器
├── MCP Client (mcp/client/)
│   ├── client.py - MCP客户端实现
│   └── streamable_http_client.py - HTTP传输
├── Integration Layer (rag/utils/)
│   └── mcp_tool_call_conn.py - 工具调用连接器
└── Management APIs (api/apps/)
    └── mcp_server_app.py - MCP管理接口
```

## 2. MCP服务器端实现

### 2.1 核心文件：`mcp/server/server.py`

**主要功能**：

- 将RAGFlow的检索能力包装为MCP工具
- 支持多种传输协议（SSE、Streamable HTTP）
- 提供认证和多租户支持

**核心类**：

```python
class RAGFlowConnector:
    """RAGFlow API连接器"""
    def __init__(self, base_url: str, version="v1"):
        self.base_url = base_url
        self.api_url = f"{self.base_url}/api/{self.version}"

    def retrieval(self, dataset_ids, document_ids=None, question="", ...):
        """调用RAGFlow检索API"""
        # 构建检索请求并返回结果
        pass
```

### 2.2 提供的MCP工具

**ragflow_retrieval工具**：

```python
types.Tool(
    name="ragflow_retrieval",
    description="从RAGFlow知识库检索相关内容",
    inputSchema={
        "type": "object",
        "properties": {
            "dataset_ids": {
                "type": "array",
                "items": {"type": "string"}
            },
            "document_ids": {
                "type": "array",
                "items": {"type": "string"}
            },
            "question": {"type": "string"},
        },
        "required": ["dataset_ids", "question"],
    },
)
```

### 2.3 启动配置

**Docker配置**：

```bash
# 启用MCP服务器的Docker参数
--enable-mcpserver              # 启用MCP服务器
--mcp-host=0.0.0.0             # 监听地址
--mcp-port=9382                # 监听端口
--mcp-base-url=http://127.0.0.1:9380  # RAGFlow API地址
--mcp-mode=self-host           # 运行模式
--mcp-host-api-key=ragflow-xxx # API密钥
```

## 3. MCP客户端实现

### 3.1 核心文件：`rag/utils/mcp_tool_call_conn.py`

**主要功能**：

- 连接外部MCP服务器
- 获取和调用MCP工具
- 管理异步连接和会话

**核心类**：

```python
class MCPToolCallSession(ToolCallSession):
    """MCP工具调用会话"""
    def __init__(self, mcp_server, server_variables=None):
        # 创建独立的事件循环和线程池
        self._event_loop = asyncio.new_event_loop()
        self._thread_pool = ThreadPoolExecutor(max_workers=1)

    def tool_call(self, name: str, arguments: dict) -> str:
        """调用MCP工具"""
        # 在异步环境中执行工具调用
        future = asyncio.run_coroutine_threadsafe(
            self._call_mcp_tool(name, arguments),
            self._event_loop
        )
        return future.result(timeout=timeout)
```

### 3.2 支持的传输协议

**SSE传输**：

```python
async with sse_client(url, headers) as stream:
    async with ClientSession(*stream) as client_session:
        await client_session.initialize()
        await self._process_mcp_tasks(client_session)
```

**Streamable HTTP传输**：

```python
async with streamablehttp_client(url, headers) as (read_stream, write_stream, _):
    async with ClientSession(read_stream, write_stream) as client_session:
        await client_session.initialize()
        await self._process_mcp_tasks(client_session)
```

### 3.3 工具格式转换

**MCP工具 → OpenAI工具格式**：

```python
def mcp_tool_metadata_to_openai_tool(mcp_tool: Tool) -> dict:
    return {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.inputSchema,
        },
    }
```

## 4. MCP与语言模型的集成机制

### 4.1 工具绑定机制

**语言模型基类**（`rag/llm/chat_model.py`）：

```python
class Base(ABC):
    def bind_tools(self, toolcall_session, tools):
        """绑定工具到语言模型"""
        if not (toolcall_session and tools):
            return
        self.is_tools = True

        for tool in tools:
            # 将MCP工具会话绑定到工具名称
            self.toolcall_sessions[tool["function"]["name"]] = toolcall_session
            self.tools.append(tool)
```

### 4.2 工具调用流程

**同步工具调用**：

```python
def chat_with_tools(self, system: str, history: list, gen_conf: dict):
    # 调用语言模型
    response = self.client.chat.completions.create(
        model=self.model_name,
        messages=history,
        tools=self.tools,  # MCP工具列表
        **gen_conf
    )

    # 处理工具调用
    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            name = tool_call.function.name
            args = json_repair.loads(tool_call.function.arguments)

            # 通过MCP会话调用工具
            tool_response = self.toolcall_sessions[name].tool_call(name, args)
            history = self._append_history(history, tool_call, tool_response)
```

**流式工具调用**：

```python
def chat_streamly_with_tools(self, system: str, history: list, gen_conf: dict):
    # 处理流式响应中的工具调用
    final_tool_calls = self._wrap_toolcall_message(stream)

    for tool_call in final_tool_calls.values():
        name = tool_call.function.name
        args = json_repair.loads(tool_call.function.arguments)

        # 通过MCP会话调用工具
        tool_response = self.toolcall_session[name].tool_call(name, args)
        history = self._append_history(history, tool_call, tool_response)
```

### 4.3 集成点

**对话服务集成**（`api/db/services/dialog_service.py`）：

```python
def chat(dialog, messages, stream=True, **kwargs):
    # 获取模型
    kbs, embd_mdl, rerank_mdl, chat_mdl, tts_mdl = get_models(dialog)

    # 绑定MCP工具
    toolcall_session, tools = kwargs.get("toolcall_session"), kwargs.get("tools")
    if toolcall_session and tools:
        chat_mdl.bind_tools(toolcall_session, tools)
```

## 5. MCP管理和配置功能

### 5.1 数据库模型

**MCP服务器模型**（`api/db/db_models.py`）：

```python
class MCPServer(DataBaseModel):
    id = CharField(max_length=32, primary_key=True)
    name = CharField(max_length=255, null=False)
    tenant_id = CharField(max_length=32, null=False, index=True)
    url = CharField(max_length=2048, null=False)
    server_type = CharField(max_length=32, null=False)  # SSE/STREAMABLE_HTTP
    description = TextField(null=True)
    variables = JSONField(null=True, default=dict)      # 配置变量
    headers = JSONField(null=True, default=dict)        # 请求头
```

### 5.2 管理API

**MCP服务器管理**（`api/apps/mcp_server_app.py`）：

| 接口          | 功能          | 描述                        |
| ------------- | ------------- | --------------------------- |
| `/list`       | 列出MCP服务器 | 分页查询用户的MCP服务器     |
| `/create`     | 创建MCP服务器 | 创建并测试MCP服务器连接     |
| `/update`     | 更新MCP服务器 | 更新配置并重新获取工具      |
| `/rm`         | 删除MCP服务器 | 批量删除MCP服务器           |
| `/import`     | 导入MCP配置   | 从JSON文件导入多个MCP服务器 |
| `/export`     | 导出MCP配置   | 导出MCP服务器配置为JSON     |
| `/list_tools` | 列出工具      | 获取MCP服务器提供的工具列表 |
| `/test_tool`  | 测试工具      | 测试特定MCP工具的功能       |

### 5.3 前端管理界面

**MCP设置页面**（`web/src/pages/profile-setting/mcp/`）：

- **服务器列表**：显示所有配置的MCP服务器
- **添加/编辑**：创建或修改MCP服务器配置
- **导入/导出**：支持JSON格式的批量配置
- **工具管理**：查看和测试MCP工具
- **状态监控**：显示连接状态和工具可用性

### 5.4 配置文件格式

**导入/导出格式**：

```json
{
  "mcpServers": {
    "server_name": {
      "type": "sse",
      "url": "http://localhost:9382/sse",
      "authorization_token": "your_token_here",
      "name": "Display Name",
      "tool_configuration": {}
    }
  }
}
```

## 6. 使用场景和工作流程

### 6.1 作为MCP服务器

**使用场景**：

- 为Claude Desktop等MCP客户端提供RAGFlow检索能力
- 在其他AI应用中集成RAGFlow的知识库

**工作流程**：

```
1. 启动RAGFlow MCP服务器 (端口9382)
2. MCP客户端连接到RAGFlow服务器
3. 客户端获取ragflow_retrieval工具
4. 调用工具检索知识库内容
5. 返回检索结果给客户端
```

### 6.2 作为MCP客户端

**使用场景**：

- 在RAGFlow对话中集成外部工具
- 扩展AI助手的功能能力

**工作流程**：

```
1. 配置外部MCP服务器
2. RAGFlow连接并获取工具列表
3. 工具绑定到语言模型
4. 用户对话触发工具调用
5. 通过MCP调用外部工具
6. 将结果集成到对话中
```

## 7. 技术特点

### 7.1 异步处理

- 使用独立的事件循环处理MCP连接
- 支持并发的工具调用
- 非阻塞的会话管理

### 7.2 协议支持

- **SSE (Server-Sent Events)**：适用于浏览器环境
- **Streamable HTTP**：适用于高性能场景
- **WebSocket**：计划中的支持

### 7.3 安全性

- API密钥认证
- 多租户隔离
- 请求头自定义

### 7.4 可扩展性

- 插件化的工具注册
- 灵活的配置管理
- 支持自定义传输协议

## 8. 限制和注意事项

### 8.1 当前限制

- 主要支持HTTP-based的MCP服务器
- 不支持命令行启动的MCP服务器
- 工具调用有超时限制

### 8.2 性能考虑

- MCP连接会占用资源
- 需要合理配置超时时间
- 建议使用连接池管理

### 8.3 兼容性

- 遵循MCP协议规范
- 与标准MCP客户端兼容
- 支持工具元数据标准格式

## 9. 总结

RAGFlow的MCP实现提供了完整的工具生态系统集成能力，既可以作为工具提供者，也可以作为工具消费者，为AI应用的功能扩展提供了强大的基础设施。

### 9.1 主要优势

- **双向集成**：既是MCP服务器又是MCP客户端
- **异步高性能**：支持并发连接和工具调用
- **完整生态**：从底层协议到用户界面的完整实现
- **企业级**：支持多租户和权限管理

### 9.2 应用价值

- **扩展AI能力**：通过MCP工具丰富AI助手功能
- **知识库共享**：让其他AI应用访问RAGFlow知识库
- **生态互联**：与MCP生态系统无缝集成
- **开发友好**：提供完整的管理和开发接口

通过MCP协议，RAGFlow实现了与更广泛的AI工具生态系统的互联互通，为用户提供了更加丰富和强大的AI应用体验。
