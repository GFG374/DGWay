import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import AccountStoreView from '@/views/user/AccountStoreView.vue'

const { copyToClipboardMock, mockAppStore } = vi.hoisted(() => ({
  copyToClipboardMock: vi.fn(),
  mockAppStore: {
    contactInfo: '484018742',
    cachedPublicSettings: null as any
  }
}))

vi.mock('@/stores/app', () => ({
  useAppStore: () => mockAppStore
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
    mockAppStore.contactInfo = '484018742'
    mockAppStore.cachedPublicSettings = null
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

  it('renders configured products and splits comma-separated features into rows', async () => {
    mockAppStore.cachedPublicSettings = {
      account_store_config: {
        enabled: true,
        title: '站长自营',
        description: '纯手搓账号，一号一 IP，稳定。',
        status_text: '人工服务正常',
        contact: {
          type: 'qq',
          value: '123456',
          label: '联系站长购买，请添加 QQ',
          copy_label: '复制 QQ'
        },
        disclaimer: '购买前请确认库存。',
        products: [
          {
            id: 'gemini',
            enabled: true,
            title: 'Gemini 成品账号',
            subtitle: '适合 Google AI 使用',
            price: '35',
            currency: '¥',
            unit: '/个',
            badge: '账号服务',
            icon: 'gemini',
            color: 'purple',
            features: ['提供登录邮箱，提供验证码接收网址，人工交付'],
            risk_note: ''
          }
        ]
      }
    }

    const wrapper = mountView()

    expect(wrapper.text()).toContain('Gemini 成品账号')
    expect(wrapper.text()).toContain('35')
    expect(wrapper.findAll('[data-testid="product-feature"]')).toHaveLength(3)
    expect(wrapper.get('[data-testid="contact-qq"]').text()).toBe('123456')

    await wrapper.get('[data-testid="copy-contact"]').trigger('click')
    expect(copyToClipboardMock).toHaveBeenCalledWith('123456', 'accountStore.contact.copied')
  })

  it('renders an uploaded product icon image before the built-in icon', () => {
    mockAppStore.cachedPublicSettings = {
      account_store_config: {
        enabled: true,
        title: '站长自营',
        description: '纯手搓账号，一号一 IP，稳定。',
        status_text: '人工服务正常',
        contact: {
          type: 'qq',
          value: '123456',
          label: '联系站长购买，请添加 QQ',
          copy_label: '复制 QQ'
        },
        disclaimer: '购买前请确认库存。',
        products: [
          {
            id: 'claude',
            enabled: true,
            title: 'Claude 成品账号',
            subtitle: '适合 Claude 使用',
            price: '35',
            currency: '¥',
            unit: '/个',
            badge: '账号服务',
            icon: 'key',
            icon_image: 'data:image/webp;base64,Y2xhdWRlLWljb24=',
            color: 'purple',
            features: ['提供登录邮箱'],
            risk_note: ''
          }
        ]
      }
    }

    const wrapper = mountView()

    const image = wrapper.get('[data-testid="product-icon-image"]')
    expect(image.attributes('src')).toBe('data:image/webp;base64,Y2xhdWRlLWljb24=')
    expect(image.attributes('alt')).toBe('Claude 成品账号')
    expect(wrapper.find('[name="key"]').exists()).toBe(false)
  })
})
