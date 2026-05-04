## Known Issues

### Back Button Navigation

**Assumption:** Press back should take you on the previous page

**Failing Test:**

- [ ] `test_go_back_button_navigates_back_to_password_step` - Fails all browsers

**Details:** The browser back button doesn't navigate to the password step as expected. May require implementation review or test adjustment.

---

### Keyboard Navigation (WebKit Only)

**Assumption:** All browsers support standard keyboard navigation

**Failing Test:**

- [ ] `test_keyboard_navigation_email_step` - Fails only on WebKit browser

**Details:** WebKit browser has compatibility issues with keyboard navigation on the email input field.

---

## General Assumptions

- Test account email/password remain valid during test runs
- Hudl API is available and responsive
- Screenshots captured only on test failure (not on pass)
