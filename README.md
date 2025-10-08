# 本地日志分析工具（Tkinter版）

本工具用于本地分析日志文件，支持：

- 高亮显示不同类型日志
- 支持正则匹配或普通关键词匹配
- 支持规则文件 YAML 配置
- 支持 `instruction` 字段显示日志提示

---

## YAML 配置说明

每条规则包含以下字段：

| 字段         | 类型       | 说明 |
| ------------ | ---------- | ---- |
| `keyword`    | 字符串     | 匹配的关键字或正则表达式 |
| `color`      | 字符串     | 匹配日志高亮颜色（可用颜色见下表） |
| `regex`      | 布尔值     | 是否按正则匹配 (`true` / `false`) |
| `instruction`| 字符串     | 对匹配日志的中文提示，可选 |

---

## 可用颜色

- red  
- yellow  
- green  
- blue  
- cyan  
- purple  
- orange  
- pink  
- gray  
- white  

> 颜色用于高亮显示匹配的日志行

---

## YAML 示例

```yaml
- keyword: 'notifyUiVisibilityChanged:vis=0x[0-9A-Fa-f]+, SystemUiVisibility=0x[0-9A-Fa-f]+'
  color: "cyan"
  regex: true
  instruction: "UI 可视化状态变化"

- keyword: 'WARN.*'
  color: "yellow"
  regex: true
  instruction: "警告信息"

- keyword: 'ERROR|Failed'
  color: "red"
  regex: true
  instruction: "错误信息"

- keyword: '0x[0-9A-Fa-f]{8,}'
  color: "purple"
  regex: true
  instruction: "十六进制地址"

- keyword: 'session_id\s*=\s*\d+'
  color: "green"
  regex: true
  instruction: "会话ID信息"

- keyword: 'INFO.*Started'
  color: "blue"
  regex: true
  instruction: "信息类启动日志"

- keyword: 'DEBUG.*'
  color: "pink"
  regex: true
  instruction: "调试信息"

- keyword: 'Exception|Traceback'
  color: "orange"
  regex: true
  instruction: "异常堆栈信息"
