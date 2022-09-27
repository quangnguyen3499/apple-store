# TODO
- [ ] Apply invoice
- [ ] Implement amount (remaining amount) field for order
- [ ] Stripe: Payment with multi cards (select one)
- [ ] Implement OrderItem (Cart is deleted when checking out)

# e-commerce
# create file local.env, copy content from local.env.example and paste to local.env
# 1. Install docker & docker compose
# 2. Copy `dev.env` to `local.env`
# 3. Run docker-compose build
# 4. Run docker-compose up -d
# 5. Run docker-compose exec platform python manage.py migrate
# 6. Run docker-compose restart
# 7. Run docker-compose exec platform python manage.py createsuperuser


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
