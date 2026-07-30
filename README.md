# Encore

An event ticket reservation & booking API built with Django REST Framework.

## Overview

Encore lets users reserve a seat for an event, then pay for it via Stripe within a fixed window. If payment isn't completed in time, the reservation is automatically released so the seat becomes available again. Ticket and event data is indexed in Elasticsearch for fast search.

## Features

- JWT-based authentication (dj-rest-auth + SimpleJWT)
- Two-phase ticket booking: reserve → pay, with automatic expiry
- Stripe PaymentIntent integration with signature-verified webhooks
- Full-text search over events/performers via Elasticsearch
- Background processing with Celery + Celery Beat
- Fully dockerized local dev environment

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Auth:** dj-rest-auth, django-allauth, SimpleJWT
- **Database:** PostgreSQL
- **Search:** Elasticsearch (django-elasticsearch-dsl)
- **Task Queue:** Celery, Celery Beat, Redis
- **Payments:** Stripe
- **Containerization:** Docker, Docker Compose
- **Dev tooling:** Flower (Celery monitoring), RedisInsight, Mailpit (email testing)

## How Booking Works

1. A user reserves an available ticket, which locks the seat for a limited window.
2. The client creates a Stripe PaymentIntent and completes payment on the frontend.
3. Stripe confirms the payment via webhook, which marks the ticket as purchased.
4. If payment isn't completed in time, a scheduled Celery task releases the reservation and cancels the pending PaymentIntent.

## Getting Started

### Prerequisites

- Docker & Docker Compose
- A Stripe account (test mode keys are fine for development)

### Setup

1. Clone the repo.
2. Create a `.env` file in the project root with the variables listed below.
3. Start everything:

   ```bash
   docker compose up --build
   ```

   This spins up the API, Postgres, Redis, Elasticsearch, the Celery worker, Celery Beat, and the dev tools below.

### Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DB_NAME` / `DB_USER` / `DB_PASS` / `DB_HOST` | Postgres connection |
| `REDIS_URL` | Redis connection string (broker + cache) |
| `ELASTICSEARCH_HOST` | Elasticsearch endpoint |
| `STRIPE_SECRET_KEY` | Stripe API secret key |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret |

### Testing Stripe Webhooks Locally

Use the [Stripe CLI](https://stripe.com/docs/stripe-cli) to forward events to your local server (adjust the URL prefix to match your root `urls.py`):

```bash
stripe listen --forward-to localhost:8000/<your-url-prefix>/webhooks/stripe/
```

## Dev Tools

| Tool | URL | Purpose |
|---|---|---|
| Flower | http://localhost:5555 | Celery task monitoring |
| RedisInsight | http://localhost:5540 | Redis browser |
| Mailpit | http://localhost:8025 | Catches outgoing emails in dev |

## Status

API-only for now — a frontend may be added later.

## License

MIT