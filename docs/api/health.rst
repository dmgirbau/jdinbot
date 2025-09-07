.. _api-health:

Health Endpoint
===============

.. http:get:: /v1/health

   Checks the health status of the JDINBot API and, in non-development environments, the database connection.

   **Example request**:

   .. sourcecode:: http

      GET /v1/health HTTP/1.1
      Host: localhost:8000
      Accept: application/json

   **Example response** (development mode):

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
          "status": "healthy",
          "api": "ok"
      }

   **Example response** (production mode, healthy database):

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
          "status": "healthy",
          "api": "ok",
          "database": "ok"
      }

   **Example response** (production mode, database error):

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
          "status": "unhealthy",
          "api": "ok",
          "database": "error: connection refused"
      }

   :statuscode 200: API is operational, with optional database status.