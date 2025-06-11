# ✅ Set your Stripe API keys
import stripe
stripe.api_key = "sk_test_51Qz9HnBebPTU6EeSFUtxCE2vAnVjVUCpLXP7rH8kT1M0H1QDXUOr64khmq6ag0IHl94O1ICOxuAV3NYhDuWnia5j00ajTBTsod"

# ✅ Define product prices (you need to create them on your Stripe Dashboard)
STRIPE_PRICES = {
    "monthly": "price_1QznNyBebPTU6EeSH732tg6X",  # Replace with your Stripe price ID for Monthly Subscription
    "yearly": "price_YYYYYYYYYYYYYY"   # Replace with your Stripe price ID for Yearly Subscription
}

