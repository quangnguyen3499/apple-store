# TODO
- [ ] Apply invoice
- [ ] Implement amount (remaining amount) field for order
- [ ] Stripe: Payment with multi cards (select one)
- [ ] Implement OrderItem (Cart is deleted when checking out)

# e-commerce
# create file local.env, copy content from local.env.example and paste to local.env
# run migrate: python manage.py makemigrations & python manage.py migrate

# PAYMENT
# Stripe usage in this project:
# 1. Create customer
# 2. Add payment details
# 3. Create payment

# Stripe docs:
# 1. https://stripe.com/docs/api
# ...

# BROKER
# RabbitMQ

# CRONTAB
# celery
