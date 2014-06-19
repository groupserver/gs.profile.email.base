=========================
``gs.profile.email.base``
=========================
------------------------
Core email settings code
------------------------

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-06-19
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.


Introduction
============

Email addresses in GroupServer_ are quite different to most
systems: people can have **multiple addresses** associated with a
profile. This opens up Pandora's Box and releases all the
Preferences into the World. This product is responsible for
recording and reporting these settings; changing the email
settings is handled by ``gs.profile.email.settings``
[#settings]_. The complexities of verifying email addresses is
handled in ``gs.profile.email.verify`` [#verify]_.

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

:See also: The getters_.

Email User
==========

The email user provides information about a person and his or her email
addresses.

Factories
---------

``gs.profile.email.base.interfaces.IGSEmailUser(user)``:
  The adaptor to create an email user from either a ``ICustomUser`` or a
  ``IGSUserInfo``.

``EmailUserFromUser(customUser)``:
  Create an email user from a ``ICustomUser``.

``EmailUser(userInfo)``:
  Create an email user from an ``IGSUserInfo``.

``createObject('groupserver.EmailUserFromEmailAddress', context, addr)``:
  The ZCA factory to create an email user from an address and Zope context.

``EmailUserFromEmailAddressFactory(context, address)``:
  Create an email user from an email address (and Zope context).


Methods
-------

Getters
~~~~~~~

See also the vocabularies_.

``get_addresses``:
  Get all the addresses associated with the user.

``get_verified_addresses``:
  Get all the addresses associated with the user that have been verified.

``get_unverified_addresses``:
  Get all the addresses associated with the user that are yet to be
  verified.

``get_delivery_addresses``:
  Get all the addresses associated with the user that are set to
  default-delivery (preferred).

``is_address_verified(address)``:
  Returns ``True`` if the address is verified, ``False`` otherwise. Raises
  the ``gs.profile.email.base.AddressMissingError`` error_ if the email-user
  lacks the address.

Setters
~~~~~~~

``set_delivery(address)``: 
    Set the address to be a delivery address. 

``drop_delivery(address)``:
   Remove the address from the list of delivery addresses.

``add_address(address, isPreferred=False)``:
    Associate an address with the user, optionally setting to be a delivery
    address. Raises the ``gs.profile.email.base.AddressExistsError``
    error_ if the email-user already has the address.

``remove_address(address)``:
    Remove an address from the user. Raises the
    ``gs.profile.email.base.AddressMissingError`` error_ if the email-user
    lacks the address.

Error
-----

The errors raised by the email user are a subclass of
``gs.profile.email.base.AddressErrror`` (itself a subclass of
``ValueError``). They have the following attributes.

``userId``: 
    The ID of the user with the error.

``address``: 
    The email-address that caused the problem.

There are two possible errors that are raised: one for when an address
exists (and it shouldn't) and one for when it is missing (and it should
exist).

:``gs.profile.email.base.AddressExistsError``:
    Raised when an email address that has been passed in as an argument
    already is part of a profile.

:``gs.profile.email.base.AddressMissingError``:
    Raised when an email address that has been passed in as an argument is
    missing from a profile.

``sanitise_address``
====================

Sanitise an email address, being tolerant of what people enter.

:Synopsis:  ``sanitise_address(emailAddress)``
:Description: This function sanitises an email address, returning the
              *addr-spec* portion stripped of odd characters. The 
              *display-name* portion, if present, is discarded.
:Arguments: ``emailAddress``: An email address, as a string.
:Returns: A sane email address (as a string).
:See also: `RFC 5322`_, ``parseaddr`` [#parseAddr]_

.. _RFC 5322: http://tools.ietf.org/html/rfc5322

Subscriber
==========

The ``remove_email_data`` subscriber listens for the
``zope.app.container.interfaces.IObjectRemovedEvent`` event on a
``Products.CustomUserFolder.interfaces.ICustomUser`` and removes
all the email addresses from the database.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.profile.email.base
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

.. [#settings] See
               <https://source.iopen.net/groupserver/gs.profile.email.settings>
.. [#verify] See <https://source.iopen.net/groupserver/gs.profile.email.verify>
.. [#parseAddr] See
               <http://docs.python.org/2.7/library/email.util.html#email.utils.parseaddr>

..  LocalWords:  nz GSProfile TODO redirector LocalWords
