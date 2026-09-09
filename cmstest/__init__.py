"""cmstest: a pytest + Playwright + Allure template for testing a content CMS.

Three layers share one registry (``cmstest.registry``):

* ``models``  -- pydantic request models that generate payloads with Faker;
* ``pages/cms`` -- Playwright page objects that fill the admin-panel forms;
* ``pages/site`` -- Playwright page objects that check the public rendering.
"""
