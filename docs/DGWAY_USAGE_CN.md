# DGWay API 使用方式

这份文档给 DGWay API 用户使用。用户只需要知道三个东西：`Base URL`、自己的 `API Key`、可用模型名称。

## 1. 基础信息

| 项目 | 当前值 |
| --- | --- |
| API 入口 | `https://dgth.shop` |
| OpenAI-compatible Base URL | `https://dgth.shop/v1` |
| Gemini-compatible Base URL | `https://dgth.shop/v1beta` |
| Antigravity Claude Code Base URL | `https://dgth.shop` |
| API Key | 在 DGWay API 的“API 密钥”页面创建 |

当前正式入口已经使用域名和 HTTPS。客户端不要再填写旧 IP 地址。

## 2. 创建 API Key

1. 登录 DGWay API。新用户可以在登录页点击“注册”，使用邮箱和密码创建账号；如果站点开启第三方登录，也可以使用 GitHub 或 Google 登录。
2. 进入“我的账户 -> API 密钥”。
3. 点击“创建密钥”。
4. 选择管理员给你的分组。
5. 创建后复制 `sk-...` 格式的密钥。

不要把自己的 API Key 发给别人。怀疑泄露时，直接删除旧 Key，重新创建。

## 3. 在 Claude Code 中使用

推荐用 CC Switch 配置 DGWay API。

### 3.1 基础配置

| 项目 | 填写 |
| --- | --- |
| 供应商名称 | `DGWay` |
| API Key | 你的 DGWay API Key |
| 请求地址 | `https://dgth.shop` |
| API 格式 | `Anthropic Messages` |
| 认证字段 | `ANTHROPIC_AUTH_TOKEN` |

配置 JSON 示例：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-你的APIKey",
    "ANTHROPIC_BASE_URL": "https://dgth.shop"
  },
  "theme": "auto"
}
```

### 3.2 模型映射

Antigravity 当前不要使用 `Opus 4.8`。建议这样映射：

| Claude Code 角色 | 显示名称 | 实际请求模型 |
| --- | --- | --- |
| Sonnet | `Sonnet 4.6` | `claude-sonnet-4-6` |
| Opus | `Opus 4.6` | `claude-opus-4-6` |
| Haiku | 可留空 | 可留空 |

如果需要思考模型，可以把 Opus 映射为 `claude-opus-4-6-thinking`。

### 3.3 常见错误

| 错误 | 原因 | 处理 |
| --- | --- | --- |
| selected model may not exist | 模型映射到了不可用模型 | 改回 `claude-sonnet-4-6` 或 `claude-opus-4-6` |
| 502 upstream error | 上游账号不支持或临时失败 | 换可用模型，或稍后重试 |
| 403 insufficient balance | 分组、额度或账号池不可用 | 联系管理员检查订阅和分组 |

## 4. 在 Codex / OpenAI-compatible 客户端中使用

适用于 Codex、Chatbox、Open WebUI、Cherry Studio、Cursor 等支持 OpenAI API 的客户端。

| 项目 | 填写 |
| --- | --- |
| Base URL | `https://dgth.shop/v1` |
| API Key | 你的 DGWay API Key |
| Chat 模型 | `gpt-5.6`、`gpt-5.6-sol`、`gpt-5.6-terra`、`gpt-5.6-luna`；兼容选项为 `gpt-5.4` 或 `gpt-5.4-mini` |
| Codex 模型 | `gpt-5.3-codex-spark` |
| 图片模型 | `gpt-image-1` 或 `gpt-image-2` |

文本测试：

```bash
curl https://dgth.shop/v1/chat/completions \
  -H "Authorization: Bearer sk-你的APIKey" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.4-mini",
    "messages": [
      {"role": "user", "content": "请回复 DGWay OK"}
    ]
  }'
```

图片测试：

```bash
curl https://dgth.shop/v1/images/generations \
  -H "Authorization: Bearer sk-你的APIKey" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image-2",
    "prompt": "生成一个简洁的蓝色字母 D 图标，白色背景",
    "size": "1024x1024",
    "n": 1
  }'
```

## 5. 在 Gemini 客户端中使用

如果客户端支持 Gemini API，可以使用：

| 项目 | 填写 |
| --- | --- |
| Base URL | `https://dgth.shop/v1beta` |
| API Key | 你的 Gemini 分组 DGWay API Key |
| 文本模型 | `gemini-2.5-flash`、`gemini-2.5-pro` |

Gemini 文本测试：

```bash
curl https://dgth.shop/v1beta/models \
  -H "Authorization: Bearer sk-你的APIKey"
```

当前普通 Gemini 分组只展示确认可用的文本模型。图片模型没有放进普通 Gemini 分组，避免用户看到不可用模型。

## 6. 当前可用模型

可用渠道页面只展示用户能调用的模型名称和定价，不展示后台分组名称。后台分组仍用于权限、调度和后续价格配置。

### GPT / OpenAI

| 能力 | 模型 |
| --- | --- |
| 聊天 | `gpt-5.6`、`gpt-5.6-sol`、`gpt-5.6-terra`、`gpt-5.6-luna`、`gpt-5.4`、`gpt-5.4-mini` |
| Codex | `gpt-5.3-codex-spark` |
| 图片生成 | `gpt-image-1`、`gpt-image-2` |

OpenAI OAuth 账号的后台“同步上游支持的模型”按钮当前不适用，管理员需要在账号白名单或分组模型列表里手动加入 `gpt-5.6` 系列。是否能成功调用，最终取决于该 OpenAI 账号本身是否已经获得 GPT-5.6 权限。

### Gemini

| 能力 | 模型 |
| --- | --- |
| 文本 | `gemini-2.5-flash`、`gemini-2.5-pro` |

### Antigravity

| 能力 | 模型 |
| --- | --- |
| Claude Code | `claude-haiku-4-5`、`claude-haiku-4-5-20251001`、`claude-opus-4-5-20251101`、`claude-opus-4-5-thinking`、`claude-opus-4-6`、`claude-opus-4-6-thinking`、`claude-opus-4-8-thinking`、`claude-sonnet-4-6` |
| Gemini 文本 | `gemini-2.5-flash`、`gemini-2.5-flash-lite`、`gemini-2.5-flash-thinking`、`gemini-3-flash`、`gemini-3-flash-agent`、`gemini-3-flash-preview`、`gemini-3-pro-high`、`gemini-3-pro-low`、`gemini-3-pro-preview`、`gemini-3.1-flash-lite`、`gemini-3.1-pro-low`、`gemini-3.5-flash-extra-low`、`gemini-3.5-flash-low`、`gemini-pro-agent`、`gpt-oss-120b-medium` |
| Gemini 图片 | `gemini-3.1-flash-image`、`gemini-3.1-flash-image-preview`、`gemini-3-pro-image`、`gemini-3-pro-image-preview` |

注意：Antigravity 模型清单按 2026-06-03 实测通过结果展示。`claude-opus-4-7`、`claude-opus-4-8`、`claude-sonnet-4-5`、`claude-sonnet-4-5-20250929`、`claude-sonnet-4-5-thinking`、`gemini-2.5-flash-image`、`gemini-2.5-flash-image-preview`、`chat_20706`、`chat_23310`、`gemini-2.5-pro`、`gemini-3.1-pro-high`、`gemini-3.1-pro-preview` 当前实测不可用或超时，不要展示给用户。

## 7. 额度说明

- GPT 聊天、Codex、图片生成在 DGWay 内按分组和模型分别计费，图片生成成本更高。
- Gemini 和 Antigravity 虽然可以使用同一个 Google 账号登录，但在 DGWay 里是两个不同平台账号，不要默认认为额度会互相扣减。
- Google 官方没有给普通 OAuth 场景提供完整用量查询接口，DGWay 页面里的 Gemini 配额是调度参考，最终以 Google 实际报错为准。
- Antigravity 的 Claude Code 模型和 Antigravity 的 Gemini 图片模型也要分开看，建议分组隔离。

## 8. 购买套餐

如果账号页面里显示“订阅套餐”或“余额充值”，可以直接选择套餐后扫码支付。

| 步骤 | 说明 |
| --- | --- |
| 选择套餐 | 确认套餐名称、有效期、额度和价格 |
| 选择支付方式 | 支持支付宝或微信扫码，具体以页面展示为准 |
| 确认支付规则 | 创建订单前会提示支付规则；恶意支付、争议支付、无效转账、重复支付，或未按页面订单金额完成的支付，平台不承诺退款 |
| 扫码付款 | 付款金额要和页面金额一致 |
| 等待回调 | 支付成功后页面会自动刷新订单状态 |
| 未到账 | 先点击订单查询/刷新；仍未到账时，把订单号发给管理员 |

支付二维码通常有有效期，超时后重新下单即可。不要重复支付同一个过期订单。

## 9. 购买账号服务

登录后，在左侧菜单点击“账号购买”。页面商品、价格、QQ 和说明以管理员后台配置为准，常见商品包括：

| 商品 | 价格 | 说明 |
| --- | --- | --- |
| OpenAI 成品账号 | 30 元/个 | 提供登录邮箱和验证码接收网址，管理员人工交付 |
| 长效手机号接码 | 10 元/30 天 | 30 天内可重复接码，最多尝试绑定 3 个 OpenAI 账号；实际数量受 OpenAI 风控影响 |
| 美国静态住宅 IP | 40 元/30 天 | 提供美国静态住宅网络出口，可降低 OpenAI 和其他 AI 服务的封控风险 |

点击页面下方“复制 QQ”或复制管理员配置的联系方式，并说明需要的商品和数量。购买前先确认库存、交付时间和使用要求；降低风控风险不代表完全消除风险。

管理员修改入口：`系统设置 -> 通用设置 -> 账号购买设置`。可以修改页面标题、说明、联系方式、底部提示，也可以新增、复制、删除、上移或下移商品。商品“功能点”输入框用中文逗号 `，` 或英文逗号 `,` 分隔，保存后前台会自动逐行展示；桌面端默认每行 3 个商品，超过 3 个自动换到下一行。

## 10. 用户排错顺序

请求失败时按这个顺序检查：

1. API Key 是否复制完整。
2. Base URL 是否填对。
3. 模型名是否在“当前可用模型”列表里。
4. API Key 绑定的分组是否正确。
5. 分组是否允许图片生成。
6. 订阅或余额是否还有额度。
7. 如果是 Claude Code，检查 CC Switch 模型映射是否正确。

最常见的问题是模型名不对、分组不对、图片生成没有开启。
