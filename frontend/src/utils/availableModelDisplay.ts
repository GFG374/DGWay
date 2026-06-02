export type ModelCapability =
  | 'chat'
  | 'image'
  | 'codex'
  | 'claude-code'
  | 'gemini-text'
  | 'gemini-image'

export function modelCapabilityLabel(capability: string | null | undefined): string {
  switch (capability) {
    case 'image':
      return 'GPT 生图'
    case 'codex':
      return 'Codex'
    case 'claude-code':
      return 'Claude Code'
    case 'gemini-text':
      return 'Gemini 文本'
    case 'gemini-image':
      return 'Gemini 生图'
    case 'chat':
      return 'GPT 聊天'
    default:
      return capability || '模型'
  }
}

export function modelStatusLabel(available: boolean): string {
  return available ? '可用' : '不可用'
}
