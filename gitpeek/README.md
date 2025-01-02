This tutorial stored the client secret in a gitignored .env file and accessed the value with ENV.fetch. When you deploy your app, you should choose a secure way to store the client secret and update your code to get the value accordingly.

For example, you can store the secret in an environment variable on the server where your application is deployed. You can also use a secret management service like Azure Key Vault.

Before you deploy your app, you should update the callback URL to use the callback URL that you use in production.
