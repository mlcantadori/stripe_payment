## How to run locally

## 1. Clone the project

```
git clone https://github.com/mlcantadori/stripe_payment.git
```

## 2. Change environment variables
Copy the .env-example file into a file named .env (stripe_payment_project/.env).

You will need a Stripe account in order to run the project. Once you set up your account, go to the Stripe [developer dashboard](https://stripe.com/docs/development#api-keys) to find your API keys.

```
STRIPE_API_KEY=<replace-with-your-secret-key>
STRIPE_PUBLISHABLE_KEY=<replace-with-your-publishable-key>
```

## 3. Run a webhook locally

To test the integration with a local webhook on your machine, use the Stripe CLI to spin one up.

First [install the CLI](https://stripe.com/docs/stripe-cli) and [link your Stripe account](https://stripe.com/docs/stripe-cli#link-account).

```
stripe listen --forward-to localhost:8000/webhook
```

The CLI will print a webhook secret key to the console. Set `STRIPE_ENDPOINT_SECRET` to this value in your .env file.

You should see events logged in the console where the CLI is running.

## 4. Run the project using Docker

**Requirements**
- Docker
- [Configured .env file]

Open a new console in this project root directory and run the following command:

```
docker-compose up
```

Go to `localhost:8000` in your browser to see the project running.

## 5. Test the integration
Use the below test card numbers with any CVC code, a future expiration date and any zip code to test for certain behaviors.

Test card number:

**4242424242424242**: Integration handles payments that don’t require authentication

**4000002500003155**: Displays a pop-up modal to authenticate; integration handles payments that require authentication

**4000000000009995**: Integration handles card declines codes like insufficient_funds

All successful transactions will generate a line in the log file `successful_payments.log`


**Thanks!**

[@mlcantadori](https://github.com/mlcantadori)
