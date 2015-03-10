Changelog
=========

3.0.2 (2015-03-10)
------------------

* Handling email addresses with ``+`` characters in them, partly
  closing `Bug 4036`_

.. _Bug 4036: https://redmine.iopen.net/issues/4036

3.0.1 (2014-10-07)
------------------

* Updating the metadata

3.0.0 (2014-06-19)
------------------

* Python 3 support
* Added unit tests
* Added a subscriber for the ``remove`` event
* Added a case-insensitive ``has_address`` method

2.1.0 (2014-02-11)
------------------

* Switching from ``assert`` statements in ``EmailUser``

2.0.0 (2014-01-31)
------------------

* Unicode update
* Adding the NewEmailAddress and EmailAddressExists to the
  general API

1.4.1 (2013-06-25)
------------------

* Code tidy-up

1.4.0 (2012-07-17)
------------------

* Adding ``EmailUser`` into the ``__init__`` for the product

1.3.0 (2012-06-22)
------------------

* Switching to ``gs.database``

1.2.1 (2011-11-03)
------------------

* Adding a note about the actual email address spec


1.2.0 (2011-04-27)
------------------

* Using the standard Python ``email.utils.parseaddr`` function
  for supporting full email addresses, closing `Issue 445
  <htps://redmine.iopen.net/issues/445>`_

1.1.0 (2011-02-23)
------------------

* Moved the ``check_email`` JavaScript here from
  ``Products.GSProfile``
* Added a method for getting the unverified email address

1.0.1 (2011-02-03)
------------------

* Fix for the adaptor configuration

1.0.0 (2011-01-26)
------------------

* Initial version
