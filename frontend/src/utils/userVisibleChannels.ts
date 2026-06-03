import type { UserAvailableChannel, UserChannelPlatformSection } from '@/api/channels'
import {
  USER_VISIBLE_PLATFORM_ORDER,
  type UserVisiblePlatform,
  userVisiblePlatformForModel,
} from '@/utils/userVisiblePlatform'

export function toUserVisibleChannels(list: UserAvailableChannel[]): UserAvailableChannel[] {
  return list
    .map((ch) => {
      const byPlatform = new Map<string, UserAvailableChannel['platforms'][number]>()
      const seen = new Set<string>()

      for (const section of ch.platforms) {
        for (const model of section.supported_models) {
          const visiblePlatform = userVisiblePlatformForModel(
            model.name,
            model.platform || section.platform,
          )
          if (!visiblePlatform) continue

          const key = `${visiblePlatform}:${model.name.toLowerCase()}`
          if (seen.has(key)) continue
          seen.add(key)

          if (!byPlatform.has(visiblePlatform)) {
            byPlatform.set(visiblePlatform, {
              platform: visiblePlatform,
              supported_models: [],
            })
          }
          byPlatform.get(visiblePlatform)?.supported_models.push({
            ...model,
            platform: visiblePlatform,
          })
        }
      }

      const platforms = [...byPlatform.values()].sort((a, b) => {
        const ai = USER_VISIBLE_PLATFORM_ORDER.indexOf(a.platform as UserVisiblePlatform)
        const bi = USER_VISIBLE_PLATFORM_ORDER.indexOf(b.platform as UserVisiblePlatform)
        return ai - bi
      })

      return platforms.length > 0 ? { ...ch, platforms } : null
    })
    .filter((ch): ch is UserAvailableChannel => ch !== null)
}

export function availableChannelsForViewer(
  list: UserAvailableChannel[],
  isAdmin: boolean,
): UserAvailableChannel[] {
  return isAdmin ? list : toUserVisibleChannels(list)
}

export function toUserVisiblePlatformSections(list: UserAvailableChannel[]): UserChannelPlatformSection[] {
  const byPlatform = new Map<string, UserChannelPlatformSection>()
  const seen = new Set<string>()

  for (const channel of toUserVisibleChannels(list)) {
    for (const section of channel.platforms) {
      if (!byPlatform.has(section.platform)) {
        byPlatform.set(section.platform, {
          platform: section.platform,
          supported_models: [],
        })
      }

      const target = byPlatform.get(section.platform)
      for (const model of section.supported_models) {
        const key = `${section.platform}:${model.name.toLowerCase()}`
        if (seen.has(key)) continue
        seen.add(key)
        target?.supported_models.push(model)
      }
    }
  }

  return [...byPlatform.values()].sort((a, b) => {
    const ai = USER_VISIBLE_PLATFORM_ORDER.indexOf(a.platform as UserVisiblePlatform)
    const bi = USER_VISIBLE_PLATFORM_ORDER.indexOf(b.platform as UserVisiblePlatform)
    return ai - bi
  })
}
