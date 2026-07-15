<template>
  <AppLayout>
    <div class="mx-auto w-full max-w-7xl space-y-6">
      <section class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 class="text-2xl font-bold tracking-normal text-gray-900 dark:text-white sm:text-3xl">
            {{ accountStoreConfig.title }}
          </h1>
          <p class="mt-2 text-sm leading-6 text-gray-500 dark:text-gray-400">
            {{ accountStoreConfig.description }}
          </p>
        </div>
        <div class="inline-flex items-center gap-2 text-sm font-medium text-emerald-700 dark:text-emerald-300">
          <span class="h-2 w-2 rounded-full bg-emerald-500 ring-4 ring-emerald-100 dark:ring-emerald-900/40"></span>
          {{ accountStoreConfig.status_text }}
        </div>
      </section>

      <section class="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
        <article
          v-for="product in visibleProducts"
          :key="product.id"
          :data-testid="product.testId"
          :class="[
            'flex min-h-[370px] flex-col rounded-lg border border-gray-200 border-t-[3px] bg-white p-6 shadow-sm dark:border-dark-700 dark:bg-dark-900',
            colorClasses(product.color).border
          ]"
        >
          <div class="flex items-start justify-between gap-4">
            <div
              :data-testid="product.icon === 'residential-ip' ? 'residential-ip-icon' : undefined"
              :class="[
                'flex h-12 w-12 items-center justify-center rounded-lg',
                colorClasses(product.color).icon
              ]"
            >
              <img
                v-if="product.icon_image"
                data-testid="product-icon-image"
                :src="product.icon_image"
                :alt="product.title"
                class="h-8 w-8 object-contain"
                loading="lazy"
              />
              <svg
                v-else-if="product.icon === 'openai'"
                data-testid="openai-logo"
                class="h-7 w-7"
                fill="currentColor"
                fill-rule="evenodd"
                viewBox="0 0 24 24"
                role="img"
                aria-label="OpenAI"
              >
                <path :d="openAiLogoPath" />
              </svg>
              <span v-else-if="product.icon === 'gemini'" class="text-lg font-bold leading-none">G</span>
              <Icon v-else :name="iconName(product.icon)" size="lg" :stroke-width="2" />
            </div>
            <span :class="['rounded-md px-2.5 py-1 text-xs font-semibold', colorClasses(product.color).badge]">
              {{ product.badge }}
            </span>
          </div>
          <h2 class="mt-7 text-xl font-bold tracking-normal text-gray-900 dark:text-white">
            {{ product.title }}
          </h2>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            {{ product.subtitle }}
          </p>
          <div class="mt-7 flex items-end gap-1 text-gray-900 dark:text-white">
            <span class="pb-1 text-lg font-bold">{{ product.currency }}</span>
            <span class="text-4xl font-bold leading-none">{{ product.price }}</span>
            <span class="pb-1 text-sm text-gray-500 dark:text-gray-400">{{ product.unit }}</span>
          </div>
          <ul class="mt-7 space-y-3 text-sm leading-6 text-gray-600 dark:text-gray-300">
            <li
              v-for="feature in normalizedFeatures(product.features)"
              :key="`${product.id}-${feature}`"
              data-testid="product-feature"
              class="flex items-start gap-3"
            >
              <Icon name="check" size="sm" :stroke-width="2" class="mt-1 flex-shrink-0 text-primary-500" />
              <span>{{ feature }}</span>
            </li>
          </ul>
          <p
            v-if="product.risk_note"
            class="mt-4 border-l-2 border-amber-400 bg-amber-50 px-3 py-2 text-xs leading-5 text-amber-800 dark:bg-amber-900/15 dark:text-amber-300"
          >
            {{ product.risk_note }}
          </p>
        </article>
      </section>

      <section class="flex flex-col gap-4 rounded-lg border border-gray-200 bg-white p-5 sm:flex-row sm:items-center sm:justify-between dark:border-dark-700 dark:bg-dark-900">
        <div class="flex min-w-0 items-center gap-4">
          <div class="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-lg bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-300">
            <Icon :name="contactIcon" size="lg" />
          </div>
          <div class="min-w-0">
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ accountStoreConfig.contact.label }}</p>
            <p data-testid="contact-qq" class="mt-1 truncate text-lg font-bold text-gray-900 dark:text-white">
              {{ contactValue }}
            </p>
          </div>
        </div>
        <button
          type="button"
          data-testid="copy-contact"
          class="btn btn-primary min-h-11 w-full flex-shrink-0 sm:w-auto"
          @click="copyContact"
        >
          <Icon :name="copied ? 'check' : 'copy'" size="sm" class="mr-2" />
          {{ copied ? t('accountStore.contact.copiedShort') : accountStoreConfig.contact.copy_label }}
        </button>
      </section>

      <p class="text-xs leading-5 text-gray-400 dark:text-gray-500">
        {{ accountStoreConfig.disclaimer }}
      </p>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import AppLayout from '@/components/layout/AppLayout.vue'
import Icon from '@/components/icons/Icon.vue'
import { useClipboard } from '@/composables/useClipboard'
import { useAppStore } from '@/stores/app'
import type { AccountStoreConfig, AccountStoreProduct } from '@/types'

type StoreProduct = AccountStoreProduct & { testId: string }
type ProductColor = 'primary' | 'amber' | 'blue' | 'purple' | 'gray'
type StoreIcon = NonNullable<AccountStoreProduct['icon']>

const { t } = useI18n()
const appStore = useAppStore()
const { copied, copyToClipboard } = useClipboard()

const defaultConfig = computed<AccountStoreConfig>(() => ({
  enabled: true,
  title: t('accountStore.hero.title'),
  description: t('accountStore.hero.description'),
  status_text: t('accountStore.hero.status'),
  contact: {
    type: 'qq',
    value: appStore.contactInfo.trim() || '484018742',
    label: t('accountStore.contact.label'),
    copy_label: t('accountStore.contact.copy')
  },
  disclaimer: t('accountStore.disclaimer'),
  products: [
    {
      id: 'openai',
      enabled: true,
      title: t('accountStore.products.openai.title'),
      subtitle: t('accountStore.products.openai.subtitle'),
      price: '30',
      currency: '¥',
      unit: t('accountStore.units.each'),
      badge: t('accountStore.products.openai.badge'),
      icon: 'openai',
      color: 'primary',
      features: [
        t('accountStore.products.openai.features.email'),
        t('accountStore.products.openai.features.decoder'),
        t('accountStore.products.openai.features.delivery')
      ],
      risk_note: ''
    },
    {
      id: 'phone',
      enabled: true,
      title: t('accountStore.products.phone.title'),
      subtitle: t('accountStore.products.phone.subtitle'),
      price: '10',
      currency: '¥',
      unit: t('accountStore.units.thirtyDays'),
      badge: t('accountStore.products.phone.badge'),
      icon: 'smartphone',
      color: 'amber',
      features: [
        t('accountStore.products.phone.features.reusable'),
        t('accountStore.products.phone.features.accounts')
      ],
      risk_note: t('accountStore.products.phone.riskNote')
    },
    {
      id: 'residential-ip',
      enabled: true,
      title: t('accountStore.products.residentialIp.title'),
      subtitle: t('accountStore.products.residentialIp.subtitle'),
      price: '40',
      currency: '¥',
      unit: t('accountStore.units.thirtyDays'),
      badge: t('accountStore.products.residentialIp.badge'),
      icon: 'residential-ip',
      color: 'blue',
      features: [
        t('accountStore.products.residentialIp.features.usStatic'),
        t('accountStore.products.residentialIp.features.period'),
        t('accountStore.products.residentialIp.features.openaiRisk'),
        t('accountStore.products.residentialIp.features.otherAiRisk')
      ],
      risk_note: ''
    }
  ]
}))

const accountStoreConfig = computed<AccountStoreConfig>(() => {
  const configured = appStore.cachedPublicSettings?.account_store_config
  if (!configured || configured.enabled === false) {
    return defaultConfig.value
  }

  return {
    ...defaultConfig.value,
    ...configured,
    contact: {
      ...defaultConfig.value.contact,
      ...(configured.contact ?? {})
    },
    products: Array.isArray(configured.products) && configured.products.length > 0
      ? configured.products
      : defaultConfig.value.products
  }
})

const visibleProducts = computed<StoreProduct[]>(() =>
  accountStoreConfig.value.products
    .filter((product) => product.enabled !== false)
    .map((product) => ({
      ...product,
      id: product.id || product.title,
      testId: product.id === 'openai'
        ? 'openai-product'
        : product.id === 'phone'
          ? 'phone-product'
          : product.id === 'residential-ip'
            ? 'residential-ip-product'
            : `product-${product.id || product.title}`
    }))
)

const contactValue = computed(() =>
  accountStoreConfig.value.contact.value.trim() || appStore.contactInfo.trim() || '484018742'
)

const contactIcon = computed(() => {
  switch (accountStoreConfig.value.contact.type) {
    case 'email':
      return 'mail'
    case 'wechat':
    case 'qq':
    case 'custom':
    default:
      return 'chat'
  }
})

function normalizedFeatures(features: string[] = []): string[] {
  return features
    .flatMap((feature) => String(feature).split(/[，,]/))
    .map((feature) => feature.trim())
    .filter(Boolean)
}

function iconName(icon: StoreIcon) {
  switch (icon) {
    case 'phone':
    case 'smartphone':
      return 'smartphone'
    case 'wifi':
    case 'residential-ip':
      return 'wifi'
    case 'mail':
      return 'mail'
    case 'key':
      return 'key'
    case 'globe':
      return 'globe'
    default:
      return 'key'
  }
}

function colorClasses(color: string = 'primary') {
  const classes = {
    primary: {
      border: 'border-t-primary-500 dark:border-t-primary-500',
      icon: 'bg-primary-50 text-gray-900 dark:bg-primary-900/20 dark:text-white',
      badge: 'bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
    },
    amber: {
      border: 'border-t-amber-400 dark:border-t-amber-400',
      icon: 'bg-amber-50 text-amber-600 dark:bg-amber-900/20 dark:text-amber-300',
      badge: 'bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
    },
    blue: {
      border: 'border-t-blue-500 dark:border-t-blue-500',
      icon: 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-300',
      badge: 'bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
    },
    purple: {
      border: 'border-t-violet-500 dark:border-t-violet-500',
      icon: 'bg-violet-50 text-violet-700 dark:bg-violet-900/20 dark:text-violet-300',
      badge: 'bg-violet-50 text-violet-700 dark:bg-violet-900/30 dark:text-violet-300'
    },
    gray: {
      border: 'border-t-gray-400 dark:border-t-gray-500',
      icon: 'bg-gray-100 text-gray-700 dark:bg-dark-700 dark:text-gray-200',
      badge: 'bg-gray-100 text-gray-700 dark:bg-dark-700 dark:text-gray-200'
    }
  } satisfies Record<string, { border: string; icon: string; badge: string }>

  return classes[color as ProductColor] ?? classes.primary
}

const openAiLogoPath = 'M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z'

function copyContact() {
  void copyToClipboard(contactValue.value, t('accountStore.contact.copied'))
}
</script>
