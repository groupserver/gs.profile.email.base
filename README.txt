=========================
``gs.profile.email.base``
=========================
------------------------
Core email settings code
------------------------

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2013-06-25
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.


Introduction
============

Email addresses in GroupServer_ are quite different to most systems: people
can have **multiple addresses** associated with a profile. This opens up
Pandora's Box and releases all the Preferences into the World. This product
is responsible for recording and reporting these settings; changing the
email settings is handled by ``gs.profile.email.settings``
[#settings]_. The complexities of verifying email addresses is handled in
``gs.profile.email.verify`` [#verify]_.

Vocabularies
============

Two *named vocabularies* are provided by this product:

``EmailAddressesForUser``:
  Provides a list of email addresses for the supplied user-info.

``EmailAddressesForLoggedInUser``:
  Provides a list of email addresses for the currently logged in user.

The latter is often used to provide an email-address selector::

    fromAddress = Choice(title=u'Email From',
        description=u'The email address that you want in the "From" '
                    u'line in the email you send.',
        vocabulary = 'EmailAddressesForLoggedInUser',
        required=True)

Email User
==========

The email user provides information about a person and his or her email
addresses.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.profile.email.base
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/

.. [#settings] See
               <https://source.iopen.net/groupserver/gs.profile.email.settings>
.. [#verify] See <https://source.iopen.net/groupserver/gs.profile.email.verify>

..  LocalWords:  nz GSProfile TODO redirector LocalWords
