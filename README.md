# Benny Interview Task - Facebook OAuth2 Integration

## Overview

This project is a demo to integrate with Facebook(Meta) OAuth2 provider, pulled the logged in person's name 
and display on the screen.

This project is dockerized. We used Django/DRF for backend APIs, React for the frontend. 

I didn't embed React into Django template for following reasons: 

1. We'll want to develop backend and frontend separately when we have dedicated devs for backend and frontend. 
2. When we deploy backend and frontend to cloud, we can easily setup serverless and load balancing for backend and frontend. 

[Workflow Video](https://www.loom.com/share/2b5c6b1924c942a6ad3c45bccc3ee217)

## Get Started

### Install Docker

[Mac Install Guideline](https://docs.docker.com/desktop/install/mac-install/)

### Setup environment variables

Copy `backend/.env.example` to `backend/.env` and set environment variables with the info from 
your own Facebook app. 

### Run docker-compose

```bash
docker-compose up -d
```

### Run tests for backend

```bash
docker-compose run backend sh -c "python manage.py test"
```

### Run tests for frontend

```bash
docker-compose run frontend sh -c "npm test"
```

## Additional Notes

I implement oauth2 integration by focusing on having full control for oauth2 workflow. 
For example, we'd like to integrate this kind of authentication for other social networks 
such as LinkedIn, Google, Twitter, and Instagram. 

Let's take a quick example to build custom social posts app which allows users to publish the 
posts to LinkedIn, Twitter, Facebook and Instagram at one place. 

But, each social network have different workflow and different data structure for user profile info
and steps to publish posts. 

To make this more structured and scalable, we can abstract main workflow into abstract class
and override required methods inside each provider. For that purpose, I'd like to implement 
that for this simple authentication. Though we're currently implementing single social network,
it's designed to integrate other social networks easily and effectively. 

I can elaborate more in the technical interview if you have more questions. 

**Elapsed Time**: 5 hours
