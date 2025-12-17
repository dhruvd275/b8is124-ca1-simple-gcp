# B8IS124 CA1 – Cloud Application Deployment (GCP)

## Project Description
This project demonstrates the deployment of a cloud-based web application using **Google Cloud Platform (GCP)**.  
The application is built using **Python (Flask)**, hosted on **Google App Engine**, and uses **Google Cloud Firestore (Datastore mode)** for persistent data storage.  
A **CI/CD pipeline** is implemented using **Google Cloud Build**, which automatically deploys the application when code is pushed to GitHub.

---

## Live Application
The application is deployed and publicly accessible on Google App Engine.

- **Homepage:** `/`
- **Visual Demo (CRUD):** `/ui`

The `/ui` page allows users to:
- Add tasks
- View tasks
- Delete tasks  

All data is stored persistently in Firestore and remains available after redeployment.

---

## Google Cloud Services Used

### 1. Google App Engine
- Hosts the Flask web application
- Manages infrastructure, scaling, and HTTPS automatically
- Provides a public `appspot.com` URL

### 2. Google Cloud Firestore (Datastore mode)
- Managed NoSQL database
- Stores application data persistently
- Accessed from the Flask backend using the Datastore client

### Supporting Service: Google Cloud Build
- Implements CI/CD automation
- Automatically builds and deploys the app on GitHub push

---

## Application Architecture
Developer (Git Push)
|
v
GitHub Repository
|
v
Cloud Build (CI/CD)
|
v
Google App Engine (Flask App)
|
v
Firestore (Datastore mode)


Users interact with the application through a browser, which communicates with the Flask backend hosted on App Engine.  
The backend performs CRUD operations on Firestore.

---

## CI/CD Pipeline – How Cloud Build Deploys the App

# Step 1: Push code to GitHub
When code is pushed to the `main` branch:

```bash
git push origin main


# Step 2: Cloud Build trigger starts

A Cloud Build trigger is configured for:

Repository: b8is124-ca1-simple-gcp

Branch: main

Build config: cloudbuild.yaml

# Step 3: Cloud Build reads cloudbuild.yaml

Cloud Build executes the steps defined in cloudbuild.yaml.

# Step 4: Install dependencies

- name: "python:3.11"
  entrypoint: "bash"
  args:
    - "-c"
    - |
      cd app
      pip install -r requirements.txt


# Step 5: Deploy to App Engine

- name: "gcr.io/google.com/cloudsdktool/cloud-sdk:slim"
  entrypoint: "bash"
  args:
    - "-c"
    - |
      cd app
      gcloud app deploy app.yaml --quiet

This step deploys the application automatically to Google App Engine.

# Step 6: Logging and timeout

timeout: "1200s"
options:
  logging: CLOUD_LOGGING_ONLY
  default_logs_bucket_behavior: REGIONAL_USER_OWNED_BUCKET

These settings configure build timeout and logging behaviour.

#Firestore Usage

Firestore (Datastore mode) is used in the backend to store task data.

CRUD operations:

-Create: Add task via /add
-Read: Retrieve tasks via /tasks
-Delete: Remove task via /delete/<id>

Firestore is schemaless, so no database migration step is required.

Security and IAM

-Cloud Build uses a service account to deploy the application
-IAM roles allow App Engine deployment and Firestore access
-Permissions were configured for development purposes

Conclusion

This project demonstrates:

-Cloud application hosting using Google App Engine
-Persistent cloud data storage using Firestore
-Automated deployment using Cloud Build CI/CD
-Clear understanding of cloud architecture concepts
