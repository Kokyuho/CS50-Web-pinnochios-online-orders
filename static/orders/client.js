// A reference to Stripe.js initialized with your real test publishable API key.
var stripe = Stripe("pk_test_CrklCo9XrobhOg3shK0Du21T00qA3xLdZq");

// Disable the button until we have Stripe set up on the page
document.querySelector("button").disabled = true;

// Fetch a payment intent as soon as the page loads
fetch("{% url 'createPaymentIntent' %}", {
    method: "POST",
    headers: {
    "Content-Type": "application/json"
    },
    // body: JSON.stringify(purchase)
})
.then(function(result) {
    return result.json();
})
.then(function(data) {
    var elements = stripe.elements();

    var style = {
        base: {
            color: "#32325d",
            fontFamily: 'Roboto, sans-serif',
            fontSmoothing: "antialiased",
            fontSize: "16px",
            "::placeholder": {
            color: "#32325d"
            }
        },
        invalid: {
            fontFamily: 'Roboto, sans-serif',
            color: "#fa755a",
            iconColor: "#fa755a"
        }
      };

    var card = elements.create("card", { style: style });

    // Stripe injects an iframe into the DOM
    card.mount("#card-element");

    // Complete payment when the submit button is clicked
    var form = document.getElementById("payment-form");
    form.addEventListener("submit", function(event) {
    event.preventDefault();
    payWithCard(stripe, card, data.clientSecret);
    });
});


// Calls stripe.confirmCardPayment
// If the card requires authentication Stripe shows a pop-up modal to
// prompt the user to enter authentication details without leaving your page.
var payWithCard = function(stripe, card, clientSecret) {
    // loading(true);
    stripe
        .confirmCardPayment(clientSecret, {
            payment_method: {
                card: card
            }
        })
        .then(function(result) {
            if (result.error) {
                // Show error to your customer
                showError(result.error.message);
                // console.log(result.error.message);
            } else {
                // The payment succeeded!
                window.location.replace("{% url 'orderPlaced' %}");
                // orderComplete(result.paymentIntent.id);
            }
        });
};
