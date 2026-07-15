<template>
  <AppLayout>
    <div class="mx-auto w-full max-w-7xl space-y-6">
      <section class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 class="text-2xl font-bold tracking-normal text-gray-900 dark:text-white sm:text-3xl">
            {{ t('accountStore.hero.title') }}
          </h1>
          <p class="mt-2 text-sm leading-6 text-gray-500 dark:text-gray-400">
            {{ t('accountStore.hero.description') }}
          </p>
        </div>
        <div class="inline-flex items-center gap-2 text-sm font-medium text-emerald-700 dark:text-emerald-300">
          <span class="h-2 w-2 rounded-full bg-emerald-500 ring-4 ring-emerald-100 dark:ring-emerald-900/40"></span>
          {{ t('accountStore.hero.status') }}
        </div>
      </section>

      <section class="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
        <article
          data-testid="openai-product"
          class="flex min-h-[370px] flex-col rounded-lg border border-gray-200 border-t-[3px] border-t-primary-500 bg-white p-6 shadow-sm dark:border-dark-700 dark:border-t-primary-500 dark:bg-dark-900"
        >
          <div class="flex items-start justify-between gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-50 text-gray-900 dark:bg-primary-900/20 dark:text-white">
              <svg
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
            </div>
            <span class="rounded-md bg-primary-50 px-2.5 py-1 text-xs font-semibold text-primary-700 dark:bg-primary-900/30 dark:text-primary-300">
              {{ t('accountStore.products.openai.badge') }}
            </span>
          </div>
          <h2 class="mt-7 text-xl font-bold tracking-normal text-gray-900 dark:text-white">
            {{ t('accountStore.products.openai.title') }}
          </h2>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            {{ t('accountStore.products.openai.subtitle') }}
          </p>
          <div class="mt-7 flex items-end gap-1 text-gray-900 dark:text-white">
            <span class="pb-1 text-lg font-bold">¥</span>
            <span class="text-4xl font-bold leading-none">30</span>
            <span class="pb-1 text-sm text-gray-500 dark:text-gray-400">{{ t('accountStore.units.each') }}</span>
          </div>
          <ul class="mt-7 space-y-3 text-sm leading-6 text-gray-600 dark:text-gray-300">
            <li v-for="feature in openAiFeatures" :key="feature" class="flex items-start gap-3">
              <Icon name="check" size="sm" :stroke-width="2" class="mt-1 flex-shrink-0 text-primary-500" />
              <span>{{ feature }}</span>
            </li>
          </ul>
        </article>

        <article
          data-testid="phone-product"
          class="flex min-h-[370px] flex-col rounded-lg border border-gray-200 border-t-[3px] border-t-amber-400 bg-white p-6 shadow-sm dark:border-dark-700 dark:border-t-amber-400 dark:bg-dark-900"
        >
          <div class="flex items-start justify-between gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-amber-50 text-amber-600 dark:bg-amber-900/20 dark:text-amber-300">
              <Icon name="smartphone" size="lg" :stroke-width="2" />
            </div>
            <span class="rounded-md bg-primary-50 px-2.5 py-1 text-xs font-semibold text-primary-700 dark:bg-primary-900/30 dark:text-primary-300">
              {{ t('accountStore.products.phone.badge') }}
            </span>
          </div>
          <h2 class="mt-7 text-xl font-bold tracking-normal text-gray-900 dark:text-white">
            {{ t('accountStore.products.phone.title') }}
          </h2>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            {{ t('accountStore.products.phone.subtitle') }}
          </p>
          <div class="mt-7 flex items-end gap-1 text-gray-900 dark:text-white">
            <span class="pb-1 text-lg font-bold">¥</span>
            <span class="text-4xl font-bold leading-none">10</span>
            <span class="pb-1 text-sm text-gray-500 dark:text-gray-400">{{ t('accountStore.units.thirtyDays') }}</span>
          </div>
          <ul class="mt-7 space-y-3 text-sm leading-6 text-gray-600 dark:text-gray-300">
            <li v-for="feature in phoneFeatures" :key="feature" class="flex items-start gap-3">
              <Icon name="check" size="sm" :stroke-width="2" class="mt-1 flex-shrink-0 text-primary-500" />
              <span>{{ feature }}</span>
            </li>
          </ul>
          <p class="mt-4 border-l-2 border-amber-400 bg-amber-50 px-3 py-2 text-xs leading-5 text-amber-800 dark:bg-amber-900/15 dark:text-amber-300">
            {{ t('accountStore.products.phone.riskNote') }}
          </p>
        </article>

        <article
          data-testid="residential-ip-product"
          class="flex min-h-[370px] flex-col rounded-lg border border-gray-200 border-t-[3px] border-t-blue-500 bg-white p-6 shadow-sm dark:border-dark-700 dark:border-t-blue-500 dark:bg-dark-900"
        >
          <div class="flex items-start justify-between gap-4">
            <div
              data-testid="residential-ip-icon"
              class="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-300"
            >
              <Icon name="wifi" size="lg" :stroke-width="2" />
            </div>
            <span class="rounded-md bg-primary-50 px-2.5 py-1 text-xs font-semibold text-primary-700 dark:bg-primary-900/30 dark:text-primary-300">
              {{ t('accountStore.products.residentialIp.badge') }}
            </span>
          </div>
          <h2 class="mt-7 text-xl font-bold tracking-normal text-gray-900 dark:text-white">
            {{ t('accountStore.products.residentialIp.title') }}
          </h2>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            {{ t('accountStore.products.residentialIp.subtitle') }}
          </p>
          <div class="mt-7 flex items-end gap-1 text-gray-900 dark:text-white">
            <span class="pb-1 text-lg font-bold">¥</span>
            <span class="text-4xl font-bold leading-none">40</span>
            <span class="pb-1 text-sm text-gray-500 dark:text-gray-400">{{ t('accountStore.units.thirtyDays') }}</span>
          </div>
          <ul class="mt-7 space-y-3 text-sm leading-6 text-gray-600 dark:text-gray-300">
            <li v-for="feature in residentialIpFeatures" :key="feature" class="flex items-start gap-3">
              <Icon name="check" size="sm" :stroke-width="2" class="mt-1 flex-shrink-0 text-primary-500" />
              <span>{{ feature }}</span>
            </li>
          </ul>
        </article>
      </section>

      <section class="flex flex-col gap-4 rounded-lg border border-gray-200 bg-white p-5 sm:flex-row sm:items-center sm:justify-between dark:border-dark-700 dark:bg-dark-900">
        <div class="flex min-w-0 items-center gap-4">
          <div class="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-lg bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-300">
            <Icon name="chat" size="lg" />
          </div>
          <div class="min-w-0">
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ t('accountStore.contact.label') }}</p>
            <p data-testid="contact-qq" class="mt-1 truncate text-lg font-bold text-gray-900 dark:text-white">
              {{ contactQQ }}
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
          {{ copied ? t('accountStore.contact.copiedShort') : t('accountStore.contact.copy') }}
        </button>
      </section>

      <p class="text-xs leading-5 text-gray-400 dark:text-gray-500">
        {{ t('accountStore.disclaimer') }}
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

const { t } = useI18n()
const appStore = useAppStore()
const { copied, copyToClipboard } = useClipboard()

const contactQQ = computed(() => appStore.contactInfo.trim() || '484018742')
const openAiFeatures = computed(() => [
  t('accountStore.products.openai.features.email'),
  t('accountStore.products.openai.features.decoder'),
  t('accountStore.products.openai.features.delivery')
])
const phoneFeatures = computed(() => [
  t('accountStore.products.phone.features.reusable'),
  t('accountStore.products.phone.features.accounts')
])
const residentialIpFeatures = computed(() => [
  t('accountStore.products.residentialIp.features.usStatic'),
  t('accountStore.products.residentialIp.features.period'),
  t('accountStore.products.residentialIp.features.openaiRisk'),
  t('accountStore.products.residentialIp.features.otherAiRisk')
])

const openAiLogoPath = 'M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z'

function copyContact() {
  void copyToClipboard(contactQQ.value, t('accountStore.contact.copied'))
}
</script>
