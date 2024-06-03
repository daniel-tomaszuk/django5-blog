# django5-blog
Blog app with Django5.
Main aim is to have usage examples of different features in a blog app context. 

Common features:

* post comments,
* add post tags (`django-tagit`),
* post sharing with email notifications,
* suggesttions with most recent / most commented posts,
* posibility to do full text search with Postgres (stemming, ranking results, removing stop words, weighting queries, trigram),

Has examples of custom ORM object manager, custom teplate tags (simple tag and inclusion tag), pagination,
sitemap XML, RSS feed.


## Start the app  (virtual env recommended)
```
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver
```

TODO: add tests, fully docerize.
