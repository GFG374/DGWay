import { describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import SupportedModelChip from '../SupportedModelChip.vue'
import type { UserSupportedModel } from '@/api/channels'

vi.mock('vue-i18n', async () => {
  const actual = await vi.importActual<typeof import('vue-i18n')>('vue-i18n')
  return {
    ...actual,
    useI18n: () => ({
      t: (key: string) => key,
    }),
  }
})

function model(name: string, platform: string): UserSupportedModel {
  return {
    name,
    display_name: name,
    platform,
    capability: 'chat',
    available: true,
    pricing: null,
  }
}

describe('SupportedModelChip native icon', () => {
  it('uses Anthropic icon for Claude models routed through Antigravity', () => {
    const wrapper = mount(SupportedModelChip, {
      props: {
        model: model('claude-sonnet-4-6', 'antigravity'),
        showPlatform: false,
      },
      global: {
        stubs: {
          PlatformIcon: {
            props: ['platform'],
            template: '<span class="platform-icon" :data-platform="platform" />',
          },
          Teleport: true,
        },
      },
    })

    expect(wrapper.find('.platform-icon').attributes('data-platform')).toBe('anthropic')
    expect(wrapper.text()).not.toContain('antigravity')
  })

  it('uses Gemini icon for Gemini models routed through Antigravity', () => {
    const wrapper = mount(SupportedModelChip, {
      props: {
        model: model('gemini-3-pro-image', 'antigravity'),
        showPlatform: false,
      },
      global: {
        stubs: {
          PlatformIcon: {
            props: ['platform'],
            template: '<span class="platform-icon" :data-platform="platform" />',
          },
          Teleport: true,
        },
      },
    })

    expect(wrapper.find('.platform-icon').attributes('data-platform')).toBe('gemini')
    expect(wrapper.text()).not.toContain('antigravity')
  })
})
