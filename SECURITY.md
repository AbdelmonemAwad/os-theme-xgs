# Security

## Reporting a vulnerability

**Not in a public issue, please.** Report it privately through GitHub -
[**Report a vulnerability**](https://github.com/AbdelmonemAwad/os-theme-xgs/security/advisories/new),
on the Security tab - where only you and the owner see it, and the fix can be prepared before anything is
public. Without a GitHub account, write to **security@npuforge.org**. Either way, include:

- what is affected - the stylesheets, the switcher of xgs-auto, the installer and the scripts beside it;
- the version you installed and the OPNsense version;
- how to reproduce it, and what you saw.

This is one person's project, worked on in the evenings: expect an answer within days, not hours.
A fix is made in a pull request and the reporter credited in it, unless they ask not to be.

## What is supported

The newest version on `main`, and the newest release where there are releases. Fixes go there,
with no backports.

## Worth knowing before you report

- **A theme is code the GUI runs on every page.** A stylesheet or the switcher that loads anything from outside the appliance, or hides a warning OPNsense shows, is a vulnerability: report it here, privately.
- The installer runs as root: anything that makes it write outside the theme directory of OPNsense is a vulnerability.
- **Never send a configuration backup.** It holds keys and passwords.
