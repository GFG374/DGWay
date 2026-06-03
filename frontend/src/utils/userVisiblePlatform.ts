import { nativeModelPlatform } from '@/utils/modelNativePlatform'

export const USER_VISIBLE_PLATFORM_ORDER = ['anthropic', 'openai', 'gemini'] as const

export type UserVisiblePlatform = (typeof USER_VISIBLE_PLATFORM_ORDER)[number]

export function userVisiblePlatformForModel(modelName: string, fallbackPlatform = ''): UserVisiblePlatform | '' {
  const platform = nativeModelPlatform(modelName, fallbackPlatform)
  if (platform === 'anthropic' || platform === 'openai' || platform === 'gemini') {
    return platform
  }
  return ''
}

export function userVisiblePlatformLabel(platform: string): string {
  switch (platform) {
    case 'anthropic':
      return 'Claude'
    case 'openai':
      return 'OpenAI'
    case 'gemini':
      return 'Gemini'
    default:
      return platform
  }
}
