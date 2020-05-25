// Set your publishable key
var main_script = document.getElementById('main-script');
var publishable_key = main_script.getAttribute("publishable_key");
var stripe = Stripe(publishable_key);
var elements = stripe.elements();

// Set up Stripe.js and Elements to use in checkout form
var style = {
  base: {
    color: "#32325d",
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#aab7c4"
    }
  },
  invalid: {
    color: "#fa755a",
    iconColor: "#fa755a"
  }
};

var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

var form = document.getElementById('payment-form');
var clientSecret = document.getElementById('submit').getAttribute("data-secret");

form.addEventListener('submit', function(ev) {
  ev.preventDefault();
  changeLoadingState(true);
  stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: card,
      billing_details: {
        name: 'Jenny Rosen'
      }
    }
  }).then(function(result) {
    if (result.error) {
      var displayError = document.getElementById('card-errors')
      // Show error to your customer (e.g., insufficient funds)
      changeLoadingState(false);
      console.log(result.error.message);
      displayError.textContent = result.error.message;
    } else {
      // The payment has been processed!
      var displaySuccess = document.getElementById('success')
      var displayFeedback = document.getElementById('feedback')
      if (result.paymentIntent.status === 'succeeded') {
        changeLoadingState(false);
        document.querySelector("button").disabled = true;
        displaySuccess.textContent = 'Payment was successful!';
        displayFeedback.textContent = "(that's what she said!)";
      }
    }
  });
});

// Show a spinner on payment submission
var changeLoadingState = function(isLoading) {
  if (isLoading) {
    document.querySelector("button").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("button").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
};
