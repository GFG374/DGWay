<template>
  <div v-if="loading" class="card py-10 text-center">
    <Icon name="refresh" size="lg" class="inline-block animate-spin text-gray-400" />
  </div>

  <div v-else-if="sections.length === 0" class="card py-12 text-center">
    <Icon name="inbox" size="xl" class="mx-auto mb-3 h-12 w-12 text-gray-400" />
    <p class="text-sm text-gray-500 dark:text-gray-400">{{ emptyLabel }}</p>
  </div>

  <div v-else class="grid gap-4 xl:grid-cols-3">
    <section
      v-for="section in sections"
      :key="section.platform"
      class="card overflow-hidden"
    >
      <div
        class="flex items-center justify-between gap-3 border-b px-4 py-3 dark:border-dark-700"
      >
        <div class="flex min-w-0 items-center gap-2">
          <span
            :class="[
              'inline-flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg border',
              platformBadgeClass(section.platform),
            ]"
          >
            <PlatformIcon :platform="section.platform as GroupPlatform" size="sm" />
          </span>
          <div class="min-w-0">
            <h3 class="truncate text-sm font-semibold text-gray-900 dark:text-white">
              {{ userVisiblePlatformLabel(section.platform) }}
            </h3>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              {{ section.supported_models.length }} 个可用模型
            </p>
          </div>
        </div>
        <span
          :class="[
            'rounded-md border px-2 py-0.5 text-[11px] font-medium uppercase',
            platformBadgeClass(section.platform),
          ]"
        >
          {{ userVisiblePlatformLabel(section.platform) }}
        </span>
      </div>

      <div class="max-h-[420px] overflow-y-auto px-4 py-4">
        <div class="flex flex-wrap gap-1.5">
          <SupportedModelChip
            v-for="model in section.supported_models"
            :key="`${section.platform}-${model.name}`"
            :model="model"
            :pricing-key-prefix="pricingKeyPrefix"
            :no-pricing-label="noPricingLabel"
            :show-platform="false"
            :platform-hint="section.platform"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import Icon from '@/components/icons/Icon.vue'
import PlatformIcon from '@/components/common/PlatformIcon.vue'
import SupportedModelChip from './SupportedModelChip.vue'
import type { UserChannelPlatformSection } from '@/api/channels'
import type { GroupPlatform } from '@/types'
import { platformBadgeClass } from '@/utils/platformColors'
import { userVisiblePlatformLabel } from '@/utils/userVisiblePlatform'

defineProps<{
  sections: UserChannelPlatformSection[]
  loading: boolean
  pricingKeyPrefix: string
  noPricingLabel: string
  emptyLabel: string
}>()
</script>
