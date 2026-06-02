import { describe, expect, it } from 'vitest'
import { modelCapabilityLabel, modelStatusLabel } from '@/utils/availableModelDisplay'

describe('availableModelDisplay', () => {
  it('maps capabilities to compact user labels', () => {
    expect(modelCapabilityLabel('image')).toBe('GPT 生图')
    expect(modelCapabilityLabel('codex')).toBe('Codex')
    expect(modelCapabilityLabel('gemini-image')).toBe('Gemini 生图')
    expect(modelCapabilityLabel('claude-code')).toBe('Claude Code')
  })

  it('marks available models without exposing diagnostics', () => {
    expect(modelStatusLabel(true)).toBe('可用')
    expect(modelStatusLabel(false)).toBe('不可用')
  })
})
