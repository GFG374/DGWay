# 模型可用性测试报告

测试时间：2026-06-03 15:55 CST

本报告根据当前 OpenAI / GPT、Google Gemini、Antigravity 三个账号上游实时测试结果整理。报告只记录模型可用性，不包含完整 API Key。

## 汇总

| 账号 | 上游展示模型数 | 测试可用 | 测试失败 |
| --- | ---: | ---: | ---: |
| OpenAI / GPT | 17 | 9 | 8 |
| Google Gemini | 9 | 5 | 4 |
| Antigravity | 39 | 27 | 12 |

## OpenAI / GPT

### 可用模型

- `gpt-5.4`
- `gpt-5.4-2026-03-05`
- `gpt-5.4-mini`
- `gpt-5.5`
- `codex-auto-review`
- `gpt-5.3-codex-spark`
- `gpt-image-1`
- `gpt-image-1.5`
- `gpt-image-2`

### 暂不建议展示

以下模型当前测试失败，不建议展示给用户作为可用模型：

| 模型 | 测试结果 |
| --- | --- |
| `gpt-4o-audio-preview` | HTTP 400，不支持当前 Codex / ChatGPT 账号 |
| `gpt-4o-realtime-preview` | HTTP 400，不支持当前 Codex / ChatGPT 账号 |
| `gpt-5.2` | HTTP 400，不支持当前 Codex / ChatGPT 账号 |
| `gpt-5.2-2025-12-11` | HTTP 400，不支持当前 Codex / ChatGPT 账号 |
| `gpt-5.2-chat-latest` | HTTP 400，不支持当前 Codex / ChatGPT 账号 |
| `gpt-5.2-pro` | HTTP 400，不支持当前 Codex / ChatGPT 账号 |
| `gpt-5.2-pro-2025-12-11` | HTTP 400，不支持当前 Codex / ChatGPT 账号 |
| `gpt-5.3-codex` | HTTP 400，不支持当前 Codex / ChatGPT 账号 |

## Google Gemini

### 可用模型

- `gemini-2.5-flash`
- `gemini-2.5-pro`
- `gemini-3-flash-preview`
- `gemini-3-pro-preview`
- `gemini-3.1-pro-preview`

### 暂不建议展示

以下模型当前测试失败，不建议展示给用户作为可用模型：

| 模型 | 测试结果 |
| --- | --- |
| `gemini-2.5-flash-image` | HTTP 404，上游返回 Requested entity was not found |
| `gemini-3.1-flash-image` | HTTP 404，上游返回 Requested entity was not found |
| `gemini-2.0-flash` | HTTP 404，上游返回 Requested entity was not found |
| `gemini-3.5-flash` | HTTP 404，上游返回 Requested entity was not found |

## Antigravity

### 可用模型

- `claude-haiku-4-5`
- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
- `claude-opus-4-5-thinking`
- `claude-opus-4-6`
- `claude-opus-4-6-thinking`
- `claude-opus-4-8-thinking`
- `claude-sonnet-4-6`
- `gemini-3-pro-image`
- `gemini-3-pro-image-preview`
- `gemini-3.1-flash-image`
- `gemini-3.1-flash-image-preview`
- `gemini-2.5-flash`
- `gemini-2.5-flash-lite`
- `gemini-2.5-flash-thinking`
- `gemini-3-flash`
- `gemini-3-flash-agent`
- `gemini-3-flash-preview`
- `gemini-3-pro-high`
- `gemini-3-pro-low`
- `gemini-3-pro-preview`
- `gemini-3.1-flash-lite`
- `gemini-3.1-pro-low`
- `gemini-3.5-flash-extra-low`
- `gemini-3.5-flash-low`
- `gemini-pro-agent`
- `gpt-oss-120b-medium`

### 暂不建议展示

以下模型当前测试失败，不建议展示给用户作为可用模型：

| 模型 | 测试结果 |
| --- | --- |
| `claude-opus-4-7` | HTTP 502，上游请求失败 |
| `claude-opus-4-8` | HTTP 502，上游请求失败 |
| `claude-sonnet-4-5` | HTTP 502，上游请求失败 |
| `claude-sonnet-4-5-20250929` | HTTP 502，上游请求失败 |
| `claude-sonnet-4-5-thinking` | HTTP 502，上游请求失败 |
| `gemini-2.5-flash-image` | HTTP 404，上游返回 Requested entity was not found |
| `gemini-2.5-flash-image-preview` | HTTP 404，上游返回 Requested entity was not found |
| `chat_20706` | HTTP 400，上游返回 Request contains an invalid argument |
| `chat_23310` | HTTP 400，上游返回 Request contains an invalid argument |
| `gemini-2.5-pro` | HTTP 502，上游服务暂时不可用 |
| `gemini-3.1-pro-high` | HTTP 400，上游返回 Request contains an invalid argument |
| `gemini-3.1-pro-preview` | HTTP 400，上游返回 Request contains an invalid argument |

## 展示建议

用户侧“可用模型”建议只展示本报告中各账号的“可用模型”。“暂不建议展示”的模型可以继续留在后台配置中观察，但不建议作为用户可调用模型公开展示，避免用户看到模型后实际调用失败。

后续如果重新调整分组、白名单或价格，建议重新跑一次上游可用性测试，并同步更新本报告。
