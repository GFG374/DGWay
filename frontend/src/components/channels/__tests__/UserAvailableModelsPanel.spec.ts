import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'

import UserAvailableModelsPanel from '../UserAvailableModelsPanel.vue'
import type { UserChannelPlatformSection } from '@/api/channels'

describe('UserAvailableModelsPanel', () => {
  it('renders public platform sections without exposing raw channel names', () => {
    const sections: UserChannelPlatformSection[] = [
      {
        platform: 'anthropic',
        supported_models: [
          {
            name: 'claude-sonnet-4-6',
            display_name: 'Claude Sonnet 4.6',
            platform: 'anthropic',
            capability: 'claude-code',
            available: true,
            pricing: null,
          },
        ],
      },
      {
        platform: 'gemini',
        supported_models: [
          {
            name: 'gemini-3-pro-image',
            display_name: 'Gemini 3 Pro Image',
            platform: 'gemini',
            capability: 'gemini-image',
            available: true,
            pricing: null,
          },
        ],
      },
    ]

    const wrapper = mount(UserAvailableModelsPanel, {
      props: {
        sections,
        loading: false,
        pricingKeyPrefix: 'availableChannels.pricing',
        noPricingLabel: '未配置定价',
        emptyLabel: '暂无可用渠道',
      },
      global: {
        stubs: {
          Icon: true,
          PlatformIcon: true,
          SupportedModelChip: {
            props: ['model'],
            template: '<span class="model-chip">{{ model.display_name }}</span>',
          },
        },
      },
    })

    const text = wrapper.text()
    expect(text).toContain('Claude')
    expect(text).toContain('Gemini')
    expect(text).toContain('Claude Sonnet 4.6')
    expect(text).toContain('Gemini 3 Pro Image')
    expect(text).not.toContain('Antigravity')
    expect(text).not.toContain('Google Gemini')
  })
})
