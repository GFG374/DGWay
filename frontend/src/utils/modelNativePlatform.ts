export function nativeModelPlatform(_modelName: string, fallbackPlatform = ''): string {
  const model = _modelName.trim().toLowerCase().replace(/^models\//, '')
  if (model.startsWith('claude-')) return 'anthropic'
  if (
    model.startsWith('gemini-') ||
    model.startsWith('nanobanana') ||
    model.includes('flash_lite') ||
    model.includes('flash-lite')
  ) {
    return 'gemini'
  }
  if (
    model.startsWith('gpt-') ||
    model.startsWith('codex-') ||
    model.startsWith('o1') ||
    model.startsWith('o3') ||
    model.startsWith('o4')
  ) {
    return 'openai'
  }
  return fallbackPlatform
}
