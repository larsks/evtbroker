from setuptools import setup, find_packages

setup(
    name = "zmqevt",
    author = 'Lars Kellogg-Stedman',
    author_email = 'lars@seas.harvard.edu',
    version = "2",
    packages = find_packages(),
    scripts = [
        'bin/evtbroker',
        'bin/evtsub',
        'bin/evtpub',
        'bin/irssi-notify-modem',
        'bin/mail-notify-modem',
        'bin/imap-check',
        ],
)

