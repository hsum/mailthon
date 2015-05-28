"""
    mailthon.api
    ~~~~~~~~~~~~

    Implements simple-to-use wrapper functions over
    the more verbose object-oriented core.

    :copyright: (c) 2015 by Eeo Jun
    :license: MIT, see LICENSE for details.
"""


from mailthon.enclosure import HTML, Attachment, BinaryAttachment
from mailthon.envelope import Envelope
from mailthon.postman import Postman
from mailthon.middleware import TLS, Auth
import mailthon.headers as headers


def email(sender=None, receivers=(), cc=(), bcc=(),
          subject=None, content=None, encoding='utf8',
          attachments=(), binaries=()):
    """
    Creates an Envelope object with a HTML *content*.

    :param content: HTML content.
    :param encoding: Encoding of the email.
    :param attachments: List of filenames to
        attach to the email.
    """
    enclosure=[]
    enclosure.append(HTML(content, encoding))
    enclosure.extend(tuple(Attachment(k) for k in attachments))
    enclosure.extend(tuple(BinaryAttachment(k, t, f) for k, t, f in binaries))
    return Envelope(
        headers=[
            headers.subject(subject),
            headers.sender(sender),
            headers.to(*receivers),
            headers.cc(*cc),
            headers.bcc(*bcc),
            headers.date(),
            headers.message_id(),
        ],
        enclosure=enclosure,
    )


def postman(host, port=587, auth=(None, None),
            force_tls=False, options=None):
    """
    Creates a Postman object with TLS and Auth
    middleware.

    :param auth: Tuple of (username, password) to
        be used to ``login`` to the server.
    :param force_tls: Whether TLS should be forced.
    :param options: Dictionary of keyword arguments
        to be used when the SMTP class is called.
    """

    username, password = auth
    return Postman(
        host=host,
        port=port,
        options=options,
        middlewares=[
            TLS(force=force_tls),
            Auth(username, password),
        ],
    )
