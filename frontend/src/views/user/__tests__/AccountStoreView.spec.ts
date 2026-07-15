import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import AccountStoreView from '@/views/user/AccountStoreView.vue'

const { copyToClipboardMock } = vi.hoisted(() => ({
  copyToClipboardMock: vi.fn()
}))

vi.mock('@/stores/app', () => ({
  useAppStore: () => ({ contactInfo: '484018742' })
}))

vi.mock('@/composables/useClipboard', () => ({
  useClipboard: () => ({
    copied: ref(false),
    copyToClipboard: copyToClipboardMock
  })
}))

vi.mock('vue-i18n', async (importOriginal) => {
  const actual = await importOriginal<typeof import('vue-i18n')>()
  return {
    ...actual,
    useI18n: () => ({ t: (key: string) => key })
  }
})

describe('AccountStoreView', () => {
  beforeEach(() => {
    copyToClipboardMock.mockReset()
    copyToClipboardMock.mockResolvedValue(true)
  })

  function mountView() {
    return mount(AccountStoreView, {
      global: {
        stubs: {
          AppLayout: { template: '<div><slot /></div>' },
          Icon: { template: '<span class="icon-stub" />' }
        }
      }
    })
  }

  it('renders the three self-operated services and their approved prices', () => {
    const wrapper = mountView()

    expect(wrapper.get('[data-testid="openai-product"]').text()).toContain('accountStore.products.openai.title')
    expect(wrapper.get('[data-testid="openai-product"]').text()).toContain('30')
    expect(wrapper.get('[data-testid="phone-product"]').text()).toContain('accountStore.products.phone.title')
    expect(wrapper.get('[data-testid="phone-product"]').text()).toContain('10')
    expect(wrapper.get('[data-testid="residential-ip-product"]').text()).toContain('accountStore.products.residentialIp.title')
    expect(wrapper.get('[data-testid="residential-ip-product"]').text()).toContain('40')
  })

  it('renders local OpenAI branding and a residential network icon', () => {
    const wrapper = mountView()

    expect(wrapper.get('[data-testid="openai-logo"]').attributes('aria-label')).toBe('OpenAI')
    expect(wrapper.get('[data-testid="residential-ip-icon"]').exists()).toBe(true)
  })

  it('copies the configured administrator QQ', async () => {
    const wrapper = mountView()

    expect(wrapper.get('[data-testid="contact-qq"]').text()).toBe('484018742')
    await wrapper.get('[data-testid="copy-contact"]').trigger('click')

    expect(copyToClipboardMock).toHaveBeenCalledWith(
      '484018742',
      'accountStore.contact.copied'
    )
  })
})
