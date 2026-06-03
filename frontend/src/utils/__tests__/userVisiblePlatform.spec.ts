import { describe, expect, it } from 'vitest'
import { userVisiblePlatformForModel, userVisiblePlatformLabel } from '@/utils/userVisiblePlatform'

describe('userVisiblePlatform', () => {
  it('maps Antigravity Claude and Gemini models to user-facing platforms', () => {
    expect(userVisiblePlatformForModel('claude-sonnet-4-6', 'antigravity')).toBe('anthropic')
    expect(userVisiblePlatformForModel('gemini-3-pro-image', 'antigravity')).toBe('gemini')
  })

  it('keeps OpenAI models user-facing and hides raw Antigravity platform', () => {
    expect(userVisiblePlatformForModel('gpt-5.4', 'openai')).toBe('openai')
    expect(userVisiblePlatformForModel('unknown-model', 'antigravity')).toBe('')
  })

  it('labels Anthropic platform as Claude for users', () => {
    expect(userVisiblePlatformLabel('anthropic')).toBe('Claude')
    expect(userVisiblePlatformLabel('openai')).toBe('OpenAI')
    expect(userVisiblePlatformLabel('gemini')).toBe('Gemini')
  })
})
