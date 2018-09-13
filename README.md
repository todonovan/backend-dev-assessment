# Backend Developer Assessment

:wave: Hey there! If you are looking at this, then that means you have been selected to complete an assessment as part of the hiring process for a developer position at [Hire an Esquire](https://hireanesquire.com/).

We require all candidates to complete this assessment for a few reasons:

1. We want to have a better understanding about how you approach and solve problems
1. We can vet candidates more accurately with a common set of criteria to compare
1. Most importantly, we will analyze your deliverables as part of our in-person interview and use them to discuss your software development ideologies

> :question: If you have any questions along the way, you can contact [lenny@hireanesquire.com](mailto:lenny@hireanesquire.com). Please note that all code contained in this repository is provided as-is and we will not be able to provide any technical assistance for that.

You are welcome to copy or fork this repository to get started.

> :clock4: We estimate that this assessment can take anywhere from 1-4 hours to complete, based on individual skill level and implementation details. If you are unable to find enough time or believe this is unreasonable, please let us know and we will do our best to accomodate you.


## Challenge

We would like you to build an API to list and interact with candidates for a job opening.

You are free to use any tools or projects at your disposal. This repo contains a starter rails app and a starter django app that you can use to get started with if you choose to do so. If you choose to use the Django project, we recommend you use [Django Rest Framework](http://http://www.django-rest-framework.org/) to build the API.

## Prerequisites

Each starter project contains a Candidate Model definition with sample data.

## Requirements

Your API must meet the following requirements:

1. All data should be transferred via JSON (`Content-Type: application/json`)
1. Create a REST endpoint that allows CRUD (Create/Read/Update/Delete) operations for a single Candidate
1. Create a REST endpoint to list all candidates
    - This endpoint should optionally accept 2 query parameters:
        - One parameter should filter the results by the `reviewed` field
        - One parameter should sort the results by either the `status` or `date_applied` field
1. Enforce the following validation rules when updating a candidate:
    - All non-readonly fields should be editable
    - `years_exp` cannot be higher than 50
    - `status` can only be updated according to the following rules:
        - Pending candidates can be changed to Accepted or Rejected
        - Accepted, Rejected candidates can be changed to Pending
        - Accepted candidates cannot be changed to Rejected, and vice versa
1. Additionally, provide logic to automatically update the `reviewed` field according to the following rules:
    - When a candidate moves from Pending to Accepted or Rejected, `reviewed` should be set to `true`
    - If an Accepted or Rejected candidate is set back to Pending, `reviewed` should remain `true`

> :information_source: There are no frontend requirements. There are also no time limits, but we will not be able to schedule your interview until we receive your submission.

## Deliverables

Please provide a code repository with your source code and any necessary instructions for installing dependencies and running your application.
