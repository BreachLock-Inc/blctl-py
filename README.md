# blctl

Command-line interface for [BreachLock AEV](https://www.breachlock.com/products/adversarial-exposure-validation/), designed for use in CI/CD pipelines. Start network and web application pentest engagements against your infrastructure directly from the terminal or your pipeline scripts.

![Logo](https://github.com/BreachLock-Inc/blctl-py/raw/main/logo.svg)

## Requirements

- Python 3.11+
- A [BreachLock AEV](https://www.breachlock.com/products/adversarial-exposure-validation/) subscription with API access enabled on your account

## Installation

```bash
pip install breachlock-blctl
```

## Configuration

`blctl` reads credentials and tenant settings from environment variables. Set these before running any commands:

| Variable | Description |
|---|---|
| `BLCTL_API_KEY` | BreachLock API key (Bearer token) |
| `BLCTL_API_URL` | Base URL of your AEV tenant (e.g. `https://tenant.app.breachlock.com`) |
| `BLCTL_ORGANIZATION_ID` | Organization ID (CUID) — required for external engagements |

All three can also be passed as explicit flags (`--api-key`, `--api-url`, `--organization-id`), but using environment variables keeps secrets out of shell history and CI logs.

## Usage

### `blctl engage`

Starts a pentest engagement against BreachLock AEV and prints the created engagement as JSON.

```
blctl engage --type <network|web> (--external|--internal) --name <name> [OPTIONS]
```

#### Engagement type and direction

| Flag | Description |
|---|---|
| `--type network` | Network pentest |
| `--type web` | Web application pentest |
| `--external` | Scan externally reachable targets (mutually exclusive with `--internal`) |
| `--internal` | Scan internal targets via a deployed agent (mutually exclusive with `--external`) |

#### Target selection

| Flag | Description |
|---|---|
| `--targets <ip,host,...>` | Comma-separated IPs or hostnames to scan. Each is registered as an external asset before the engagement starts. External only. |
| `--asset-id <CUID>` | Asset ID to include. Repeatable. For `--external`, combinable with `--targets`. For `--internal`, at least one is required. |
| `--organization-id <CUID>` | Organization ID. Required for `--external`. Defaults to `$BLCTL_ORGANIZATION_ID`. |
| `--deployment-id <CUID>` | Deployment ID. Required for `--internal`. |

#### Scan controls

| Flag | Default | Description |
|---|---|---|
| `--scan-intensity` | `NORMAL` | `STEALTH`, `QUIET`, `POLITE`, `NORMAL`, `AGGRESSIVE`, or `EXTREME`. Affects host timeout and scan depth. |
| `--severity-threshold` | `NONE` | Minimum result severity: `NONE`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`. |
| `--confidence-threshold` | `VERY_LOW` | Minimum vulnerability confidence: `VERY_LOW`, `LOW`, `MEDIUM`, `HIGH`, `VERY_HIGH`. |

#### Feature flags

| Flag | Default | Description |
|---|---|---|
| `--exploitation` / `--no-exploitation` | `false` for network, `true` for web | Attempt exploitation. |
| `--credential-recovery` / `--no-credential-recovery` | `false` | Attempt credential recovery. |
| `--tailored-remediation` / `--no-tailored-remediation` | `false` | Provide tailored remediation advice. |
| `--screenshots` / `--no-screenshots` | `false` | Capture screenshots during the engagement. |
| `--learn-findings` / `--no-learn-findings` | `false` for network, `true` for web | Feed findings into the BreachLock learning pipeline. |
| `--learn-exploits` / `--no-learn-exploits` | `false` for network, `true` for web | Feed exploits into the BreachLock learning pipeline. |

#### Network reconnaissance (network engagements only)

| Flag | Default | Description |
|---|---|---|
| `--advanced-network-recon` / `--no-advanced-network-recon` | `false` | Run advanced network reconnaissance. |
| `--advanced-web-server-recon` / `--no-advanced-web-server-recon` | `false` | Run advanced web server reconnaissance. |
| `--active-directory-recon` / `--no-active-directory-recon` | `false` | Run Active Directory reconnaissance. |
| `--azure-ad-recon` / `--no-azure-ad-recon` | `false` | Run Azure AD reconnaissance. Only valid with `--type=network --internal`. |

#### Web application credentials (web engagements only)

Provide these to enable authenticated scanning. `--username` and `--password` must be supplied together, or omitted together for an unauthenticated scan. `--totp-secret` requires both.

| Flag | Env var | Description |
|---|---|---|
| `--username` | `BLCTL_WEB_USERNAME` | Username the agent uses to log in to the target application. |
| `--password` | `BLCTL_WEB_PASSWORD` | Password for the above username. Prefer the env var to keep it out of logs. |
| `--totp-secret` | `BLCTL_WEB_TOTP_SECRET` | Base32 TOTP shared secret for MFA. Prefer the env var. |

#### Filtering

| Flag | Description |
|---|---|
| `--excluded-protocol <id>` | Protocol ID or code to exclude. Repeatable. |
| `--excluded-finding <id>` | Finding ID or code to exclude. Repeatable. |
| `--excluded-cve <CVE-ID>` | CVE to exclude. Repeatable. |
| `--included-cve <CVE-ID>` | CVE to explicitly include. Repeatable. |

#### Webhooks and assessments

| Flag | Description |
|---|---|
| `--notify-url <spec>` | Webhook URL to call on engagement updates. Repeatable. Pass a bare URL (`https://hook/`) or a URL with pipe-separated headers (`https://hook/\|Authorization=Bearer abc\|X-Trace=42`). |
| `--threat-actor-assessment-id <CUID>` | Threat actor assessment to associate with the engagement. Repeatable. |

## Examples

### External network scan

```bash
export BLCTL_API_KEY="your-api-key"
export BLCTL_API_URL="https://tenant.app.breachlock.com"
export BLCTL_ORGANIZATION_ID="org-cuid"

blctl engage \
  --type network \
  --external \
  --name "Weekly perimeter scan" \
  --targets "203.0.113.10,203.0.113.11" \
  --scan-intensity AGGRESSIVE \
  --advanced-network-recon \
  --active-directory-recon
```

### External web application scan with authenticated scanning

```bash
export BLCTL_WEB_USERNAME="testuser@example.com"
export BLCTL_WEB_PASSWORD="s3cr3t"
export BLCTL_WEB_TOTP_SECRET="BASE32SECRET"

blctl engage \
  --type web \
  --external \
  --name "Sprint 42 web scan" \
  --targets "app.example.com" \
  --screenshots \
  --tailored-remediation \
  --severity-threshold MEDIUM
```

### Internal network scan via deployed agent

```bash
blctl engage \
  --type network \
  --internal \
  --name "Internal audit Q3" \
  --deployment-id "dep-cuid" \
  --asset-id "asset-cuid-1" \
  --asset-id "asset-cuid-2" \
  --azure-ad-recon \
  --advanced-network-recon
```

### Webhook notification with auth header

```bash
blctl engage \
  --type web \
  --external \
  --name "Nightly scan" \
  --targets "app.example.com" \
  --notify-url "https://hooks.example.com/bl|Authorization=Bearer token123"
```

### CI/CD pipeline (GitHub Actions)

```yaml
- name: Start BreachLock engagement
  env:
    BLCTL_API_KEY: ${{ secrets.BLCTL_API_KEY }}
    BLCTL_API_URL: ${{ secrets.BLCTL_API_URL }}
    BLCTL_ORGANIZATION_ID: ${{ secrets.BLCTL_ORGANIZATION_ID }}
  run: |
    blctl engage \
      --type web \
      --external \
      --name "PR ${{ github.event.number }} scan" \
      --targets "${{ vars.SCAN_TARGET }}" \
      --severity-threshold HIGH \
      --no-learn-findings \
      --no-learn-exploits
```

### CI/CD pipeline (GitLab CI)

```yaml
breachlock-scan:
  stage: test
  script:
    - pip install breachlock-blctl
    - |
      blctl engage \
        --type web \
        --external \
        --name "MR $CI_MERGE_REQUEST_IID scan" \
        --targets "$SCAN_TARGET" \
        --severity-threshold HIGH \
        --no-learn-findings \
        --no-learn-exploits
  variables:
    BLCTL_API_KEY: $BLCTL_API_KEY
    BLCTL_API_URL: $BLCTL_API_URL
    BLCTL_ORGANIZATION_ID: $BLCTL_ORGANIZATION_ID
```

Store `BLCTL_API_KEY`, `BLCTL_API_URL`, and `BLCTL_ORGANIZATION_ID` as [masked CI/CD variables](https://docs.gitlab.com/ee/ci/variables/) in your project or group settings. `SCAN_TARGET` can be a plain variable.

## Output

On success, `blctl engage` prints the created engagement as JSON:

```json
{
  "id": "eng-cuid",
  "name": "Weekly perimeter scan",
  ...
}
```

On error, a non-zero exit code is returned and the error is written to stderr.
