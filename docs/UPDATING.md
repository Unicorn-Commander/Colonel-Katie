# 🔄 Updating Colonel Katie

This guide explains how to update your Colonel Katie installation to the latest version.

## Quick Update

For most users, simply run:

```bash
cd /path/to/Colonel-Katie
./update.sh
```

This will:
- Pull the latest code from GitHub
- Update dependencies
- Preserve your configuration and data

## Manual Update Process

### 1. Navigate to Installation Directory
```bash
cd /path/to/Colonel-Katie
```

### 2. Check Current Status
```bash
# Check for local changes
git status

# See current version
git log -1 --oneline
```

### 3. Pull Latest Changes
```bash
# Fetch and merge latest changes
git pull origin main
```

### 4. Update Dependencies
```bash
# For headless installations
./install-headless.sh

# For GUI installations
python install.py
```

## Advanced Update Options

### Using update-headless.sh

The `update-headless.sh` script provides more control:

```bash
./update-headless.sh
```

Features:
- Automatic backup of user data
- Stashes local changes
- Shows what will be updated
- Handles dependency updates
- Runs migration scripts

### Preserving Local Changes

If you have local modifications:

```bash
# Stash your changes
git stash

# Update
git pull origin main
./install-headless.sh

# Restore your changes
git stash pop
```

### Updating from a Specific Version

```bash
# Update to a specific tag
git fetch --tags
git checkout v2.1.0
./install-headless.sh
```

## What Gets Preserved

During updates, the following are preserved:

✅ **Always Preserved:**
- `~/.interpreter/config.yaml` - Your configuration
- `~/.interpreter/conversations/` - Chat history
- Custom profiles in `profiles/custom/`
- API keys and settings
- Virtual environment (updated in place)

⚠️ **May Be Overwritten:**
- Default profiles
- System scripts
- Documentation files
- Example configurations

## Rollback Process

If an update causes issues:

### 1. Check Backup Directory
```bash
# Backups are created automatically
ls -la .backup_*
```

### 2. Restore Previous Version
```bash
# Find previous commit
cat .backup_*/previous_version.txt

# Rollback to that version
git checkout [commit-hash]

# Reinstall dependencies
./install-headless.sh
```

### 3. Restore Configuration
```bash
# Copy back your config
cp .backup_*/config.yaml ~/.interpreter/config.yaml
```

## Automated Updates

### Using Cron

Add to crontab for weekly updates:
```bash
# Edit crontab
crontab -e

# Add this line (updates Sundays at 2 AM)
0 2 * * 0 cd /path/to/Colonel-Katie && ./update.sh >> /var/log/colonel-katie-update.log 2>&1
```

### Using systemd Timer

Create `/etc/systemd/system/colonel-katie-update.service`:
```ini
[Unit]
Description=Update Colonel Katie

[Service]
Type=oneshot
ExecStart=/path/to/Colonel-Katie/update.sh
User=your-username
```

Create `/etc/systemd/system/colonel-katie-update.timer`:
```ini
[Unit]
Description=Weekly Colonel Katie Update

[Timer]
OnCalendar=weekly
Persistent=true

[Install]
WantedBy=timers.target
```

Enable timer:
```bash
sudo systemctl enable colonel-katie-update.timer
sudo systemctl start colonel-katie-update.timer
```

## Update Notifications

To get notified about updates:

### 1. Watch GitHub Repository
- Go to https://github.com/Unicorn-Commander/Colonel-Katie
- Click "Watch" → "Custom" → "Releases"

### 2. Check for Updates Script
```bash
#!/bin/bash
# check-updates.sh

cd /path/to/Colonel-Katie
git fetch origin main

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "Updates available!"
    echo "Run: ./update.sh"
fi
```

## Troubleshooting Updates

### Permission Errors
```bash
# Fix ownership
sudo chown -R $USER:$USER /path/to/Colonel-Katie

# Fix permissions
chmod -R 755 /path/to/Colonel-Katie
```

### Dependency Conflicts
```bash
# Clean install dependencies
rm -rf venv
./install-headless.sh
```

### Git Conflicts
```bash
# Reset to clean state (WARNING: loses local changes)
git reset --hard origin/main

# Or stash and try again
git stash
git pull origin main
git stash pop
```

### Python Version Issues
```bash
# Check Python version
python3 --version

# If needed, specify Python version
python3.11 -m venv venv
source venv/bin/activate
./install-headless.sh
```

## Best Practices

1. **Backup Before Major Updates**
   ```bash
   cp -r ~/.interpreter ~/.interpreter.backup
   ```

2. **Test After Updating**
   ```bash
   ./katie --version
   ./test-installation.sh
   ```

3. **Read Release Notes**
   - Check [GitHub Releases](https://github.com/Unicorn-Commander/Colonel-Katie/releases)
   - Review [CHANGELOG.md](../CHANGELOG.md)

4. **Update Regularly**
   - Weekly or monthly updates recommended
   - Security updates should be applied immediately

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](./TROUBLESHOOTING.md)
2. Search [existing issues](https://github.com/Unicorn-Commander/Colonel-Katie/issues)
3. Open a new issue with:
   - Your Python version
   - Update error messages
   - Steps to reproduce

---

**Remember**: Colonel Katie is actively developed. Regular updates bring new features, improvements, and security fixes! 🦄⚡