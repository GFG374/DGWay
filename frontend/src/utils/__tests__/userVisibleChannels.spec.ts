import { describe, expect, it } from 'vitest'
import type { UserAvailableChannel } from '@/api/channels'
import { availableChannelsForViewer, toUserVisibleChannels } from '@/utils/userVisibleChannels'

describe('userVisibleChannels', () => {
  it('splits raw Antigravity models into Claude and Gemini user-facing sections', () => {
    const rows: UserAvailableChannel[] = [
      {
        name: 'AG',
        description: '',
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

    const [channel] = toUserVisibleChannels(rows)

    expect(channel.platforms.map((p) => p.platform)).toEqual(['anthropic', 'gemini'])
    expect(channel.platforms[0].supported_models[0].platform).toBe('anthropic')
    expect(channel.platforms[1].supported_models[0].platform).toBe('gemini')
  })

  it('drops models that cannot be mapped to a public platform', () => {
    const rows: UserAvailableChannel[] = [
      {
        name: 'AG',
        description: '',
        platforms: [
          {
            platform: 'antigravity',
            supported_models: [
              {
                name: 'chat_20706',
                display_name: 'chat_20706',
                platform: 'antigravity',
                capability: 'chat',
                available: true,
                pricing: null,
              },
            ],
          },
        ],
      },
    ]

    expect(toUserVisibleChannels(rows)).toEqual([])
  })

  it('keeps raw Antigravity platform visible for admins only', () => {
    const rows: UserAvailableChannel[] = [
      {
        name: 'AG',
        description: '',
        platforms: [
          {
            platform: 'antigravity',
            supported_models: [
              {
                name: 'chat_20706',
                display_name: 'chat_20706',
                platform: 'antigravity',
                capability: 'chat',
                available: true,
                pricing: null,
              },
            ],
          },
        ],
      },
    ]

    expect(availableChannelsForViewer(rows, true)).toBe(rows)
    expect(availableChannelsForViewer(rows, false)).toEqual([])
  })
})
