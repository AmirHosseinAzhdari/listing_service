# Listing Service

***

a Simple Django reservation project using DRF and including features:
* class based views, viewsets and generics
* model serialization and validation
* code documentations
* Django models and ORM querysets
* unittest (for helper module)
* API documentations using swagger
* postman API test documentation


## API Documentations

To view the endpoints documents, you can open your run project in the browser.
For default: `http://127.0.0.1:8000/`


```
./manage.py runserver
```

## Test APIs

For test APIs import collection (`Listing Service.postman_collection.json`) in project root to your postman account.


## Run UnitTests

to run unittest for truly working project logic

```
./manage.py test listings.tests
```