=====
Django-Admeris-IOP
=====

Django-Admeris_IOP is a Python-Django port of the Salt/Admeris IOPHttpsTransaction libraries
to be used for Interac Online transactions via the vendor's API.

If you check out the vendor's libraries, this is not a rewrite, but rather a translation
of their libraries to one suitable for Python and Django. 

Detailed documentation for Admeris IOPHttpsTransaction is on the vendor's website.

http://www.admeris.com/developers/downloads/

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'IOPHttpsTransaction',
    )

2. Run `python manage.py migrate` to create the polls models.

3. Refer to the Admeris documentation for using this as your payment solution.

