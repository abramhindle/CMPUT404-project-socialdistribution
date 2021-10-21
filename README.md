# social.distance

`social.distance` is a project forked from [CMPUT404-project-socialdistribution](https://github.com/abramhindle/CMPUT404-project-socialdistribution). It is a course project for CMPUT404, Fall2021.

See project.org (plain-text/org-mode) for a description of the project.

CMPUT404F21T01 Members:

Format: Name (github id, ccid)
- Lucas Zeng (c25vdw, zichang)
- Ze Hui Peng (zhpeng811, zhpeng)
- Sang Le (sqle157, sqle)
- Khang Vuong (kdvuong, kdvuong)
- Quoc Trung Tran (QuocTrungTran, quoctrun)

## Development Setup

1. Create `.env` at the project root. In the file, put
```
SECRET_KEY=a_very_long_bunch_of_chars
DEBUG=True

# belows are optional
# for format of database url, see https://github.com/jacobian/dj-database-url#url-schema
DATABASE_URL=sqlite:///db.sqlite3
EXTRA_ALLOWED_HOST=["0.0.0.0", "localhost", "whatever_domain_you_are_hosting_the_app"]
# allow react CORS? not tested
EXTRA_ALLOWED_ORIGINS=["http://localhost:8080"]
```
make sure the `SECRET_KEY` value is different than the example.

You can generate a `SECRET_KEY` [here](https://djecrety.ir/)

2. Activate virtualenv.

3. `pip install -r requirements.txt`

## Deploying API

heroku project at https://social-distance-api.herokuapp.com/ will update when `master` is updated by a merge or direct push.

## Contributing

Send a pull request and be sure to update this file with your name.

## Contributors / Licensing

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

Contributors:

    Karim Baaba
    Ali Sajedi
    Kyle Richelhoff
    Chris Pavlicek
    Derek Dowling
    Olexiy Berjanskii
    Erin Torbiak
    Abram Hindle
    Braedy Kuzma
    Nhan Nguyen 
