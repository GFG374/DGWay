import { describe, expect, it } from 'vitest'

import { nativeModelPlatform } from '../modelNativePlatform'

describe('nativeModelPlatform', () => {
  it('maps Antigravity Claude models to Anthropic branding', () => {
    expect(nativeModelPlatform('claude-sonnet-4-6', 'antigravity')).toBe('anthropic')
    expect(nativeModelPlatform('claude-opus-4-8-thinking', 'antigravity')).toBe('anthropic')
  })

  it('maps Antigravity Gemini models to Gemini branding', () => {
    expect(nativeModelPlatform('gemini-3-pro-image', 'antigravity')).toBe('gemini')
    expect(nativeModelPlatform('gemini-3.5-flash-low', 'antigravity')).toBe('gemini')
    expect(nativeModelPlatform('tab_flash_lite_preview', 'antigravity')).toBe('gemini')
    expect(nativeModelPlatform('nanobananapro', 'antigravity')).toBe('gemini')
  })

  it('keeps OpenAI and unknown models on their routing platform', () => {
    expect(nativeModelPlatform('gpt-5.5', 'openai')).toBe('openai')
    expect(nativeModelPlatform('custom-model', 'antigravity')).toBe('antigravity')
  })
})
