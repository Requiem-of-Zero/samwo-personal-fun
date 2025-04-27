# Mail Fetching on macOS with Fetchmail & Procmail

This guide walks you through setting up **Fetchmail** and **Procmail** on macOS to retrieve and deliver your IMAP (Gmail) mail into your local mailbox accessible via the `mail` command.

---

## Prerequisites

- **Homebrew** installed. If you don’t have it:
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
- A Gmail account with an [App Password][app-pass] (needed if 2FA is enabled).

---

## 1. Install Required Tools

1. **Fetchmail**

   ```bash
   brew install fetchmail
   ```

2. **Procmail** (Mail Delivery Agent)

   ```bash
   brew install procmail
   ```

---

## 2. Configuration Files

### `~/.fetchmailrc`

Create or update your **Fetchmail** configuration in your home directory:

```bash˚
defaults
    proto IMAP
    timeout 30
    port 993
    ssl
    sslcertck

poll imap.gmail.com with proto IMAP
  user "youremail@gmail.com" there with password "YOUR_APP_PASSWORD"
  mda "$(which procmail) -d $USER"
  keep
EOF
```

- **Customize**:
  - `youremail@gmail.com` → your Gmail address
  - `YOUR_APP_PASSWORD` → your Gmail App Password
  - `mda` path → verifies via `which procmail` (e.g. `/opt/homebrew/bin/procmail`)

Set strict permissions:

```bash
chmod 600 ~/.fetchmailrc
```

- Create your `Maildir` if you prefer:
  ```bash
  maildirmake Maildir
  ```

---

## 3. Running Fetchmail

- **Check only** (no download):

  ```bash
  fetchmail -c -v
  ```

- **Fetch all mail**:

  ```bash
  fetchmail -v -a
  ```

On first run, all unseen messages (e.g. 70 000+ in Gmail) will be fetched and handed off to Procmail.

---

## 4. Verifying Mail Delivery

- **System mailbox**:

  ```bash
  ls -lh /var/mail/$USER
  mail    # launches the built‑in mail CLI
  ```

---

## 5. Using the `mail` Command & Filtering by Subject

Once mail is in your local mailbox, use the `mail` CLI:

```bash
mail
```

### Search by subject keyword (shell)

```bash
grep -n -i "^Subject:.*YourKeyword" /var/mail/$USER
```

---

## 6. File Summary

| File              | Purpose                                     |
| ----------------- | ------------------------------------------- |
| `~/.fetchmailrc`  | Fetchmail config (server, MDA, credentials) |
| `~/.procmailrc`   | Procmail delivery rules & logging           |
| `/var/mail/$USER` | System mailbox file                         |

---

Happy mailing! 🎉
