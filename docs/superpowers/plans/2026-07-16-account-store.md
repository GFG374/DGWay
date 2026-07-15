# DGWay Account Store Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the approved account-store page to the authenticated DGWay UI and deploy it to the production VPS.

**Architecture:** Implement a static Vue view that reads the existing public `contact_info` setting and uses the existing clipboard composable. Register the view in the authenticated router and shared self-navigation builder so users and administrators see the same entry. No backend, order, inventory, or payment state is added.

**Tech Stack:** Vue 3, TypeScript, Vue Router, Pinia, vue-i18n, Tailwind CSS, Vitest, Docker Compose.

---

### Task 1: Lock Page Behavior With Tests

**Files:**
- Create: `frontend/src/views/user/__tests__/AccountStoreView.spec.ts`
- Modify: `frontend/src/components/layout/__tests__/AppSidebar.spec.ts`

- [ ] **Step 1: Write the failing page test**

Mount `AccountStoreView` with `AppLayout` and `Icon` stubbed. Assert that the three products, prices, OpenAI logo, configured QQ, and copy button render. Mock `useClipboard` and assert clicking the button calls `copyToClipboard('484018742', 'accountStore.contact.copied')`.

- [ ] **Step 2: Write the failing navigation test**

Read `AppSidebar.vue` as source and assert it contains `path: '/account-store'`, `t('nav.accountStore')`, and `AccountStoreIcon`.

- [ ] **Step 3: Verify the tests fail for the missing feature**

Run:

```bash
cd frontend
npm run test:run -- src/views/user/__tests__/AccountStoreView.spec.ts src/components/layout/__tests__/AppSidebar.spec.ts
```

Expected: the page import is missing and the sidebar source assertions fail.

### Task 2: Implement the Account Store Page

**Files:**
- Create: `frontend/src/views/user/AccountStoreView.vue`

- [ ] **Step 1: Add the production page**

Use `<AppLayout>` with a responsive three-card grid. Render the approved account, phone, and residential-IP copy. Inline the OpenAI mark as an accessible SVG; use existing `Icon` components for phone, network, check, message, and copy visuals. Compute the QQ as `appStore.contactInfo.trim() || '484018742'` and call the existing `useClipboard` composable.

- [ ] **Step 2: Verify page tests pass**

Run:

```bash
cd frontend
npm run test:run -- src/views/user/__tests__/AccountStoreView.spec.ts
```

Expected: all account-store page tests pass.

### Task 3: Add Route, Navigation, and Locales

**Files:**
- Modify: `frontend/src/router/index.ts`
- Modify: `frontend/src/components/layout/AppSidebar.vue`
- Modify: `frontend/src/i18n/locales/zh/common.ts`
- Modify: `frontend/src/i18n/locales/en/common.ts`
- Modify: `frontend/src/i18n/locales/zh/misc.ts`
- Modify: `frontend/src/i18n/locales/en/misc.ts`

- [ ] **Step 1: Register the authenticated route**

Add `/account-store` beside `/purchase`, lazy-load `AccountStoreView.vue`, require authentication, and use `accountStore.title` and `accountStore.description` route metadata.

- [ ] **Step 2: Add the shared sidebar entry**

Create a shopping-bag line icon component and insert `{ path: '/account-store', label: t('nav.accountStore'), icon: AccountStoreIcon }` between purchase and orders in `buildSelfNavItems`.

- [ ] **Step 3: Add complete Chinese and English messages**

Add navigation, page title, product names, prices, feature copy, risk notes, contact labels, and copied-state messages. Keep the approved Chinese copy verbatim and provide clear English fallback copy.

- [ ] **Step 4: Verify navigation and page tests pass**

Run:

```bash
cd frontend
npm run test:run -- src/views/user/__tests__/AccountStoreView.spec.ts src/components/layout/__tests__/AppSidebar.spec.ts
```

Expected: both test files pass.

### Task 4: Update User Documentation

**Files:**
- Modify: `docs/DGWAY_USAGE_CN.md`

- [ ] **Step 1: Document the purchase flow**

Add a user-facing section explaining where to find “账号购买”, the three listed services, that delivery is manual, and that users copy QQ `484018742` to contact the administrator. Preserve unrelated existing edits in the file and stage only this task's hunk.

### Task 5: Verify, Commit, and Push

**Files:**
- All files changed in Tasks 1-4.

- [ ] **Step 1: Run focused tests**

```bash
cd frontend
npm run test:run -- src/views/user/__tests__/AccountStoreView.spec.ts src/components/layout/__tests__/AppSidebar.spec.ts
```

- [ ] **Step 2: Run frontend typecheck and production build**

```bash
cd frontend
npm run typecheck
npm run build
```

- [ ] **Step 3: Inspect the diff and commit only related changes**

Run `git diff --check`, explicitly stage page, tests, route, sidebar, locales, plan, and only the related usage-guide hunk, then commit with `feat: add user account store`.

- [ ] **Step 4: Push main to GitHub**

Run `git push origin main` and verify the remote accepts the commit.

### Task 6: Deploy and Verify Production

**Files:**
- Server checkout: `/opt/dgway-deploy`

- [ ] **Step 1: Update the server checkout**

SSH to `149.104.69.175` with `~/.ssh/lightnode_sub2api_rsa`, fast-forward the deployment checkout, and rebuild/recreate the application through the existing Docker Compose workflow. Do not create long-lived binary backups.

- [ ] **Step 2: Verify containers and public site**

Confirm all Compose services are healthy, `https://dgth.shop/account-store` returns the SPA successfully, and key public API endpoints still return success.

- [ ] **Step 3: Visually verify desktop and mobile**

Capture the production page at desktop and mobile viewport sizes. Confirm all three icons render, cards do not overlap, text fits, and the QQ copy button is visible and usable.
