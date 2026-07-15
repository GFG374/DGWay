# Configurable Account Store Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the account-store page editable from system settings, including contact info and a dynamic product list.

**Architecture:** Store one JSON document in the existing `settings` table under `account_store_config`. Admin settings reads and writes the JSON; public settings exposes it to the frontend; the user page renders configured products with current default products as fallback.

**Tech Stack:** Go backend settings service and handlers, Vue 3 admin/user frontend, Vitest focused tests, existing Docker deployment.

---

### Task 1: Backend Settings Contract

**Files:**
- Modify: `backend/internal/service/domain_constants.go`
- Modify: `backend/internal/service/settings_view.go`
- Modify: `backend/internal/service/setting_parse.go`
- Modify: `backend/internal/service/setting_update.go`
- Modify: `backend/internal/service/setting_public.go`
- Modify: `backend/internal/handler/dto/settings.go`
- Modify: `backend/internal/handler/setting_handler.go`
- Modify: `backend/internal/handler/admin/setting_handler.go`
- Modify: `backend/internal/handler/admin/setting_handler_update.go`
- Test: `backend/internal/service/setting_service_public_test.go`

- [ ] Add `SettingKeyAccountStoreConfig = "account_store_config"` with a safe default JSON string.
- [ ] Add `AccountStoreConfig` DTO structs for page config and product config.
- [ ] Parse invalid or empty JSON as the default three products.
- [ ] Include `account_store_config` in admin and public settings responses.
- [ ] Validate admin saves: max 24 products, required title for enabled products, non-negative price, bounded string lengths.
- [ ] Run `go test ./backend/internal/service ./backend/internal/handler ./backend/internal/handler/dto`.

### Task 2: Frontend Types and User Page

**Files:**
- Modify: `frontend/src/types/index.ts`
- Modify: `frontend/src/api/admin/settings.ts`
- Modify: `frontend/src/views/user/AccountStoreView.vue`
- Test: `frontend/src/views/user/__tests__/AccountStoreView.spec.ts`

- [ ] Add `AccountStoreConfig` and `AccountStoreProduct` frontend types.
- [ ] Render products from `appStore.cachedPublicSettings.account_store_config`, falling back to defaults.
- [ ] Keep desktop grid at three cards per row, then wrap.
- [ ] Render icon choices without remote assets.
- [ ] Split feature strings by `,` and `，` when needed.
- [ ] Run the focused user page test.

### Task 3: Admin Settings Form

**Files:**
- Modify: `frontend/src/views/admin/SettingsView.vue`
- Modify: `frontend/src/i18n/locales/zh/common.ts`
- Modify: `frontend/src/i18n/locales/en/common.ts`
- Test: existing admin settings typecheck/build

- [ ] Add an “账号购买设置” card in the general settings tab.
- [ ] Add page-level fields for enabled, title, description, status, contact type/value, contact label, copy button, disclaimer.
- [ ] Add product list fields for enabled, title, subtitle, price, currency, unit, badge, icon, color, features, risk note.
- [ ] Add product add, copy, remove, up, down actions.
- [ ] Serialize feature input by splitting on Chinese and English commas.
- [ ] Include `account_store_config` in `saveSettings`.
- [ ] Run `pnpm --dir frontend run typecheck` and `pnpm --dir frontend run build`.

### Task 4: Docs, Merge, Deploy

**Files:**
- Modify: `docs/DGWAY_USAGE_CN.md`
- Modify: `docs/DGWay-API-设置与盈利.md` if the file exists and has relevant account-store/commercialization content.

- [ ] Document how to edit account-store products in system settings.
- [ ] Run focused tests and production build.
- [ ] Commit and push to GitHub main.
- [ ] Build `dgway-local:amd64`, load it on the VPS, recreate only `sub2api`.
- [ ] Verify Docker Compose health, `https://dgth.shop/health`, and `https://dgth.shop/account-store`.
