import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'

import AvailableChannelsTable from '../AvailableChannelsTable.vue'
import type { UserAvailableChannel } from '@/api/channels'

const rows: UserAvailableChannel[] = [
  {
    name: 'Antigravity',
    description: 'OAuth upstream',
    platforms: [
      {
        platform: 'antigravity',
        supported_models: [
          {
            name: 'claude-sonnet-4-6',
            display_name: 'Claude Sonnet 4.6',
            platform: 'antigravity',
            capability: 'claude-code',
            available: true,
            pricing: null,
          },
          {
            name: 'gemini-3-pro-image',
            display_name: 'Gemini 3 Pro Image',
            platform: 'antigravity',
            capability: 'gemini-image',
            available: true,
            pricing: null,
          },
        ],
      },
    ],
  },
]

describe('AvailableChannelsTable', () => {
  it('shows available model names without exposing group names', () => {
    const wrapper = mount(AvailableChannelsTable, {
      props: {
        columns: {
          name: '渠道名',
          description: '描述',
          platform: '平台',
          supportedModels: '可用模型',
        },
        rows,
        loading: false,
        pricingKeyPrefix: 'availableChannels.pricing',
        noPricingLabel: '未配置定价',
        noModelsLabel: '未配置模型',
        emptyLabel: '暂无可用渠道',
      },
      global: {
        stubs: {
          Icon: true,
          PlatformIcon: true,
          SupportedModelChip: {
            props: ['model'],
            template: '<span class="model-chip">{{ model.name }}</span>',
          },
        },
      },
    })

    const text = wrapper.text()
    expect(text).toContain('可用模型')
    expect(text).toContain('claude-sonnet-4-6')
    expect(text).toContain('gemini-3-pro-image')
    expect(text).not.toContain('我可访问的分组')
    expect(text).not.toContain('测试分组')
  })
})
